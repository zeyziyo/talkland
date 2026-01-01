# Flet Android Deployment Guide

## 1. Version Compatibility (CRITICAL)
As of late 2024 (Flet 0.80.0+):
- **Core Library**: `flet` package no longer contains everything.
- **Audio Recording**: `AudioRecorder` control was moved from `flet` core to **`flet-audio-recorder`** package.
- **Documentation**: Always check [PyPI](https://pypi.org/project/flet/) for the real latest version. Do not trust local old versions.

**Requirements:**
```txt
flet>=0.80.0
flet-audio-recorder>=0.80.0
```

## 2. Entry Point
For Android (and iOS) packaging, you **must** use `ft.app` instead of `ft.run`.
`ft.run` is for desktop debugging and may cause "White Screen" issues or immediate crashes on mobile devices.

```python
# Correct for Mobile
import flet as ft

def main(page: ft.Page):
    ...

ft.app(target=main)
```

## 3. Audio Recorder Implementation
Since Flet 0.80.0, usage has changed significantly.

### Correct Import
```python
import flet_audio_recorder as far
# NOT: from flet import AudioRecorder (Deprecated/Removed)
```

### Initialization
Note `on_state_change` (no 'd') and strict `configuration` object.

```python
self.audio_recorder = far.AudioRecorder(
    configuration=far.AudioRecorderConfiguration(
        encoder=far.AudioEncoder.WAV
    ),
    on_state_change=self._on_state_changed
)
```

### Starting Recording
```python
# Must provide output path
self.audio_recorder.start_recording(self.output_filename)
```

## 4. Permissions & Config (flet.yaml)
Ensure `flet.yaml` contains necessary permissions and dependencies.

```yaml
permissions:
  - RECORD_AUDIO
  - INTERNET

dependencies:
  # Must specify recent version to get AudioRecorder support (via external lib)
  flet: ">=0.80.0"
  flet-audio-recorder: ">=0.80.0"
```

## 5. Troubleshooting
- **'NoneType' object has no attribute 'stop_recording'**: Initialization failed silently. Always wrap `AudioRecorder` init in `try-except` and handle permission failures gracefully.

## 6. Build Command (CRITICAL)
For external packages like `flet-audio-recorder` to work on Android, you **must** include them in the build command:
```bash
flet build apk --include-packages flet_audio_recorder
```
Without this flag, the Python code will run but the Android client will not know about the `AudioRecorder` control, resulting in "Unknown control" errors.
