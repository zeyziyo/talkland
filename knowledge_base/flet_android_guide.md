# Flet Android Deployment Guide

## 1. Version Compatibility (STABLE)
We are using **Flet 0.25.2 (Stable)** to ensure Android compatibility and proven stability.

**Requirements:**
```txt
flet==0.25.2
# AudioRecorder is built-in (flet core), no extra package needed.
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
In Flet 0.25.2, `AudioRecorder` is part of the `flet` core package.

### Initialization
```python
import flet as ft

# Direct initialization (Classic API)
self.audio_recorder = ft.AudioRecorder(
    audio_encoder=ft.AudioEncoder.WAV,
    on_state_changed=self._on_state_changed
)
```

### Starting Recording
```python
# Provide output path
self.audio_recorder.start_recording(self.output_filename)
```

## 4. pyproject.toml Configuration

Use `flet==0.25.2` and avoid external `flet-audio-recorder` dependencies.

```toml
[project]
name = "talkland"
version = "0.1.0"
dependencies = [
    "flet==0.25.2",
    # "flet-audio-recorder",  <-- REMOVE THIS
]

[tool.setuptools.packages.find]
include = ["app*"]

[tool.flet]
platforms = ["android"]

[tool.flet.android]
permissions = ["android.permission.RECORD_AUDIO", "android.permission.INTERNET"]
```

## 5. Troubleshooting

### Gradle Build Error (403 Forbidden)
GitHub Actions의 `ubuntu-latest` (v24.04) 러너에서 Maven Central 접근 시 403 오류가 발생할 수 있습니다.
**해결책**: `runs-on: ubuntu-22.04`로 변경하여 빌드 환경을 고정하세요.

| 오류 메시지 | 원인 및 해결책 |
|------------|---------------|
| **"Unknown control AudioRecorder"** | Flutter 플러그인 미등록. 위 `pyproject.toml`의 Git dependency 설정 필수. |
| **"Could not GET ... 403 Forbidden"** | GitHub Actions Runner 네트워크 문제. `ubuntu-22.04` 사용 권장. |
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

## 7. Mandatory Build Status Check
Whenever you modify the application or build settings, you **MUST** refer to `knowledge_base/build_config_reference.md`.
This file contains the "Gold Standard" configuration that is known to work. Always verify your:
1. `pyproject.toml`
2. `requirements.txt`
3. `.github/workflows/build-apk.yml`

against the reference document to prevent regression.

## 8. Android Runtime API Sensitivity (IMPORTANT)
The Android Flet runtime is stricter than Desktop. You **MUST** use the lowercase module paths for factory methods and instances, not the capitalized class names.

**Incorrect (Causes runtime crash on Android):**
```python
ft.Alignment.CENTER
ft.Border.all(2)
ft.Radius.all(10)
```

**Correct:**
```python
ft.alignment.center
ft.border.all(2)
ft.radius.all(10)
```

Always use lowercase `ft.border`, `ft.colors`, `ft.alignment` etc. when accessing helper functions or constants.
