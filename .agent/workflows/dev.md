---
description: 개발 워크플로우 - 로컬 실행 및 테스트
---
// turbo-all

# 개발 워크플로우

## 1. 로컬 앱 실행
```bash
flet run main.py
```

## 2. 코드 문법 검사 (Python)
```bash
python -m py_compile main.py
```

## 3. 앱 모듈 문법 검사
```bash
python -c "import app"
```
