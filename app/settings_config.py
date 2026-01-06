# app/settings_config.py
"""
언어 및 음성 설정 구성 모듈

지원 언어, 음성 옵션, 기본 설정값을 정의합니다.
"""

from typing import Dict, List, TypedDict

class VoiceOption(TypedDict):
    """음성 옵션 타입"""
    name: str          # 표시 이름 (예: "Neural2-A (여성)")
    code: str          # 음성 코드 (예: "ko-KR-Neural2-A")
    gender: str        # 성별 (male/female)
    quality: str       # 품질 (standard/wavenet/neural2)

class LanguageConfig(TypedDict):
    """언어 설정 타입"""
    name: str          # 표시 이름 (예: "한국어")
    code: str          # 언어 코드 (예: "ko")
    locale: str        # 로케일 코드 (예: "ko-KR")
    voices: List[VoiceOption]

# ===========================================
# 지원 언어 목록
# ===========================================

SUPPORTED_LANGUAGES: Dict[str, LanguageConfig] = {
    "ko": {
        "name": "한국어",
        "code": "ko",
        "locale": "ko-KR",
        "voices": [
            # Standard Voices
            {"name": "Standard-A (여성)", "code": "ko-KR-Standard-A", "gender": "female", "quality": "standard"},
            {"name": "Standard-B (여성)", "code": "ko-KR-Standard-B", "gender": "female", "quality": "standard"},
            {"name": "Standard-C (남성)", "code": "ko-KR-Standard-C", "gender": "male", "quality": "standard"},
            {"name": "Standard-D (남성)", "code": "ko-KR-Standard-D", "gender": "male", "quality": "standard"},
            # WaveNet Voices
            {"name": "Wavenet-A (여성)", "code": "ko-KR-Wavenet-A", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-B (여성)", "code": "ko-KR-Wavenet-B", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-C (남성)", "code": "ko-KR-Wavenet-C", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-D (남성)", "code": "ko-KR-Wavenet-D", "gender": "male", "quality": "wavenet"},
            # Neural2 Voices (최고 품질)
            {"name": "Neural2-A (여성)", "code": "ko-KR-Neural2-A", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-B (여성)", "code": "ko-KR-Neural2-B", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-C (남성)", "code": "ko-KR-Neural2-C", "gender": "male", "quality": "neural2"},
        ]
    },
    "en": {
        "name": "English",
        "code": "en",
        "locale": "en-US",
        "voices": [
            # Standard Voices
            {"name": "Standard-A (Female)", "code": "en-US-Standard-A", "gender": "female", "quality": "standard"},
            {"name": "Standard-B (Male)", "code": "en-US-Standard-B", "gender": "male", "quality": "standard"},
            {"name": "Standard-C (Female)", "code": "en-US-Standard-C", "gender": "female", "quality": "standard"},
            {"name": "Standard-D (Male)", "code": "en-US-Standard-D", "gender": "male", "quality": "standard"},
            # WaveNet Voices
            {"name": "Wavenet-A (Female)", "code": "en-US-Wavenet-A", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-B (Male)", "code": "en-US-Wavenet-B", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-C (Female)", "code": "en-US-Wavenet-C", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-D (Male)", "code": "en-US-Wavenet-D", "gender": "male", "quality": "wavenet"},
            # Neural2 Voices
            {"name": "Neural2-A (Female)", "code": "en-US-Neural2-A", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-C (Female)", "code": "en-US-Neural2-C", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-D (Male)", "code": "en-US-Neural2-D", "gender": "male", "quality": "neural2"},
        ]
    },
    "es": {
        "name": "Español",
        "code": "es",
        "locale": "es-ES",
        "voices": [
            # Standard Voices
            {"name": "Standard-A (Mujer)", "code": "es-ES-Standard-A", "gender": "female", "quality": "standard"},
            {"name": "Standard-B (Hombre)", "code": "es-ES-Standard-B", "gender": "male", "quality": "standard"},
            {"name": "Standard-C (Mujer)", "code": "es-ES-Standard-C", "gender": "female", "quality": "standard"},
            {"name": "Standard-D (Mujer)", "code": "es-ES-Standard-D", "gender": "female", "quality": "standard"},
            # WaveNet Voices
            {"name": "Wavenet-A (Mujer)", "code": "es-ES-Wavenet-A", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-B (Hombre)", "code": "es-ES-Wavenet-B", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-C (Mujer)", "code": "es-ES-Wavenet-C", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-D (Mujer)", "code": "es-ES-Wavenet-D", "gender": "female", "quality": "wavenet"},
            # Neural2 Voices
            {"name": "Neural2-A (Mujer)", "code": "es-ES-Neural2-A", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-B (Hombre)", "code": "es-ES-Neural2-B", "gender": "male", "quality": "neural2"},
            {"name": "Neural2-C (Mujer)", "code": "es-ES-Neural2-C", "gender": "female", "quality": "neural2"},
        ]
    },
    "ja": {
        "name": "日本語",
        "code": "ja",
        "locale": "ja-JP",
        "voices": [
            # Standard Voices
            {"name": "Standard-A (女性)", "code": "ja-JP-Standard-A", "gender": "female", "quality": "standard"},
            {"name": "Standard-B (女性)", "code": "ja-JP-Standard-B", "gender": "female", "quality": "standard"},
            {"name": "Standard-C (男性)", "code": "ja-JP-Standard-C", "gender": "male", "quality": "standard"},
            {"name": "Standard-D (男性)", "code": "ja-JP-Standard-D", "gender": "male", "quality": "standard"},
            # WaveNet Voices
            {"name": "Wavenet-A (女性)", "code": "ja-JP-Wavenet-A", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-B (女性)", "code": "ja-JP-Wavenet-B", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-C (男性)", "code": "ja-JP-Wavenet-C", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-D (男性)", "code": "ja-JP-Wavenet-D", "gender": "male", "quality": "wavenet"},
            # Neural2 Voices
            {"name": "Neural2-B (女性)", "code": "ja-JP-Neural2-B", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-C (男性)", "code": "ja-JP-Neural2-C", "gender": "male", "quality": "neural2"},
            {"name": "Neural2-D (男性)", "code": "ja-JP-Neural2-D", "gender": "male", "quality": "neural2"},
        ]
    },
    "zh": {
        "name": "中文",
        "code": "zh-CN",
        "locale": "zh-CN",
        "voices": [
            # Standard Voices
            {"name": "Standard-A (女性)", "code": "cmn-CN-Standard-A", "gender": "female", "quality": "standard"},
            {"name": "Standard-B (男性)", "code": "cmn-CN-Standard-B", "gender": "male", "quality": "standard"},
            {"name": "Standard-C (男性)", "code": "cmn-CN-Standard-C", "gender": "male", "quality": "standard"},
            {"name": "Standard-D (女性)", "code": "cmn-CN-Standard-D", "gender": "female", "quality": "standard"},
            # WaveNet Voices
            {"name": "Wavenet-A (女性)", "code": "cmn-CN-Wavenet-A", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-B (男性)", "code": "cmn-CN-Wavenet-B", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-C (男性)", "code": "cmn-CN-Wavenet-C", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-D (女性)", "code": "cmn-CN-Wavenet-D", "gender": "female", "quality": "wavenet"},
        ]
    },
    "fr": {
        "name": "Français",
        "code": "fr",
        "locale": "fr-FR",
        "voices": [
            # Standard Voices
            {"name": "Standard-A (Femme)", "code": "fr-FR-Standard-A", "gender": "female", "quality": "standard"},
            {"name": "Standard-B (Homme)", "code": "fr-FR-Standard-B", "gender": "male", "quality": "standard"},
            {"name": "Standard-C (Femme)", "code": "fr-FR-Standard-C", "gender": "female", "quality": "standard"},
            {"name": "Standard-D (Homme)", "code": "fr-FR-Standard-D", "gender": "male", "quality": "standard"},
            # WaveNet Voices
            {"name": "Wavenet-A (Femme)", "code": "fr-FR-Wavenet-A", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-B (Homme)", "code": "fr-FR-Wavenet-B", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-C (Femme)", "code": "fr-FR-Wavenet-C", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-D (Homme)", "code": "fr-FR-Wavenet-D", "gender": "male", "quality": "wavenet"},
            # Neural2 Voices
            {"name": "Neural2-A (Femme)", "code": "fr-FR-Neural2-A", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-B (Homme)", "code": "fr-FR-Neural2-B", "gender": "male", "quality": "neural2"},
        ]
    },
    "de": {
        "name": "Deutsch",
        "code": "de",
        "locale": "de-DE",
        "voices": [
            # Standard Voices
            {"name": "Standard-A (Weiblich)", "code": "de-DE-Standard-A", "gender": "female", "quality": "standard"},
            {"name": "Standard-B (Männlich)", "code": "de-DE-Standard-B", "gender": "male", "quality": "standard"},
            {"name": "Standard-C (Weiblich)", "code": "de-DE-Standard-C", "gender": "female", "quality": "standard"},
            {"name": "Standard-D (Männlich)", "code": "de-DE-Standard-D", "gender": "male", "quality": "standard"},
            # WaveNet Voices
            {"name": "Wavenet-A (Weiblich)", "code": "de-DE-Wavenet-A", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-B (Männlich)", "code": "de-DE-Wavenet-B", "gender": "male", "quality": "wavenet"},
            {"name": "Wavenet-C (Weiblich)", "code": "de-DE-Wavenet-C", "gender": "female", "quality": "wavenet"},
            {"name": "Wavenet-D (Männlich)", "code": "de-DE-Wavenet-D", "gender": "male", "quality": "wavenet"},
            # Neural2 Voices
            {"name": "Neural2-A (Weiblich)", "code": "de-DE-Neural2-A", "gender": "female", "quality": "neural2"},
            {"name": "Neural2-B (Männlich)", "code": "de-DE-Neural2-B", "gender": "male", "quality": "neural2"},
        ]
    }
}

# ===========================================
# 기본 설정값
# ===========================================

DEFAULT_SETTINGS = {
    "source_lang": "ko",
    "source_voice": "ko-KR-Neural2-C",  # 기본: 한국어 남성 Neural2
    "target_lang": "es",
    "target_voice": "es-ES-Neural2-A",  # 기본: 스페인어 여성 Neural2
}

# ===========================================
# 유틸리티 함수
# ===========================================

def get_language_display_name(lang_code: str) -> str:
    """언어 코드로 표시 이름 가져오기"""
    return SUPPORTED_LANGUAGES.get(lang_code, {}).get("name", lang_code)

def get_voice_display_name(voice_code: str) -> str:
    """음성 코드로 표시 이름 가져오기"""
    for lang_config in SUPPORTED_LANGUAGES.values():
        for voice in lang_config["voices"]:
            if voice["code"] == voice_code:
                return voice["name"]
    return voice_code

def get_locale_from_lang_code(lang_code: str) -> str:
    """언어 코드로 로케일 가져오기 (예: ko → ko-KR)"""
    return SUPPORTED_LANGUAGES.get(lang_code, {}).get("locale", lang_code)

def get_default_voice_for_lang(lang_code: str) -> str:
    """언어의 기본 음성 가져오기 (Neural2 우선)"""
    lang_config = SUPPORTED_LANGUAGES.get(lang_code)
    if not lang_config:
        return ""
    
    # Neural2 음성 우선 선택
    for voice in lang_config["voices"]:
        if voice["quality"] == "neural2":
            return voice["code"]
    
    # Neural2 없으면 첫 번째 음성
    if lang_config["voices"]:
        return lang_config["voices"][0]["code"]
    
    return ""
