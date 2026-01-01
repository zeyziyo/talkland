import flet_audio_recorder as far
import inspect

print("on_state_change:", hasattr(far.AudioRecorder, 'on_state_change'))
print("on_state_changed:", hasattr(far.AudioRecorder, 'on_state_changed'))

# Inspect init again to be sure if it accepts kwargs or specific args
print("Init full:", inspect.signature(far.AudioRecorder.__init__))
