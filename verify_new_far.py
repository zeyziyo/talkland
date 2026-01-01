import flet as ft
import flet_audio_recorder as far # Must import this
from unittest.mock import MagicMock
import sys
import os

# Add local path to sys.path
sys.path.append(os.getcwd())

try:
    from app.speech.android_speech_backend import AndroidSpeechBackend
    
    def test_new_impl():
        print("Testing AndroidSpeechBackend with flet-audio-recorder...")
        page = MagicMock()
        page.platform = "android"
        page.overlay = []
        page.update = MagicMock()
        
        # We need to make sure AudioRecorder can be instantiated even if invalid arg types are passed to Mock?
        # Actually since we have logic in code, we just run it.
        # But flet.audio_recorder might need Page context? 
        # Usually controls are fine to init.
        
        backend = AndroidSpeechBackend(page)
        
        if backend.audio_recorder:
             print(f"Recorder created: {type(backend.audio_recorder)}")
             print(f"Config: {backend.audio_recorder.configuration}")
             # Check if it was added to overlay
             if backend.audio_recorder in page.overlay:
                 print("Added to overlay: OK")
             else:
                 print("Added to overlay: FAIL")
        else:
             print(f"Init Failed: {backend.init_error}")
             
    test_new_impl()

except Exception as e:
    print(f"Test Error: {e}")
    import traceback
    traceback.print_exc()
