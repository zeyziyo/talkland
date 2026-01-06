# TalkLand - Render.com 배포 가이드

## 1️⃣ GitHub에 코드 업로드

```bash
# Git 초기화 (처음 한 번만)
git init
git add .
git commit -m "Initial commit for Render deployment"

# GitHub 저장소 생성 후
git remote add origin https://github.com/YOUR_USERNAME/talkland.git
git push -u origin main
```

## 2️⃣ Render.com 배포

### 웹 UI 방식 (권장)

1. **Render.com 가입**
   - https://render.com 접속
   - GitHub 계정으로 가입 (신용카드 불필요)

2. **New Web Service 생성**
   - Dashboard → New + → Web Service
   - Connect GitHub repository
   - `talkland` 저장소 선택

3. **설정**
   - **Name**: `talkland`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
   - **Plan**: `Free`

4. **Deploy 클릭**
   - 자동으로 배포 시작
   - 5-10분 소요

5. **배포 완료**
   - URL 확인: `https://talkland.onrender.com`
   - 안드로이드 브라우저에서 접속!

---

### render.yaml 방식 (자동)

이미 `render.yaml` 파일이 있으므로:

1. GitHub에 push
2. Render.com → New + → Blueprint
3. 저장소 선택
4. 자동으로 `render.yaml` 읽어서 배포

---

## 3️⃣ 주의사항

### Free Plan 제한
- ✅ 무료
- ⚠️ 15분 미사용 시 슬립 모드
  - 첫 접속 시 30초 정도 로딩
  - 이후 정상 속도
- ✅ HTTPS 자동 지원
- ✅ 월 750시간 무료

### 슬립 방지 (선택사항)
무료 플랜에서 슬립 방지하려면:
- 매 14분마다 health check
- UptimeRobot 같은 서비스 사용

---

## 4️⃣ 환경 변수 (필요 시)

Render.com Dashboard → Environment:
- `PYTHON_VERSION`: `3.13.2`
- `PORT`: `10000` (자동 설정됨)

---

## 🎉 배포 완료 후

안드로이드/PC 어디서나:
```
https://your-app-name.onrender.com
```

**모든 기능 작동:**
- ✅ 마이크 (Web Speech API)
- ✅ 번역 (Google Translate)
- ✅ TTS (Edge TTS 고품질 음성)

---

## 🆘 문제 해결

### 배포 실패 시
1. Render.com Dashboard → Logs 확인
2. Python 버전 확인 (`3.13.2` → `3.11`로 변경 시도)
3. requirements.txt 확인

### 앱 느려요
- Free plan의 슬립 모드 때문
- 첫 접속 시 30초 대기 후 정상 속도
