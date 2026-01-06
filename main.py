import flet as ft
from app.text.translate import translate
from app.speech.speech_backend_factory import create_speech_backend
from app.ui.mode1 import Mode1Section
from app.ui.mode2 import Mode2Section
from app.settings_manager import SettingsManager
from app.ui.settings_dialog import SettingsDialog

def main(page: ft.Page) -> None:
    page.title = "TalkLand"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40  # Safe area for Android status bar

    # -----------------
    # 초기 로딩 UI (White Screen 방지)
    # -----------------
    loading_text = ft.Text("로딩 중...", size=20, color=ft.Colors.BLUE)
    page.add(loading_text)
    page.update()
    print("UI: Loading screen displayed")

    try:
        # -----------------
        # 공통 상태
        # -----------------
        mode: str = "translate"  # translate | practice
        
        # Debug log display (Android debugging)
        debug_log = ft.Text("", size=10, color=ft.Colors.GREY_700, selectable=True)
        debug_logs = []
        
        def add_log(message: str):
            """Add a log message to the debug display"""
            print(message)  # Also print to console
            debug_logs.append(message)
            if len(debug_logs) > 10:  # Keep only last 10 logs
                debug_logs.pop(0)
            debug_log.value = "\n".join(debug_logs)
            try:
                # Only update if the control is attached to a page
                if debug_log.page:
                    debug_log.update()
            except Exception:
                pass
        
        # Speech backend 초기화 (에러 처리 추가)
        try:
            add_log(f"Platform: {page.platform}")
            add_log("Initializing speech backend...")
            speech_backend = create_speech_backend(page)
            add_log(f"[OK] Backend: {type(speech_backend).__name__}")
        except Exception as e:
            add_log(f"[ERR] Init failed: {e}")
            import traceback
            error_details = traceback.format_exc()
            # Show first line of traceback
            add_log(error_details.split('\n')[0] if error_details else "Unknown error")
            # 음성 기능 없이도 앱이 실행되도록 더미 백엔드 사용
            from app.speech.dummy_speech_backend import DummySpeechBackend
            speech_backend = DummySpeechBackend()
    
        # -----------------
        # 설정 관리자 초기화
        # -----------------
        settings_manager = SettingsManager(page)
        add_log(f"Settings loaded: {settings_manager.get_source_lang()} -> {settings_manager.get_target_lang()}")
        
        # -----------------
        # 공통 UI
        # -----------------
        title = ft.Text("TalkLand", size=28, weight=ft.FontWeight.BOLD)
        
        # 설정 버튼
        settings_button = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            tooltip="설정",
            on_click=lambda e: show_settings_dialog()
        )
    
        mode_selector = ft.SegmentedButton(
            selected=["translate"],
            segments=[
                ft.Segment(value="translate", label=ft.Text("의미 학습")),
                ft.Segment(value="practice", label=ft.Text("발음 훈련")),
            ],
        )
    
        # -----------------
        # MODE 1 & 2 UI (Refactored)
        # -----------------
        mode1_section = Mode1Section(
            page, 
            speech_backend, 
            settings_manager.get_source_lang(), 
            settings_manager.get_target_lang()
        )
        mode2_section = Mode2Section(page)
        
        # 설정 변경 시 호출될 콜백 함수
        def on_settings_saved(new_settings):
            """설정이 저장되었을 때 Mode1/Mode2 업데이트"""
            add_log(f"Settings updated: {new_settings['source_lang']} -> {new_settings['target_lang']}")
            
            # Mode1 업데이트
            mode1_section.source_lang = new_settings['source_lang']
            mode1_section.target_lang = new_settings['target_lang']
            mode1_section.source_voice = new_settings.get('source_voice')
            mode1_section.target_voice = new_settings.get('target_voice')
            
            add_log("Modes updated with new settings")
        
        # 설정 다이얼로그
        def show_settings_dialog():
            dialog = SettingsDialog(
                page=page,
                settings_manager=settings_manager,
                on_save=on_settings_saved
            )
            dialog.show()
        

    
        # -----------------
        # MODE 전환 로직
        # -----------------
        def on_mode_change(e: ft.ControlEvent) -> None:
            nonlocal mode
            mode = next(iter(mode_selector.selected))
    
            mode1_section.visible = mode == "translate"
            mode2_section.visible = mode == "practice"
    
            page.update()
    
        mode_selector.on_change = on_mode_change
    
        # -----------------
        # 레이아웃 구성 (로딩 텍스트 제거 후 추가)
        # -----------------
        page.controls.clear() # 기존 로딩 텍스트 제거
        page.add(
            # 헤더 (타이틀 + 설정 버튼)
            ft.Row(
                controls=[
                    title,
                    settings_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            debug_log,  # Debug log display
            ft.Divider(),
            mode_selector,
            ft.Divider(),
            mode1_section,
            mode2_section,
        )
        page.update()
        
    except Exception as ie:
        # 치명적 초기화 오류 발생 시 화면에 표시
        print(f"Critical Startup Error: {ie}")
        import traceback
        traceback.print_exc()
        page.controls.clear()
        page.add(
             ft.Text("앱 초기화 중 오류가 발생했습니다.", color=ft.Colors.RED, size=20),
             ft.Text(f"Error: {ie}", color=ft.Colors.RED),
             ft.Text(traceback.format_exc(), size=10)
        )
        page.update()

# Flet 0.80.1 Entry Point
# To run as Web: set WEB_MODE=true, then python main.py
# To run as Desktop: python main.py (default)
import os
WEB_MODE = os.getenv("WEB_MODE", "false").lower() == "true"

if WEB_MODE:
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8570)
else:
    ft.app(target=main)
