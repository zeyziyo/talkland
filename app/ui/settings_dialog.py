# app/ui/settings_dialog.py
"""
설정 다이얼로그 UI

언어 및 음성 설정을 변경할 수 있는 다이얼로그를 제공합니다.
"""

import flet as ft
from typing import Callable, Optional
from app.settings_config import SUPPORTED_LANGUAGES
from app.settings_manager import SettingsManager

class SettingsDialog:
    """설정 다이얼로그 클래스"""
    
    def __init__(
        self, 
        page: ft.Page, 
        settings_manager: SettingsManager,
        on_save: Optional[Callable] = None
    ):
        """
        Args:
            page: Flet Page 객체
            settings_manager: 설정 관리자
            on_save: 설정 저장 시 호출할 콜백 함수
        """
        self.page = page
        self.settings_manager = settings_manager
        self.on_save_callback = on_save
        
        # 현재 설정 가져오기
        current_settings = settings_manager.get_all_settings()
        
        # ===========================================
        # 언어 및 음성 선택 드롭다운
        # ===========================================
        
        # 모국어 선택
        self.source_lang_dropdown = ft.Dropdown(
            label="모국어",
            width=300,
            options=[
                ft.dropdown.Option(key=lang_code, text=lang_config["name"])
                for lang_code, lang_config in SUPPORTED_LANGUAGES.items()
            ],
            value=current_settings["source_lang"]
        )
        self.source_lang_dropdown.on_change = self._on_source_lang_change
        
        # 모국어 음성 선택
        self.source_voice_dropdown = ft.Dropdown(
            label="모국어 음성",
            width=300,
            value=current_settings["source_voice"]
        )
        self._update_source_voices(current_settings["source_lang"])
        
        # 대상 언어 선택
        self.target_lang_dropdown = ft.Dropdown(
            label="대상 언어",
            width=300,
            options=[
                ft.dropdown.Option(key=lang_code, text=lang_config["name"])
                for lang_code, lang_config in SUPPORTED_LANGUAGES.items()
            ],
            value=current_settings["target_lang"]
        )
        self.target_lang_dropdown.on_change = self._on_target_lang_change
        
        # 대상 언어 음성 선택
        self.target_voice_dropdown = ft.Dropdown(
            label="대상 언어 음성",
            width=300,
            value=current_settings["target_voice"]
        )
        self._update_target_voices(current_settings["target_lang"])
        
        # ===========================================
        # 버튼
        # ===========================================
        
        self.save_button = ft.ElevatedButton(
            content=ft.Text("저장"),
            icon=ft.Icons.SAVE,
            on_click=self._on_save_click
        )
        
        self.cancel_button = ft.TextButton(
            content=ft.Text("취소"),
            on_click=self._on_cancel_click
        )
        
        self.reset_button = ft.TextButton(
            content=ft.Text("기본값으로 초기화"),
            icon=ft.Icons.RESTORE,
            on_click=self._on_reset_click
        )
        
        # ===========================================
        # 다이얼로그 구성
        # ===========================================
        
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚙️ 설정"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # 모국어 섹션
                        ft.Text("📚 모국어 설정", size=16, weight=ft.FontWeight.BOLD),
                        self.source_lang_dropdown,
                        self.source_voice_dropdown,
                        ft.Divider(),
                        
                        # 대상 언어 섹션
                        ft.Text("🎯 대상 언어 설정", size=16, weight=ft.FontWeight.BOLD),
                        self.target_lang_dropdown,
                        self.target_voice_dropdown,
                        ft.Divider(),
                        
                        # 초기화 버튼
                        self.reset_button,
                    ],
                    spacing=10,
                    tight=True,
                ),
                width=400,
            ),
            actions=[
                self.cancel_button,
                self.save_button,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def show(self):
        """다이얼로그 표시"""
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def close(self):
        """다이얼로그 닫기"""
        self.dialog.open = False
        self.page.update()
    
    # ===========================================
    # 이벤트 핸들러
    # ===========================================
    
    def _on_source_lang_change(self, e):
        """모국어 변경 시 음성 목록 업데이트"""
        selected_lang = e.control.value
        self._update_source_voices(selected_lang)
        self.page.update()
    
    def _on_target_lang_change(self, e):
        """대상 언어 변경 시 음성 목록 업데이트"""
        selected_lang = e.control.value
        self._update_target_voices(selected_lang)
        self.page.update()
    
    def _update_source_voices(self, lang_code: str):
        """모국어 음성 드롭다운 업데이트"""
        lang_config = SUPPORTED_LANGUAGES.get(lang_code)
        if not lang_config:
            return
        
        self.source_voice_dropdown.options = [
            ft.dropdown.Option(key=voice["code"], text=voice["name"])
            for voice in lang_config["voices"]
        ]
        
        # 첫 번째 Neural2 음성을 기본으로 설정
        for voice in lang_config["voices"]:
            if voice["quality"] == "neural2":
                self.source_voice_dropdown.value = voice["code"]
                break
        else:
            # Neural2 없으면 첫 번째 음성
            if lang_config["voices"]:
                self.source_voice_dropdown.value = lang_config["voices"][0]["code"]
    
    def _update_target_voices(self, lang_code: str):
        """대상 언어 음성 드롭다운 업데이트"""
        lang_config = SUPPORTED_LANGUAGES.get(lang_code)
        if not lang_config:
            return
        
        self.target_voice_dropdown.options = [
            ft.dropdown.Option(key=voice["code"], text=voice["name"])
            for voice in lang_config["voices"]
        ]
        
        # 첫 번째 Neural2 음성을 기본으로 설정
        for voice in lang_config["voices"]:
            if voice["quality"] == "neural2":
                self.target_voice_dropdown.value = voice["code"]
                break
        else:
            # Neural2 없으면 첫 번째 음성
            if lang_config["voices"]:
                self.target_voice_dropdown.value = lang_config["voices"][0]["code"]
    
    def _on_save_click(self, e):
        """저장 버튼 클릭"""
        # 새 설정 생성
        new_settings = {
            "source_lang": self.source_lang_dropdown.value,
            "source_voice": self.source_voice_dropdown.value,
            "target_lang": self.target_lang_dropdown.value,
            "target_voice": self.target_voice_dropdown.value,
        }
        
        # 설정 저장
        if self.settings_manager.save_settings(new_settings):
            # 저장 성공 메시지
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("✅ 설정이 저장되었습니다."),
                bgcolor=ft.Colors.GREEN_700,
            )
            self.page.snack_bar.open = True
            
            # 콜백 호출
            if self.on_save_callback:
                self.on_save_callback(new_settings)
            
            # 다이얼로그 닫기
            self.close()
        else:
            # 저장 실패 메시지
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ 설정 저장에 실패했습니다."),
                bgcolor=ft.Colors.RED_700,
            )
            self.page.snack_bar.open = True
        
        self.page.update()
    
    def _on_cancel_click(self, e):
        """취소 버튼 클릭"""
        self.close()
    
    def _on_reset_click(self, e):
        """초기화 버튼 클릭"""
        # 확인 다이얼로그
        def confirm_reset(ce):
            confirm_dialog.open = False
            self.page.update()
            
            if ce.control.text == "확인":
                self.settings_manager.reset_to_defaults()
                
                # UI 업데이트
                default_settings = self.settings_manager.get_all_settings()
                self.source_lang_dropdown.value = default_settings["source_lang"]
                self.target_lang_dropdown.value = default_settings["target_lang"]
                self._update_source_voices(default_settings["source_lang"])
                self._update_target_voices(default_settings["target_lang"])
                self.source_voice_dropdown.value = default_settings["source_voice"]
                self.target_voice_dropdown.value = default_settings["target_voice"]
                
                # 알림
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("🔄 설정이 기본값으로 초기화되었습니다."),
                    bgcolor=ft.Colors.BLUE_700,
                )
                self.page.snack_bar.open = True
                self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("초기화 확인"),
            content=ft.Text("모든 설정을 기본값으로 초기화하시겠습니까?"),
            actions=[
                ft.TextButton(content=ft.Text("취소"), on_click=confirm_reset),
                ft.ElevatedButton(content=ft.Text("확인"), on_click=confirm_reset),
            ],
        )
        
        self.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        self.page.update()
