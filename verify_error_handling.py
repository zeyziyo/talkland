import flet as ft
from unittest.mock import MagicMock
import sys
import os

# Add local path to sys.path
sys.path.append(os.getcwd())

try:
    from app.speech.android_speech_backend import AndroidSpeechBackend
    
    def test_error_handling():
        print("Test 1: Normal Initialization")
        # Reuse verify_fix logic briefly
        page = MagicMock()
        page.platform = "android"
        page.overlay = []
        page.update = MagicMock()
        
        backend = AndroidSpeechBackend(page) # Should work unless mocked heavily (ft.AudioRecorder needs running event loop or mocks)
        # Assuming verify_fix passed before, this relies on ft being available. 
        # But if ft.AudioRecorder fails without a page loop, we might see the error handling here.
        
        print(f"Backend 1 Recorder: {backend.audio_recorder}")
        if backend.audio_recorder is None:
             print(f"Init Error Caught: {backend.init_error}")
        
        print("\nTest 2: Forced Failure Initialization")
        # We can simulate failure by patching ft.AudioRecorder to raise
        original_ar = ft.AudioRecorder
        ft.AudioRecorder = MagicMock(side_effect=Exception("Simulated Init Failure"))
        
        backend_fail = AndroidSpeechBackend(page)
        print(f"Backend 2 Recorder: {backend_fail.audio_recorder}")
        print(f"Backend 2 Init Error: {backend_fail.init_error}")
        
        print("Testing start_stt on failed backend:")
        backend_fail.start_stt() # Should not crash
        
        print("Testing stop_stt on failed backend:")
        result = backend_fail.stop_stt()
        print(f"Result: {result}")
        if "Simulated Init Failure" in result:
             print("[PASS] Error propagated correctly")
        else:
             print("[FAIL] Error message mismatch")

        # Restore
        ft.AudioRecorder = original_ar

    test_error_handling()

except ImportError as ie:
    print(f"Import failed: {ie}")
