import flet as ft
import inspect

try:
    print("ft.AudioRecorder exists:", hasattr(ft, "AudioRecorder"))
    if hasattr(ft, "AudioRecorder"):
        print("AudioRecorder init sig:", inspect.signature(ft.AudioRecorder.__init__))
        print("AudioRecorder.start_recording sig:", inspect.signature(ft.AudioRecorder.start_recording))
    
    print("ft.AudioEncoder exists:", hasattr(ft, "AudioEncoder"))
    if hasattr(ft, "AudioEncoder"):
        print("AudioEncoder members:", dir(ft.AudioEncoder))

except Exception as e:
    print(e)
