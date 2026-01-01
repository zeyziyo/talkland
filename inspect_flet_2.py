import flet as ft
import inspect

try:
    if hasattr(ft, "AudioRecorder"):
        sig = inspect.signature(ft.AudioRecorder.__init__)
        print(f"Init Sig: {sig}")
        
        start_sig = inspect.signature(ft.AudioRecorder.start_recording)
        print(f"Start Sig: {start_sig}")
        
        # Check if on_state_changed is a property
        ar = ft.AudioRecorder()
        print(f"Has on_state_changed: {hasattr(ar, 'on_state_changed')}")
        
    else:
        print("ft.AudioRecorder not found")

except Exception as e:
    print(f"Error: {e}")
