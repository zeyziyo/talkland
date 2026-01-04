import flet as ft
from app.text.translate import translate
from app.speech.speech_backend_factory import create_speech_backend
from app.ui.mode1 import Mode1Section
from app.ui.mode2 import Mode2Section

SOURCE_LANG = "ko"
TARGET_LANG = "es"

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
        # 공통 UI
        # -----------------
        title = ft.Text("TalkLand", size=28, weight=ft.FontWeight.BOLD)
    
        mode_selector = ft.SegmentedButton(
            selected=["translate"],
            segments=[
                ft.Segment(value="translate", label=ft.Text("MODE 1 · 의미 학습")),
                ft.Segment(value="practice", label=ft.Text("MODE 2 · 발음 훈련")),
            ],
        )
    
        # -----------------
        # MODE 1 & 2 UI (Refactored)
        # -----------------
        mode1_section = Mode1Section(page, speech_backend, SOURCE_LANG, TARGET_LANG)
        mode2_section = Mode2Section(page)
        

    
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
            title,
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
# Mobile/Web: ft.app is required.
# To run as Web: flet run main.py --web
ft.app(target=main)
