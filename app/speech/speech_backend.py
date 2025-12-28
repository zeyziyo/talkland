# app/speech/speech_backend.py
"""
SpeechBackend 인터페이스 정의

이 모듈은:
- STT / TTS의 '계약(contract)'만 정의한다.
- 어떤 플랫폼에서도 안전하게 import 가능해야 한다.
- 실제 구현은 포함하지 않는다.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class SpeechBackend(ABC):
    """
    STT / TTS 기능을 추상화한 인터페이스.

    UI 계층은 이 클래스만 의존하며,
    실제 구현은 플랫폼별로 분리된다.
    """

    @abstractmethod
    def start_stt(self) -> None:
        """
        음성 인식을 시작한다.

        - Desktop: 마이크 녹음 시작
        - Mobile(Web): SpeechRecognition.start()
        """
        raise NotImplementedError

    @abstractmethod
    def stop_stt(self) -> Optional[str]:
        """
        음성 인식을 종료하고 인식된 텍스트를 반환한다.

        반환값:
        - 성공 시: 인식된 문자열
        - 실패 / 취소 시: None
        """
        raise NotImplementedError

    @abstractmethod
    def speak(self, text: str, slow: bool = False) -> None:
        """
        주어진 텍스트를 음성으로 출력한다.

        매개변수:
        - text: 읽을 문장
        - slow: 느린 발음 여부
        """
        raise NotImplementedError
