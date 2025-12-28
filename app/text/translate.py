# app/text/translate.py
"""
번역 로직 모듈 (MODE 1 전용)

이 모듈은:
- STT 결과 텍스트를 다른 언어로 번역한다.
- UI / Flet / SpeechBackend에 의존하지 않는다.
- Desktop / Web / Android 모두에서 import 안전하다.

초기 버전은 Mock 구현이며,
추후 Google / DeepL / OpenAI API로 교체 가능하다.
"""

from deep_translator import GoogleTranslator

def translate(text: str, src_lang: str, dst_lang: str) -> str:
    """
    입력 텍스트를 다른 언어로 번역한다. (Google Translate 사용)

    매개변수:
    - text: 번역할 원문
    - src_lang: 원본 언어 코드 (ex. "ko")
    - dst_lang: 대상 언어 코드 (ex. "en")

    반환값:
    - 번역된 문자열
    - 번역 불가 시 에러 메시지 반환
    """
    normalized = text.strip()
    if not normalized:
        return ""

    try:
        translated = GoogleTranslator(source=src_lang, target=dst_lang).translate(normalized)
        return translated
    except Exception as e:
        print(f"Translation Error: {e}")
        return f"번역 오류: {e}"
