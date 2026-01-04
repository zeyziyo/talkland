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
        print("[Factory] CRITICAL: Could not import DummySpeechBackend")
        class DummySpeechBackend(SpeechBackend): # Inline fallback
            def start_stt(self, *args, **kwargs): pass
            def stop_stt(self) -> str: return "Critical Error: Dummy Backend Missing"
            def speak(self, *args, **kwargs): pass

    # 3. Detect Platform
    is_web = False
    
    # Debugging: Print all relevant properties
    print(f"[Factory DEBUG] sys.platform: {sys.platform}")
    if page:
        print(f"[Factory DEBUG] page.web: {getattr(page, 'web', 'N/A')}")
        print(f"[Factory DEBUG] page.platform: {getattr(page, 'platform', 'N/A')}")
    
    # Check 1: Flet page.web property (Most reliable for PWA)
    if hasattr(page, 'web') and page.web:
        is_web = True
    # Check 2: Pyodide sys.platform
    elif sys.platform == "emscripten":
        is_web = True
        
    print(f"[Factory] Platform Detection - Web: {is_web}")

    # 4. Return Backend
    try:
        if is_web:
            # Plan C: Use AndroidSpeechBackend for Web (It handles Blob URLs)
            print("[Factory] Using AndroidSpeechBackend for Web (PWA Mode)")
            from .android_speech_backend import AndroidSpeechBackend
            return AndroidSpeechBackend(page)
            
        elif platform_info and ("android" in platform_info.lower() or "ios" in platform_info.lower()):
            # Mobile
            print(f"[Factory] Using AndroidSpeechBackend for Mobile ({platform_info})")
            from .android_speech_backend import AndroidSpeechBackend
            return AndroidSpeechBackend(page)
            
        else:
            # Desktop
            print("[Factory] Using DesktopSpeechBackend")
            from .desktop_speech_backend import DesktopSpeechBackend
            return DesktopSpeechBackend()
            
    except Exception as e:
        print(f"[Factory] Backend initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return DummySpeechBackend()

