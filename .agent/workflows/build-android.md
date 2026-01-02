---
description: Android APK 빌드 워크플로우
---
// turbo-all

# Android APK 빌드

## 1. 코드 문법 검사
```bash
python -m py_compile main.py
```

## 2. 앱 모듈 임포트 검사
```bash
python -c "import app; print('✅ App module OK')"
```

## 3. Android APK 빌드
```bash
flet build apk --verbose
```

Dependencies and permissions are now configured in `pyproject.toml`.
- Flutter dependencies: `[tool.flet.flutter.dependencies]`
- Permissions: `[tool.flet.android]`
```

## 4. 빌드 결과 확인
```bash
dir build\apk
```
