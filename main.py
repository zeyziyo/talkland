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

    # -----------------
    # 공통 상태
    # -----------------
    mode: str = "translate"  # translate | practice
    speech_backend = create_speech_backend(page)

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
    def on_mode_change(e: ft.Event) -> None:
        nonlocal mode
        mode = next(iter(mode_selector.selected))

        mode1_section.visible = mode == "translate"
        mode2_section.visible = mode == "practice"

        page.update()

    mode_selector.on_change = on_mode_change

    # -----------------
    # 레이아웃
    # -----------------
    page.add(
        title,
        ft.Divider(),
        mode_selector,
        ft.Divider(),
        mode1_section,
        mode2_section,
    )

ft.run(main)
