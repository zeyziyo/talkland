"""
DesktopSpeechBackend 단독 테스트 스크립트

- UI 없이 STT / TTS가 실제로 동작하는지 검증
- main.py 완성 전에 반드시 통과해야 함
"""

import time
from app.speech.desktop_speech_backend import DesktopSpeechBackend


def main() -> None:
    print("🔊 TTS 테스트 시작")
    backend = DesktopSpeechBackend()

    backend.speak("This is a desktop TTS test.", slow=False)
    time.sleep(2)

    print("🎤 STT 테스트 시작 (5초간 말하세요)")
    backend.start_stt()
    time.sleep(5)
    result = backend.stop_stt()

    print("📝 인식 결과:", result)


if __name__ == "__main__":
    main()
