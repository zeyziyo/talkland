import flet as ft
try:
    print(f"Flet Version: {ft.version}")
except:
    print("No ft.version")

print(f"Has AudioRecorder: {hasattr(ft, 'AudioRecorder')}")

try:
    import flet_audio_recorder
    print("flet_audio_recorder package: FOUND")
except ImportError:
    print("flet_audio_recorder package: NOT_FOUND")
