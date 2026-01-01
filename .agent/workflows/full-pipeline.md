---
description: 전체 파이프라인 - 검증부터 배포까지
---
// turbo-all

# 전체 파이프라인 (코드 수정 → 검증 → 커밋 → 빌드 트리거)

## 1. Python 문법 검사
```bash
python -m py_compile main.py
```

## 2. 앱 모듈 임포트 검사
```bash
python -c "import app; print('✅ App module OK')"
```

## 3. 로컬 테스트 실행 (있는 경우)
```bash
python -c "print('✅ No unit tests configured - skipping')"
```

## 4. 변경 사항 확인
```bash
git status
```

## 5. 변경 사항 스테이징
```bash
git add -A
```

## 6. 커밋 생성
```bash
git commit -m "chore: 자동 커밋"
```

## 7. main 브랜치에 푸시 (GitHub Actions 빌드 트리거)
```bash
git push origin main
```

## 8. 완료 메시지
푸시가 완료되면 GitHub Actions에서 자동으로 Android APK 빌드가 시작됩니다.
GitHub Repository의 Actions 탭에서 빌드 진행 상황을 확인하세요.
