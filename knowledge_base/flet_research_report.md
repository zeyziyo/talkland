# [ARCHIVED] Flet 0.80.0 & Android Build Research Report
> **⚠️ NOTE**: This document is historical. For the latest build rules and Flet 0.80.1 configuration, please refer to **[Flet Android Guide](flet_android_guide.md)**.


## 1. Overview: The 0.80.0 Paradigm Shift (개요: 0.80.0의 패러다임 전환)
Based on the documentation ([Creating a new Flet app](https://docs.flet.dev/getting-started/create-flet-app/)), Flet 0.80.0 (codenamed "Flet 1.0 Beta") represents a fundamental architectural change.

(문서([Creating a new Flet app](https://docs.flet.dev/getting-started/create-flet-app/))에 따르면, Flet 0.80.0 ("Flet 1.0 Beta")은 근본적인 아키텍처 변화를 의미합니다.)

- **Old World (Pre-0.80)**: Monolithic. `flet` package contained everything. `AudioRecorder` was built-in.

  (**이전 (0.80 미만)**: 모놀리식 구조. `flet` 패키지에 모든 것이 포함됨. `AudioRecorder`가 내장되어 있었음.)

- **New World (0.80+)**: Modular. The core `flet` package is lean. 
Features like Audio, Video, and Maps are now **Extensions** (separate packages).

  (**현재 (0.80 이상)**: 모듈식 구조. 핵심 `flet` 패키지는 가벼워짐. 오디오, 비디오, 지도 같은 기능은 이제 **확장(Extensions)**(별도 패키지)이 됨.)

## 2. Audio Recorder Status (오디오 녹음기 현황)
The [flet-audio-recorder PyPI page](https://pypi.org/project/flet-audio-recorder/) and [User Extensions guide](https://docs.flet.dev/extend/user-extensions/) confirm:

([flet-audio-recorder PyPI 페이지](https://pypi.org/project/flet-audio-recorder/)와 [사용자 확장 가이드](https://docs.flet.dev/extend/user-extensions/)에서 확인한 내용:)

- **It is an Extension**: It wraps a 3rd-party Flutter package (`record`).
  (**확장 기능임**: 제3자 Flutter 패키지인 `record`를 래핑함.)

- **Version Gap**: The PyPI version is `0.1.0` (ancient), while Flet core is `0.80.0`. This explains why `pip install flet-audio-recorder` fails to satisfy the `0.80.0` requirement when versions strictly check.

  (**버전 격차**: PyPI 버전은 `0.1.0`(구버전)인 반면, Flet 코어는 `0.80.0`임. 이는 버전이 엄격히 체크될 때 `pip install`이 실패하는 이유를 설명함.)

- **Implication**: While using Git source fixes the version gap, documentation says "Built-in extensions" should strictly adhere to `dependencies` list without manual configs.

  (**시사점**: Git 소스를 사용하면 버전 차이를 해결할 수 있지만, 문서는 "내장 확장"의 경우 수동 설정 없이 `dependencies` 목록만 따를 것을 명시함.)

## 3. Android Build Mechanics (안드로이드 빌드 메커니즘)
The [Packaging app for Android guide](https://docs.flet.dev/publish/android/) highlights three critical components:

([안드로이드 앱 패키징 가이드](https://docs.flet.dev/publish/android/)는 세 가지 핵심 요소를 강조함:)

### A. Prerequisites & SDK (전제 조건 및 SDK)
- The build process relies on a **Template** (`flet-build-template`).
  (빌드 프로세스는 **템플릿**(`flet-build-template`)에 의존함.)

- The CLI automatically fetches this template. **Crucially**, the CLI attempts to match the template version to the installed Flet version.

  (CLI는 자동으로 이 템플릿을 가져옴. **중요한 점은**, CLI가 설치된 Flet 버전과 일치하는 템플릿 버전을 찾으려 시도한다는 것임.)

### B. Binary Python Packages (바이너리 파이썬 패키지)
- "Non-pure" packages (like those containing C/Rust or Flutter wrappers) require special handling.

  ("비순수" 패키지(C/Rust 또는 Flutter 래퍼 포함)는 특별한 처리가 필요함.)

- `flet-audio-recorder` falls into this category because it essentially injects native Android code (Java/Kotlin) via the Flutter plugin system.

  (`flet-audio-recorder`는 Flutter 플러그인 시스템을 통해 네이티브 안드로이드 코드(Java/Kotlin)를 주입하므로 이 범주에 속함.)

## 4. Analysis of "Template Not Found" Error ("템플릿을 찾을 수 없음" 오류 분석)
Combining findings from `flet build apk --help` and the `publish/android` doc:

(`flet build apk --help`와 `publish/android` 문서의 내용을 종합하면:)

- **The Bug**: `flet` CLI 0.80.0 appears to default to seeking a `0.81.0` template (likely anticipating the next nightly build).

  (**버그**: `flet` CLI 0.80.0은 기본적으로 `0.81.0` 템플릿을 찾으려 하는 것으로 보임(다음 나이틀리 빌드를 예상하는 듯함).)

- **The Evidence**: The error explicitly states `ref "0.81.0" ... could not found`.

  (**증거**: 오류 메시지에 `ref "0.81.0" ... could not found`라고 명시됨.)

- **The Docs Solution**: The build command accepts `--template-ref {version}`. This is the documented override switch provided precisely for situations where the default template inference fails (e.g., CI/CD environments or version mismatches).

  (**문서상 해결책**: 빌드 명령어는 `--template-ref {version}`을 허용함. 이는 기본 템플릿 추론이 실패하는 상황(CI/CD 환경이나 버전 불일치 등)을 위해 제공되는 문서화된 재정의 스위치임.)

## 5. Conclusion & Recommendation (결론 및 권장 사항)
The documentation confirms that our direction is correct, but we missed one tool instantiation parameter.

(문서는 우리의 방향이 맞다는 것을 확인해주었지만, 도구 실행 매개변수 하나를 놓쳤음.)

1.  **Dependency**: Using Git for `flet-audio-recorder` is correct (Standard Extension pattern). -> **UPDATE**: User requested strict adherence to docs (using PyPI).

    (**의존성**: `flet-audio-recorder`에 Git을 사용하는 것이 맞음(표준 확장 패턴). -> **업데이트**: 사용자가 문서 엄수(PyPI 사용)를 요청함.)

2.  **Configuration**: `pyproject.toml` is the authoritative source (Standard Build pattern).

    (**구성**: `pyproject.toml`이 권한 있는 소스임(표준 빌드 패턴).)

3.  **The Missing Piece**: We trusted the CLI's default template selection logic, which is flawed in this Beta release.

    (**놓친 부분**: 이번 베타 릴리스에서 결함이 있는 CLI의 기본 템플릿 선택 로직을 신뢰했음.)

**Action Item (조치 항목):**
We must explicitly tell the build system which template version to use, overriding its faulty default.

(우리는 빌드 시스템에 어떤 템플릿 버전을 사용할지 명시적으로 알려주어, 결함 있는 기본값을 재정의해야 함.)

> **Command**: `flet build apk --template-ref 0.80.0`

This aligns with the [Advanced Build Configuration](https://docs.flet.dev/publish/android/#flet-build-apk) documentation.

(이는 [고급 빌드 구성](https://docs.flet.dev/publish/android/#flet-build-apk) 문서와 일치함.)
