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

## 4. pyproject.toml Configuration (CRITICAL)

Flet 0.80.0에서는 `flet.yaml` 대신 `pyproject.toml`을 사용하여 설정합니다.

```toml
[project]
name = "your-app"
version = "0.1.0"
dependencies = [
    "flet>=0.80.0",
    "flet-audio-recorder>=0.80.0",
]

[tool.setuptools.packages.find]
# 앱 패키지만 포함, knowledge_base 등 제외
include = ["app*"]

[tool.flet]
platforms = ["android"]

[tool.flet.android]
permissions = ["android.permission.RECORD_AUDIO", "android.permission.INTERNET"]

# Flutter 의존성 (CRITICAL - 이것이 없으면 "Unknown control" 오류 발생)
[tool.flet.flutter.dependencies]
flet_audio_recorder = ""
```

## 5. Troubleshooting

| 오류 메시지 | 원인 및 해결책 |
|------------|---------------|
| **"Unknown control AudioRecorder"** | `[tool.flet.flutter.dependencies]`에 `flet_audio_recorder` 누락 |
| **'NoneType' object has no attribute 'stop_recording'** | 초기화 실패. `try-except`로 감싸고 권한 실패 처리 |
| **setuptools "Multiple top-level packages"** | `[tool.setuptools.packages.find]`에 `include = ["app*"]` 추가 |

### Lazy Initialization 권장
앱 시작 시 바로 `AudioRecorder`를 초기화하면 오류가 발생할 수 있습니다.
**녹음 시작 시점에 지연 초기화**하는 것을 권장합니다:

```python
def _ensure_recorder_initialized(self):
    if self._recorder_initialized:
        return self.audio_recorder is not None
    self._recorder_initialized = True
    try:
        self.audio_recorder = far.AudioRecorder(...)
        self.page.overlay.append(self.audio_recorder)
        return True
    except Exception as e:
        self.init_error = e
        return False
```

## 6. Build Command

> **⚠️ 주의**: Flet 0.80.0에서 `--include-packages` 플래그는 **더 이상 지원되지 않습니다**.
> Flutter 의존성은 반드시 `pyproject.toml`의 `[tool.flet.flutter.dependencies]`에서 지정해야 합니다.

```bash
# 올바른 명령어 (Flet 0.80.0+)
flet build apk --verbose

# 더 이상 지원되지 않음 ❌
# flet build apk --include-packages flet_audio_recorder
```
