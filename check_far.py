import flet_audio_recorder as far
import inspect

print("AudioRecorder found:", hasattr(far, "AudioRecorder"))
if hasattr(far, "AudioRecorder"):
    print("Init sig:", inspect.signature(far.AudioRecorder.__init__))
    print("Start sig:", inspect.signature(far.AudioRecorder.start_recording))
