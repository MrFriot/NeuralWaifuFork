# -*-coding: utf-8 -*-
"""
This is main file with import
of all necessary libraries and functions.
You need run this file to run project.
"""

from configparser import ConfigParser
from openai import OpenAI
from PyQt6.QtWidgets import QMainWindow, QApplication
import random
import configparser
import webbrowser
import time
import sys

import core.configuration as conf
import core.gui as gui
import core.dialogue as dialogue
import core.audio_detection as audio_detection
import core.audio_speaking as audio_speaking


class MainWindow(QMainWindow, gui.Ui_MainWindow):
    def __init__(self, client, dialog, mod):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.dialog = dialog
        self.mod = mod
        self.pushButton.clicked.connect(self.button_clicked)
        self.pushButton.setCheckable(True)

    def button_clicked(self):
        print("Clicked!")
        entered_message = self.lineEdit.text()
        if entered_message.strip() != '':
            self.listWidget.addItem(entered_message)
            print(f"Entered message: {entered_message}")
            self.lineEdit.setText('')
            time.sleep(random.randint(10, 30) / 1000)
            if self.mod == "base":
                self.listWidget.addItem(
                    dialogue.generate_response(
                        self.dialog, entered_message,
                        self.mod,
                        self.client
                    )
                )
            elif self.mod == "free":
                self.listWidget.addItem(
                    dialogue.generate_response(
                        dialogue_history=self.dialog,
                        message=entered_message,
                        mod=self.mod
                    )
                )
            print(self.dialog)


def main():
    start: float = time.time()

    # read data from the configuration file
    conf_ini: ConfigParser = configparser.ConfigParser()
    conf_ini.read("configuration.ini")
    api_key: str = conf_ini['DEFAULT']['Api_key']

    # initializing an OpenAI client
    client: OpenAI = OpenAI(
        api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
        base_url="https://api.proxyapi.ru/openai/v1"
    )

    # list for storing dialog history
    dialogue_history: list = []

    # checking the OpenAI client for correctness
    mod: str = "base"
    print(dialogue.generate_response(
        dialogue_history,
        "Кто ты?",
        mod,
        client
    ))

    # if the api key doesn't work, use the free model
    if dialogue.generate_response(
            dialogue_history,
            "Кто ты?",
            mod,
            client
    ) is None:
        mod = "free"
    else:
        mod = dialogue.get_mod()

    # creating an application
    app: QApplication = QApplication(sys.argv)

    # creating MainWindow
    window: MainWindow = MainWindow(
        client=client,
        dialog=dialogue_history,
        mod=mod
    )
    window.show()

    # fix the browser path
    webbrowser.register(
        conf.BASE_BROWSER,
        None,
        webbrowser.BackgroundBrowser(conf.CHROME_PATH)
    )

    # output debugging information
    print(
        f"{conf.VA_NAME} (v{conf.VA_VERSION}) начал свою работу ...\n"
        f"Api key: {api_key}\n"
        f"OpenAI client: {client}\n"
        f"Mod = {mod}\n"
        f"Время на запуск: {(time.time() - start):.2f} секунд"
    )

    # starting the event loop
    app.exec()

    # starting the voice assistant
    audio_speaking.va_speak(
        random.choice(conf.GREETING_LIST)
    )  # greeting at startup
    audio_detection.va_listen(
        dialogue.va_respond,
        client,
        dialogue_history,
        mod
    )  # start listening to commands


if __name__ == "__main__":
    main()
