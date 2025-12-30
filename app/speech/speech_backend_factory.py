# app/speech/speech_backend_factory.py

"""
SpeechBackendFactory

- 실행 환경에 따라 적절한 SpeechBackend를 생성한다.
- UI 계층은 이 모듈만 사용한다.
"""

import sys
from typing import Any

from .speech_backend import SpeechBackend
from .web_speech_backend import WebSpeechBackend


def is_web_runtime() -> bool:
    """
    현재 실행 환경이 Web / Android인지 판별한다.

    True:
    - Pyodide
    - Flet Web
    - Flet Android

    False:
    - Windows / macOS / Linux (Desktop)
    """
    return sys.platform == "emscripten"


def create_speech_backend(page: Any) -> SpeechBackend:
    """
    실행 환경에 맞는 SpeechBackend 인스턴스를 반환한다.

    매개변수:
    - page: Flet Page (Web backend에서 필요)

    반환:
    - SpeechBackend 구현체
    """

    # Web (Pyodide) or Mobile (Android/iOS)
    # page.platform gives "android", "ios", "macos", "linux", "windows" or "web" (if generic)
    # sys.platform == "emscripten" covers Pyodide web.
    # We want WebSpeechBackend for Android/iOS as well.
    if is_web_runtime() or page.platform in ["android", "ios"]:
        return WebSpeechBackend(page)

    # Desktop - import only when needed to avoid loading sounddevice on mobile
    from .desktop_speech_backend import DesktopSpeechBackend
    return DesktopSpeechBackend()
