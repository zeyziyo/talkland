# Talkland Speech Architecture

## 개요
Talkland는 플랫폼별 음성 처리 차이를
SpeechBackend 인터페이스로 추상화한다.

## 구조

UI
 └─ SpeechBackend (interface)
     ├─ DesktopSpeechBackend
     │   ├─ Whisper (STT)
     │   └─ pyttsx3 (TTS)
     └─ WebSpeechBackend
         └─ Web Speech API (JS)

## Desktop 전용 이유
- 로컬 마이크 접근 필요
- OS 음성 엔진 의존
- 대용량 Whisper 모델 로딩

## Web / Android 전용 이유
- Python 음성 라이브러리 사용 불가
- 브라우저/웹뷰 API만 허용
- JS 기반 음성 처리 필수

## 설계 원칙
- UI는 플랫폼을 모른다
- Backend가 책임을 가진다
- WebSpeechBackend는 의도적으로 타입을 포기한다
