import os
import flet as ft
import speech_recognition as sr
from .speech_backend import SpeechBackend
import tempfile

class AndroidSpeechBackend(SpeechBackend):
    """
    Android Native App용 음성 인식 백엔드
    
    작동 원리:
    1. Flet의 AudioRecorder를 사용하여 마이크 입력을 WAV 파일로 녹음
    2. 녹음이 끝나면 저장된 파일을 speech_recognition 라이브러리로 읽어들임
    3. Google Speech API로 전송하여 텍스트 변환
    """
    def __init__(self, page: ft.Page):
        self.page = page
        self.recognizer = sr.Recognizer()
        # ft.AudioRecorder (Flet 0.24.0+)
        try:
            self.audio_recorder = ft.AudioRecorder(
                audio_encoder=ft.AudioEncoder.WAV
            )
            self.audio_recorder.on_state_changed = self._on_state_changed
            self.page.overlay.append(self.audio_recorder)
            self.page.update()
        except Exception as e:
            print(f"[AndroidBackend] Error initializing AudioRecorder: {e}")
            self.audio_recorder = None
        
        # 녹음 파일 경로 (캐시 디렉토리 등 사용 권장되지만, Flet은 기본적으로 앱 데이터 폴더 사용)
        # 안드로이드에서는 권한 문제로 경로 설정이 중요함. 
        # Flet AudioRecorder는 기본적으로 get_temporary_directory() 등을 사용할 것으로 추정되나,
        # 명시적 경로 없이 output_path를 지정하지 않으면 임시 파일로 저장되거나 에러가 날 수 있음.
        # 일단 단순 파일명으로 시도하고 문제 시 경로 수정.
        self.output_filename = os.path.join(tempfile.gettempdir(), "voice_input.wav")
        
        self.is_recording = False
        self.on_silence_callback = None # 안드로이드 파일 녹음 방식에서는 VAD(무음 감지) 구현이 어려움 (수동 종료 권장)

    def _on_state_changed(self, e):
        print(f"AudioRecorder state changed: {e.data}")

    def start_stt(self, on_silence=None, lang: str = "ko-KR") -> None:
        """
        녹음 시작
        안드로이드는 파일 녹음 방식이므로 실시간 무음 감지(on_silence)는 어렵습니다.
        사용자가 '정지' 버튼을 누를 때까지 계속 녹음합니다.
        """
        self.on_silence_callback = on_silence
        print("[AndroidBackend] Starting recording...")
        
        # 녹음 시작 (WAV 포맷)
        if self.page.platform in ["android", "ios"]:
             # 모바일 환경에서는 경로 이슈가 있을 수 있으므로 주의
             pass
        
        try:
            # ft.AudioRecorder.start_recording takes output_path
            self.audio_recorder.start_recording(self.output_filename)
        except Exception as e:
             print(f"[AndroidBackend] Start invalid config: {e}")
             # Fallback (though arguments are fixed now)
             pass
        self.is_recording = True

    def stop_stt(self) -> str:
        """
        녹음 종료 및 변환 수행
        """
        if not self.is_recording:
            return ""

        print("[AndroidBackend] Stopping recording...")
        try:
            # 녹음 중지 및 파일 저장 완료 대기
            # stop_recording은 비동기일 수 있으나 Flet Python API는 await 없이 호출됨.
            # 하지만 실제 파일이 써지기까지 약간의 딜레이가 필요할 수 있음.
            result = self.audio_recorder.stop_recording()
            self.is_recording = False
            
            # 파일이 저장될 때까지 잠시 대기? (Flet API 동작 확인 필요)
            # 보통 stop_recording() 리턴값으로 경로가 오거나, 지정한 경로에 저장됨.
            
            # 저장된 WAV 파일 인식
            if os.path.exists(self.output_filename):
                print(f"[AndroidBackend] File found: {self.output_filename}")
                return self._recognize_file(self.output_filename)
            else:
                print(f"[AndroidBackend] Error: Output file not found at {self.output_filename}")
                return "녹음 파일을 찾을 수 없습니다."
                
        except Exception as e:
            print(f"[AndroidBackend] Stop/Recognize Error: {e}")
            return f"오류: {e}"

    def _recognize_file(self, filename: str) -> str:
        print("[AndroidBackend] Removing noise and recognizing...")
        try:
            with sr.AudioFile(filename) as source:
                # 오디오 데이터 읽기
                audio_data = self.recognizer.record(source)
                # 구글 인식 (기본 'ko-KR')
                text = self.recognizer.recognize_google(audio_data, language="ko-KR")
                print(f"[AndroidBackend] Result: {text}")
                return text
        except sr.UnknownValueError:
            print("[AndroidBackend] Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"[AndroidBackend] API Error: {e}")
            return f"통신 오류: {e}"
        except Exception as e:
            print(f"[AndroidBackend] File processing error: {e}")
            return f"처리 오류: {e}"

    def speak(self, text: str, slow: bool = False, lang: str = "ko-KR") -> None:
        """TTS는 기존대로 (필요시 구현, 일단은 더미 혹은 웹 방식 사용)"""
        # Android Native TTS를 쓸 수 있다면 좋지만, 현재는 패스
        print(f"[AndroidBackend] TTS request: {text}")
