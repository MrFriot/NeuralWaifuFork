# config: utf-8

from fuzzywuzzy import fuzz
import vosk
import sys
import sounddevice
import queue
import json
import logging
import time
import torch

import core.configuration as config

# speech recognition model
model: vosk.Model = vosk.Model("./core/model/")
samplerate = 16000

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# microphone listening function
def va_listen(callback, client, dialog, mod):
    with sounddevice.RawInputStream(
            samplerate=samplerate,
            blocksize=8000,
            device=config.DEVICE,
            dtype="int16",
            channels=1,
            callback=q_callback
    ) as stream:
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # suspend the microphone listening while the assistant is responding
                stream.stop()
                callback(
                    json.loads(rec.Result())["text"],
                    client,
                    dialog,
                    mod
                )
                # Resume listening to the microphone
                stream.start()


# function for recognizing the assistant's name in a speech segment
def va_wake_word_recognition(word: str) -> bool:
    for name in config.VA_WAKE_WORD_LIST:
        detection_probability = fuzz.ratio(name, word)
        if detection_probability > config.NAME_PERCENT_DETECTION:
            print(f"Модель распознала свое имя с вероятностью {detection_probability}%")
            return True
    return False


# function for trimming speech to a meaningful segment
def va_wake_word_detection(message: str) -> str:
    separated_message: list[str] = message.split()
    for i in range(len(separated_message)):
        if va_wake_word_recognition(separated_message[i]):
            ask = ''
            for word in separated_message[i + 1:]:
                ask += f"{word} "
            print(f"Модель распознала следующее обращение: {ask}")
            return ask
    return ''

logger = logging.getLogger(__name__)


class TTS:
    def __init__(self,
                 device: str = "cpu",
                 sample_rate: int = 48000,
                 speaker: str = "aidar") -> None:
        self.device = torch.device(device)
        self.sample_rate = sample_rate
        self.speaker = speaker
        try:
            self.model, _ = torch.hub.load(
                repo_or_dir="snakers4/silero-models",
                model="silero_tts",
                language="ru",
                speaker="ru_v3"
            )
            self.model.to(self.device)
            logger.info("Silero TTS model loaded successfully.")
        except Exception as e:
            logger.exception("Failed to load Silero TTS model.")
            raise RuntimeError("TTS initialization failed.") from e

    def va_speak(self, text: str, speaker: str = "aidar") -> None:
        if not text.strip():
            logger.warning("Empty text provided to TTS.")
            return
        try:
            audio = self.model.apply_tts(
                text=f"{text}..",
                speaker=speaker or self.speaker,
                sample_rate=self.sample_rate,
                put_accent=True,
                put_yo=True
            )
            logger.debug(f"Generated audio for: {text}")
        except Exception as e:
            logger.exception("TTS synthesis failed.")
            return
        try:
            duration = len(audio) / self.sample_rate
            sounddevice.play(audio, int(self.sample_rate * 1.05))
            time.sleep(duration + 0.5)
            logger.info("Audio playback completed.")
        except KeyboardInterrupt:
            logger.info("Playback interrupted by user.")
        except Exception as e:
            logger.exception("Audio playback failed.")
        finally:
            sounddevice.stop()
