import flet as ft
import inspect

try:
    if hasattr(ft, "AudioRecorder"):
        print(f"Start Sig: {inspect.signature(ft.AudioRecorder.start_recording)}")
except Exception as e:
    print(f"Error: {e}")
