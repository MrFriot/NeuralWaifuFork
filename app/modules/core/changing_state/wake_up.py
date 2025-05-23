# Импорт библиотек
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Импорт модулей
from app.modules.core.logic.config import BASE_VOLUME


def wake_up():
    # Инициализация
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    # Корректировка громкости
    volume.SetMasterVolumeLevelScalar(BASE_VOLUME, None)
