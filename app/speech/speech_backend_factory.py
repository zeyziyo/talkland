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
    
    print(f"[Factory] Creating backend for platform: {page.platform}, sys.platform: {sys.platform}")

    # Web (Pyodide only) - uses JavaScript Web Speech API
    if is_web_runtime():
        print("[Factory] Using WebSpeechBackend for web platform")
        return WebSpeechBackend(page)
    
    # Android/iOS - use dummy backend
    # Normalize platform string (page.platform is an Enum in Flet, e.g. PagePlatform.ANDROID)
    platform_val = str(page.platform).lower() if page.platform else ""
    # The Enum string might be "PagePlatform.ANDROID" or just "android" depending on version/context.
    # Checking if it contains "android" or "ios" is safer.
    
    if "android" in platform_val or "ios" in platform_val:
        print(f"[Factory] Using DummySpeechBackend for {page.platform}")
        from .dummy_speech_backend import DummySpeechBackend
        return DummySpeechBackend()

    # Desktop - import only when needed to avoid loading sounddevice on mobile
    print("[Factory] Using DesktopSpeechBackend for desktop")
    from .desktop_speech_backend import DesktopSpeechBackend
    return DesktopSpeechBackend()

