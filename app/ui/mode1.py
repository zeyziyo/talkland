import threading
import flet as ft
from app.text.translate import translate

class Mode1Section(ft.Column):
    def __init__(self, page: ft.Page, speech_backend, source_lang="ko", target_lang="es"):
        super().__init__()
        # self.page = page  <-- REMOVED: Managed by Flet Control

        self.speech_backend = speech_backend
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        self.is_recording = False
        
        # UI Components
        # self.mode1_info = ft.Text("🎤 한국어로 말해보세요", size=18) # Removed per request
        self.mode1_result = ft.TextField(
            value="",
            hint_text="한국어로 말하거나 입력하세요",
            multiline=True,
            min_lines=1,
            max_lines=5,
            text_size=20,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            expand=True,
        )
        self.mode1_translated = ft.Text("", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        
        # Container wrapper to ensure alignment
        def wrap_icon(icon_btn):
            return ft.Container(content=icon_btn, width=60, alignment=ft.Alignment(0, 0))

        self.mode1_start_btn = ft.IconButton(
            icon=ft.Icons.MIC,
            icon_size=32,
            icon_color=ft.Colors.GREEN,
            tooltip="말하기 시작",
            on_click=self.run_mode1,
            visible=True,
        )
        
        self.mode1_stop_btn = ft.IconButton(
            icon=ft.Icons.STOP,
            icon_size=32,
            icon_color=ft.Colors.GREEN,
            tooltip="녹음 종료",
            on_click=self.stop_recording_and_transcribe,
            visible=False,
        )

        # Row for Mic Button + Input TextField
        self.input_row = ft.Row(
            controls=[
                # Wrap start/stop buttons in a container for fixed width alignment
                ft.Container(
                    content=ft.Stack([self.mode1_start_btn, self.mode1_stop_btn]),
                    width=60, # Fixed width for icon column
                    alignment=ft.Alignment(0, 0)
                ),
                self.mode1_result,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.mode1_translate_btn = ft.IconButton(
            icon=ft.Icons.G_TRANSLATE,
            icon_size=30,
            tooltip="스페인어로 번역하기",
            on_click=self.on_translate_click,
            visible=True,
            icon_color=ft.Colors.GREEN,
        )

        self.mode1_translated = ft.TextField(
            value="",
            hint_text="번역된 텍스트가 여기에 표시됩니다",
            multiline=True,
            min_lines=1,
            max_lines=5,
            text_size=20,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            read_only=True,
            expand=True,
        )
        
        # Row for Translate Button + TextField
        self.translation_row = ft.Row(
            controls=[
                wrap_icon(self.mode1_translate_btn),
                self.mode1_translated,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.mode1_tts_btn = ft.IconButton(
            icon=ft.Icons.VOLUME_UP,
            icon_size=32,
            icon_color=ft.Colors.GREEN,
            tooltip="스페인어 듣기",
            on_click=lambda _: self.speech_backend.speak(self.mode1_translated.value or "No text", lang=self.target_lang),
            disabled=False,
        )
        
        # Column setup
        self.controls = [
            self.input_row,
            self.translation_row, 
            wrap_icon(self.mode1_tts_btn) # Centered or aligned? If independent, just btn is fine, or wrap for consistency if needed.
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.visible = True
        self.spacing = 20

    def on_translate_click(self, e):
        if not self.mode1_result.value:
            return
        
        translated = translate(self.mode1_result.value, self.source_lang, self.target_lang)
        self.mode1_translated.value = translated
        self.mode1_translated.update()
        
        self.mode1_tts_btn.disabled = False
        self.mode1_tts_btn.update()

    def run_mode1(self, e=None):
        print(f"run_mode1 called. Current state: is_recording={self.is_recording}")
        
        try:
            if not self.is_recording:
                # 녹음 시작
                print("Starting recording...")
                self.is_recording = True
                
                # 버튼 교체
                self.mode1_start_btn.visible = False
                self.mode1_stop_btn.visible = True
                
                self.mode1_result.hint_text = "듣고 있습니다... (10초 무음 시 자동 종료)"
                # self.mode1_result.value = "듣고 있습니다... (10초 무음 시 자동 종료)"
                
                self.mode1_start_btn.update()
                self.mode1_stop_btn.update()
                self.mode1_result.update()
                self.page.update()
                
                self.speech_backend.start_stt(on_silence=self.on_silence_detected)
                print("Backend recording started.")
                
            else:
                self.stop_recording_and_transcribe()
                
        except Exception as ex:
            print(f"Error in run_mode1: {ex}")
            self.is_recording = False
            # self.mode1_start_btn.content = ft.Text("여기를 눌러 원하는 한국어를 말하세요") # N/A for IconButton
            self.mode1_start_btn.disabled = False
            # self.mode1_start_btn.style = None
            self.mode1_result.value = f"오류 발생: {ex}"
            self.mode1_start_btn.update()
            self.mode1_result.update()
            self.page.update()

    def stop_recording_and_transcribe(self, e=None):
        if not self.is_recording:
             return

        print("Stopping recording...")
        self.is_recording = False
        
        # self.mode1_start_btn.content = ft.Text("변환 중...") # N/A for IconButton
        self.mode1_start_btn.disabled = True
        # self.mode1_start_btn.style = None
        
        self.page.update()
        
        try:
             text = self.speech_backend.stop_stt()
             print(f"Transcribed text: {text}")
             
             if text:
                 self.mode1_result.value = text
             else:
                 self.mode1_result.hint_text = "음성을 인식하지 못했습니다. 다시 시도해주세요."
                 # self.mode1_result.value = "음성을 인식하지 못했습니다. 다시 시도해주세요."
        except Exception as ex:
             print(f"STT Error: {ex}")
             self.mode1_result.value = f"변환 오류: {ex}"
        
        self.mode1_result.hint_text = "한국어로 말하거나 입력하세요"

        self.mode1_stop_btn.visible = False
        self.mode1_start_btn.visible = True
        self.mode1_start_btn.disabled = False
        # self.mode1_start_btn.content = ft.Text("여기를 눌러 원하는 한국어를 말하세요") # N/A for IconButton
        
        self.mode1_stop_btn.update()
        self.mode1_start_btn.update()
        self.mode1_result.update()
        self.page.update()

    def on_silence_detected(self):
        print("Silence detected! Auto-stopping...")
        def stop_task():
            self.stop_recording_and_transcribe()
            
        threading.Thread(target=stop_task, daemon=True).start()
