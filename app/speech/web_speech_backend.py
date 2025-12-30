"""
WebSpeechBackend (INTENTIONALLY UNSAFE IMPLEMENTATION)

이 모듈은 Web / Android (Flet Mobile) 환경 전용이다.

중요한 설계 결정:
- Flet Web/Android의 Page 객체는 런타임에
  JavaScript 브릿지 메서드를 동적으로 주입한다.
- run_js, on_event 는 공식 Python 타입 정의에 존재하지 않는다.
- 따라서 이 모듈은 타입 안정성을 의도적으로 포기한다.

규칙:
- Any, getattr 사용은 "버그"가 아니라 "설계"이다.
- mypy / pylance 경고는 무시 대상이다.
- Desktop 환경에서 import 금지.
"""

# app/speech/web_speech_backend.py

from typing import Any, Optional
from .speech_backend import SpeechBackend

class WebSpeechBackend(SpeechBackend):
    """
    Web / Android용 STT / TTS backend

    - Web Speech API 사용 (JS)
    - Flet JS 브릿지를 통해 통신
    - 타입 안정성보다 런타임 안정성 우선
    """

    def __init__(self, page: Any):
        """
        page: Flet Page (JS 브릿지 포함)
        """
        print("[WebSpeechBackend] Initializing...")
        self.page: Any = page
        self._result: Optional[str] = None
        self._on_silence = None

        try:
            # JS → Python 이벤트 수신
            print("[WebSpeechBackend] Setting up event listener...")
            on_event_func = getattr(self.page, "on_event", None)
            if on_event_func is None:
                raise AttributeError("page.on_event not available")
            
            on_event_func("stt-result", self._on_stt_result)
            print("[WebSpeechBackend] Event listener registered successfully")

            # JS 로드 (인라인 방식으로 변경 - Android 호환성)
            print("[WebSpeechBackend] Loading inline JavaScript...")
            js_code = """
let recognition = null;

// =========================
// STT
// =========================
function startSTT(lang = 'ko-KR') {
    console.log('[WebSpeech] Starting STT with lang:', lang);
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        console.log('[WebSpeech] Speech recognition not supported');
        flet.sendEvent("stt-result", { text: "" });
        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    recognition = new SpeechRecognition();
    recognition.lang = lang;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        console.log('[WebSpeech] STT result:', text);
        flet.sendEvent("stt-result", { text });
    };

    recognition.onerror = (error) => {
        console.log('[WebSpeech] STT error:', error);
        flet.sendEvent("stt-result", { text: "" });
    };

    recognition.start();
    console.log('[WebSpeech] STT started');
}

function stopSTT() {
    console.log('[WebSpeech] Stopping STT');
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
}

// =========================
// TTS
// =========================
function speak(text, slow = false, lang = 'ko-KR') {
    console.log('[WebSpeech] Speaking:', text, 'lang:', lang);
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = lang;
    utter.rate = slow ? 0.7 : 1.0;
    speechSynthesis.speak(utter);
}

console.log('[WebSpeech] JavaScript loaded successfully');
"""
            run_js_func = getattr(self.page, "run_js", None)
            if run_js_func is None:
                raise AttributeError("page.run_js not available")
            
            run_js_func(js_code)
            print("[WebSpeechBackend] JavaScript loaded successfully")
            
        except Exception as e:
            print(f"[WebSpeechBackend] Initialization error: {e}")
            import traceback
            traceback.print_exc()
            raise

    # =========================
    # STT
    # =========================

    def start_stt(self, on_silence=None, lang: str = "ko-KR") -> None:
        """음성 인식 시작 (JS)
        
        Args:
            on_silence: Callback for silence detection (not implemented in web)
            lang: Language code for STT (e.g., 'ko-KR', 'en-US')
        """
        self._result = None
        self._on_silence = on_silence
        # Pass language to JS
        getattr(self.page, "run_js")(f"startSTT('{lang}');")

    def stop_stt(self) -> Optional[str]:
        """음성 인식 종료 및 결과 반환"""
        getattr(self.page, "run_js")("stopSTT();")
        return self._result

    # =========================
    # TTS
    # =========================

    def speak(self, text: str, slow: bool = False, lang: str = "ko-KR") -> None:
        """텍스트를 음성으로 출력 (JS)
        
        Args:
            text: Text to speak
            slow: Whether to speak slowly
            lang: Language code for TTS (e.g., 'ko-KR', 'es-ES')
        """
        slow_js = "true" if slow else "false"
        getattr(self.page, "run_js")(
            f"speak({text!r}, {slow_js}, '{lang}');"
        )

    # =========================
    # 내부 이벤트 핸들러
    # =========================

    def _on_stt_result(self, e: Any) -> None:
        """JS에서 전달된 STT 결과 처리"""
        self._result = e.data.get("text", "")