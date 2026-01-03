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
    
    # 1. Platform Detection
    platform_info = "UNKNOWN"
    try:
        if page and hasattr(page, 'platform'):
            platform_info = str(page.platform)
    except:
        pass
        
    print(f"[Factory] Creating backend. Page Platform: {platform_info}, Sys Platform: {sys.platform}")

    # 2. Prepare Dummy Backend (Safe Fallback)
    try:
        from .dummy_speech_backend import DummySpeechBackend
    except ImportError:
        # Should not happen, but as a last resort define inline or fail
        print("[Factory] CRITICAL: Could not import DummySpeechBackend")
        class DummySpeechBackend(SpeechBackend): # Inline fallback
            def start_stt(self, *args, **kwargs): pass
            def stop_stt(self) -> str: return "Critical Error: Dummy Backend Missing"
            def speak(self, *args, **kwargs): pass

    # 3. Web / Pyodide
    if is_web_runtime():
        print("[Factory] Environment: Web/Pyodide")
        try:
            from .web_speech_backend import WebSpeechBackend
            return WebSpeechBackend(page)
        except Exception as e:
            print(f"[Factory] Failed to load WebSpeechBackend: {e}")
            return DummySpeechBackend()

    # 4. Android / iOS (Mobile)
    # Check "android" or "ios" in the platform string case-insensitively
    is_mobile = False
    if platform_info:
        p = platform_info.lower()
        if "android" in p or "ios" in p:
            is_mobile = True
    
    if is_mobile:
        print(f"[Factory] Environment: Mobile ({platform_info})")
        try:
            # Try to import Android backend
            # This might fail if dependencies (like sounddevice if wrongly imported) are missing
            print("[Factory] Attempting to import AndroidSpeechBackend...")
            from .android_speech_backend import AndroidSpeechBackend
            return AndroidSpeechBackend(page)
        except Exception as e:
            print(f"[Factory] Failed to load AndroidSpeechBackend: {e}")
            import traceback
            traceback.print_exc()
            print("[Factory] Fallback to DummySpeechBackend")
            return DummySpeechBackend()

    # 5. Desktop (Windows/Mac/Linux)
    print("[Factory] Environment: Desktop")
    try:
        print("[Factory] Attempting to import DesktopSpeechBackend...")
        from .desktop_speech_backend import DesktopSpeechBackend
        return DesktopSpeechBackend()
    except Exception as e:
        print(f"[Factory] Failed to load DesktopSpeechBackend: {e}")
        import traceback
        traceback.print_exc()
        return DummySpeechBackend()

