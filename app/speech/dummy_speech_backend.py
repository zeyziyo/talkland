# app/speech/dummy_speech_backend.py

"""
DummySpeechBackend

Android 네이티브 앱에서 사용하는 더미 백엔드
실제 음성 기능은 제공하지 않지만, 에러 없이 작동함
"""

from typing import Optional
from .speech_backend import SpeechBackend


class DummySpeechBackend(SpeechBackend):
    """
    음성 기능을 제공하지 않는 더미 백엔드
    Android 네이티브 앱에서 사용
    """

    def __init__(self):
        """초기화"""
        print("[DummySpeechBackend] Initialized (no speech features)")

    # =========================
    # STT
    # =========================

    def start_stt(self, *args, **kwargs):
        """음성 인식 시작 (더미 - 아무것도 하지 않음)"""
        print("Dummy start_stt called. Backend is inactive.")

    def stop_stt(self) -> str:
        """음성 인식 종료 (더미 - 빈 문자열 반환)"""
        msg = "음성 인식 기능이 비활성화되었습니다."
        if self.init_error:
            msg += f"\n(초기화 오류: {self.init_error})"
        return msg

    # =========================
    # TTS
    # =========================

    def speak(self, text: str, slow: bool = False) -> None:
        """텍스트를 음성으로 출력 (더미 - 아무것도 하지 않음)"""
        print(f"Dummy speak: {text}")
```
