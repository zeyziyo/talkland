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
        
        # 서버 TTS URL 설정
        # 개발: http://localhost:5000
        # 배포: https://your-app.fly.dev
        import os
        self.server_url = os.getenv('TTS_SERVER_URL', 'http://localhost:5000')
        
        print(f"[WebSpeechBackend] TTS Server URL: {self.server_url}")
        print("[WebSpeechBackend] Initialization complete")
    
    # ===========================================
    # STT
    # ===========================================

    def start_stt(self, on_silence=None, lang: str = "ko-KR") -> None:
        """음성 인식 시작 (간소화 모드)"""
        print(f"[WebSpeechBackend] STT requested for lang: {lang}")
        print("[WebSpeechBackend] Note: Direct browser Web Speech API access required")
        self._result = None
        self._on_silence = on_silence

    def stop_stt(self) -> Optional[str]:
        """음성 인식 종료 및 결과 반환"""
        print("[WebSpeechBackend] STT stop requested")
        # 웹 모드에서는 브라우저가 직접 처리해야 함
        return self._result or "웹 모드: 브라우저 콘솔 확인 필요"

    # ===========================================
    # TTS
    # ===========================================

    def speak(self, text: str, slow: bool = False, lang: str = "ko-KR", voice: str = None) -> None:
        """
        서버 TTS API로 음성 출력
        
        Args:
            text: 음성으로 변환할 텍스트
            slow: 느리게 말하기 (rate 조정)
            lang: 언어 코드 (예: 'ko', 'ja', 'es')
            voice: 음성 코드 (예: 'ko-KR-Neural2-C')
        """
        print(f"[WebSpeechBackend] Server TTS requested: '{text}' in {lang}")
        
        # 음성 코드 매핑 (간단한 버전)
        if not voice:
            voice_map = {
                "ko": "ko-KR-SunHiNeural",
                "en": "en-US-JennyNeural",
                "es": "es-ES-AlvaroNeural",
                "ja": "ja-JP-NanamiNeural",
                "zh": "zh-CN-XiaoxiaoNeural",
                "fr": "fr-FR-DeniseNeural",
                "de": "de-DE-KatjaNeural",
            }
            voice = voice_map.get(lang, "en-US-JennyNeural")
        
        rate = "-20%" if slow else "+0%"
        
        # JavaScript로 서버 TTS 호출
        js_code = f"""
        (async function() {{
            try {{
                console.log('[WebSpeechBackend] Calling server TTS...');
                
                const response = await fetch('{self.server_url}/api/tts', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        text: {text!r},
                        voice: '{voice}',
                        rate: '{rate}'
                        // volume: '100%', // Optional
                        // pitch: '0Hz' // Optional
                    }})
                }});
                
                if (!response.ok) {{
                    throw new Error('Server TTS failed: ' + response.status);
                }}
                
                const blob = await response.blob();
                const audioUrl = URL.createObjectURL(blob);
                const audio = new Audio(audioUrl);
                
                audio.onended = () => {{
                    URL.revokeObjectURL(audioUrl);
                    console.log('[WebSpeechBackend] TTS playback complete');
                }};
                
                audio.play();
                console.log('[WebSpeechBackend] Playing server TTS');
                
            }} catch (error) {{
                console.error('[WebSpeechBackend] Server TTS error:', error);
                
                // 폴백: 브라우저 기본 TTS
                console.log('[WebSpeechBackend] Falling back to browser TTS');
                const utter = new SpeechSynthesisUtterance({text!r});
                utter.lang = '{lang}-{lang.upper()}';
                utter.rate = {0.7 if slow else 1.0};
                speechSynthesis.speak(utter);
            }}
        }})();
        """
        
        try:
            # JavaScript 실행 시도
            if hasattr(self.page, 'run_js'):
                self.page.run_js(js_code)
            else:
                print("[WebSpeechBackend] page.run_js not available, cannot execute TTS")
        except Exception as e:
            print(f"[WebSpeechBackend] JavaScript execution error: {e}")

    # =========================
    # 내부 이벤트 핸들러
    # =========================

    def _on_stt_result(self, e: Any) -> None:
        """JS에서 전달된 STT 결과 처리"""
        self._result = e.data.get("text", "")