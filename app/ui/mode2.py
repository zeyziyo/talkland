import flet as ft

def fake_stt_result() -> str:
    """임시 STT 결과"""
    return "안녕하세요"

class Mode2Section(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page  # Store page reference

        
        self.native_sentence = ft.Text(
            "나는 오늘 커피를 마시고 싶다.",
            size=16,
        )

        self.slot_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
        self.timer_text = ft.Text("")
        self.result_text = ft.Text("")

        self.start_btn = ft.ElevatedButton(content=ft.Text("START"), on_click=self.start_practice)
        self.stop_btn = ft.ElevatedButton(content=ft.Text("STOP")) # currently unused in main.py logic but present in UI

        self.controls = [
            self.native_sentence,
            ft.Container(
                content=self.slot_text,
                height=80,
                alignment=ft.alignment.center,
                border=ft.border.all(2),
                expand=True,
            ),
            self.timer_text,
            ft.Row(
                controls=[self.start_btn, self.stop_btn],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            self.result_text,
        ]
        self.visible = False
        self.spacing = 15

    def start_practice(self, e) -> None:
        self.slot_text.value = "🎰"
        self.timer_text.value = "발음 중..."
        self._page.update()

        spoken = fake_stt_result()
        self.slot_text.value = spoken
        self.result_text.value = "정확도: 80%"
        self._page.update()
