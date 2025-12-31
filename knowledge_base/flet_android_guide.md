# Flet Android Deployment Guide

## 1. Entry Point
For Android (and iOS) packaging, you **must** use `ft.app` instead of `ft.run`.
`ft.run` is for desktop debugging and may cause "White Screen" issues or immediate crashes on mobile devices.

```python
# Correct for Mobile
import flet as ft

def main(page: ft.Page):
    ...

ft.app(target=main)
```

## 2. Permissions & Config
Ensure `flet.yaml` contains necessary permissions and dependencies.

### Audio Recording
If using `flet_audio_recorder`:
1. Add `flet-audio-recorder` to `dependencies` in `flet.yaml`.
2. Add `RECORD_AUDIO` to `permissions` in `flet.yaml`.
3. In code, use `tempfile.gettempdir()` to avoid permission errors when saving files.

```yaml
permissions:
  - RECORD_AUDIO

dependencies:
  flet: ">=0.80.0"
  flet-audio-recorder: ""
```

## 3. Build Command
Use the verbose flag to see detailed errors during GitHub Actions builds.
```bash
flet build apk --verbose
```
