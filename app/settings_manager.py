# app/settings_manager.py
"""
설정 관리 모듈

사용자 설정을 로컬 스토리지에 저장하고 불러오는 기능을 제공합니다.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
import flet as ft
from .settings_config import DEFAULT_SETTINGS, SUPPORTED_LANGUAGES, get_default_voice_for_lang

class SettingsManager:
    """설정 저장/로드 관리 클래스"""
    
    STORAGE_KEY = "talkland_settings"
    
    def __init__(self, page: ft.Page):
        """
        Args:
            page: Flet Page 객체 (호환성 유지)
        """
        self.page = page
        self._settings: Dict[str, Any] = {}
        
        # 설정 파일 경로 (사용자 홈 디렉토리)
        self.settings_dir = Path.home() / ".talkland"
        self.settings_file = self.settings_dir / "settings.json"
        
        # 디렉토리 생성
        self.settings_dir.mkdir(parents=True, exist_ok=True)
        
        self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """
        저장된 설정을 불러옵니다.
        
        Returns:
            설정 딕셔너리
        """
        try:
            # JSON 파일에서 설정 읽기
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self._settings = json.load(f)
                print(f"[Settings] Loaded from file: {self._settings}")
            else:
                # 저장된 설정이 없으면 기본값 사용
                self._settings = DEFAULT_SETTINGS.copy()
                print(f"[Settings] Using defaults: {self._settings}")
                # 기본값을 파일로 저장
                self.save_settings(self._settings)
        except Exception as e:
            print(f"[Settings] Load error: {e}, using defaults")
            self._settings = DEFAULT_SETTINGS.copy()
        
        # 설정 검증 및 보정
        self._validate_settings()
        
        return self._settings
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """
        설정을 저장합니다.
        
        Args:
            settings: 저장할 설정 딕셔너리
            
        Returns:
            성공 여부
        """
        try:
            # 설정 검증
            if not self._validate_settings_dict(settings):
                print("[Settings] Invalid settings, not saving")
                return False
            
            # JSON 파일로 저장
            self._settings = settings.copy()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, ensure_ascii=False, indent=2)
            print(f"[Settings] Saved to {self.settings_file}: {self._settings}")
            return True
        except Exception as e:
            print(f"[Settings] Save error: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        특정 설정값 가져오기
        
        Args:
            key: 설정 키
            default: 기본값
            
        Returns:
            설정값
        """
        return self._settings.get(key, default)
    
    def get_all_settings(self) -> Dict[str, Any]:
        """모든 설정 가져오기"""
        return self._settings.copy()
    
    def update_setting(self, key: str, value: Any) -> bool:
        """
        특정 설정값 업데이트 및 저장
        
        Args:
            key: 설정 키
            value: 새 값
            
        Returns:
            성공 여부
        """
        self._settings[key] = value
        return self.save_settings(self._settings)
    
    def reset_to_defaults(self) -> bool:
        """설정을 기본값으로 초기화"""
        return self.save_settings(DEFAULT_SETTINGS.copy())
    
    def _validate_settings(self):
        """현재 설정 검증 및 보정"""
        # 필수 키 확인
        for key in ["source_lang", "source_voice", "target_lang", "target_voice"]:
            if key not in self._settings:
                self._settings[key] = DEFAULT_SETTINGS[key]
        
        # 언어 코드 검증
        if self._settings["source_lang"] not in SUPPORTED_LANGUAGES:
            self._settings["source_lang"] = DEFAULT_SETTINGS["source_lang"]
            self._settings["source_voice"] = DEFAULT_SETTINGS["source_voice"]
        
        if self._settings["target_lang"] not in SUPPORTED_LANGUAGES:
            self._settings["target_lang"] = DEFAULT_SETTINGS["target_lang"]
            self._settings["target_voice"] = DEFAULT_SETTINGS["target_voice"]
        
        # 음성 코드 검증
        if not self._is_valid_voice(self._settings["source_lang"], self._settings["source_voice"]):
            self._settings["source_voice"] = get_default_voice_for_lang(self._settings["source_lang"])
        
        if not self._is_valid_voice(self._settings["target_lang"], self._settings["target_voice"]):
            self._settings["target_voice"] = get_default_voice_for_lang(self._settings["target_lang"])
    
    def _validate_settings_dict(self, settings: Dict[str, Any]) -> bool:
        """설정 딕셔너리 검증"""
        # 필수 키 확인
        required_keys = ["source_lang", "source_voice", "target_lang", "target_voice"]
        for key in required_keys:
            if key not in settings:
                return False
        
        # 언어 코드 검증
        if settings["source_lang"] not in SUPPORTED_LANGUAGES:
            return False
        if settings["target_lang"] not in SUPPORTED_LANGUAGES:
            return False
        
        return True
    
    def _is_valid_voice(self, lang_code: str, voice_code: str) -> bool:
        """음성 코드가 해당 언어에 유효한지 확인"""
        lang_config = SUPPORTED_LANGUAGES.get(lang_code)
        if not lang_config:
            return False
        
        for voice in lang_config["voices"]:
            if voice["code"] == voice_code:
                return True
        
        return False
    
    # ===========================================
    # 편의 메서드
    # ===========================================
    
    def get_source_lang(self) -> str:
        """모국어 코드"""
        return self._settings.get("source_lang", "ko")
    
    def get_target_lang(self) -> str:
        """대상 언어 코드"""
        return self._settings.get("target_lang", "es")
    
    def get_source_voice(self) -> str:
        """모국어 음성 코드"""
        return self._settings.get("source_voice", "ko-KR-Neural2-C")
    
    def get_target_voice(self) -> str:
        """대상 언어 음성 코드"""
        return self._settings.get("target_voice", "es-ES-Neural2-A")
    
    def get_source_locale(self) -> str:
        """모국어 로케일 (예: ko-KR)"""
        lang_code = self.get_source_lang()
        return SUPPORTED_LANGUAGES.get(lang_code, {}).get("locale", lang_code)
    
    def get_target_locale(self) -> str:
        """대상 언어 로케일 (예: es-ES)"""
        lang_code = self.get_target_lang()
        return SUPPORTED_LANGUAGES.get(lang_code, {}).get("locale", lang_code)
