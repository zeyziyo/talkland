import flet as ft
from unittest.mock import MagicMock
import sys
import os

# Add local path to sys.path
sys.path.append(os.getcwd())

try:
    from app.speech.android_speech_backend import AndroidSpeechBackend
    
    def test():
        print("Testing AndroidSpeechBackend initialization...")
        page = MagicMock()
        page.platform = "android"
        page.overlay = []
        page.update = MagicMock()
        
        try:
            backend = AndroidSpeechBackend(page)
            print("Backend initialized successfully")
            if backend.audio_recorder:
                print(f"AudioRecorder created: {backend.audio_recorder}")
                # Check properties
                print(f"on_state_changed set: {backend.audio_recorder.on_state_changed}")
                
                # Verify start_stt basic call (mocking verify)
                # We need to mock start_recording to avoid actual recording attempt which might fail on desktop without context or crash
                backend.audio_recorder.start_recording = MagicMock()
                backend.start_stt()
                print("start_stt called successfully")
                backend.audio_recorder.start_recording.assert_called()
                print("start_recording triggered successfully")
                
            else:
                print("AudioRecorder is None (Import failed or exception caught)")
                
        except TypeError as te:
            print(f"[FAIL] TypeError during init: {te}")
        except Exception as e:
            print(f"[FAIL] Other error: {e}")
            import traceback
            traceback.print_exc()

    test()

except ImportError as ie:
    print(f"Import failed: {ie}")
    print("Ensure you are running from project root.")
