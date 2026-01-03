import os
import flet as ft
import flet_audio_recorder as far
import speech_recognition as sr
from .speech_backend import SpeechBackend
import tempfile

class AndroidSpeechBackend(SpeechBackend):
    """
    Android Native App용 음성 인식 백엔드
    """
    def __init__(self, page: ft.Page):
        self.page = page
        self.recognizer = sr.Recognizer()
        
        # Lazy initialization
        self.audio_recorder = None
        self.init_error = None
        self._recorder_initialized = False
        
        self.output_filename = os.path.join(tempfile.gettempdir(), "voice_input.wav")
        self.is_recording = False
        self.on_silence_callback = None

    def _ensure_recorder_initialized(self):
        if self._recorder_initialized:
            return self.audio_recorder is not None
        
        self._recorder_initialized = True
        
        try:
            print("[AndroidBackend] Initializing flet_audio_recorder (External)...")
            self.audio_recorder = far.AudioRecorder(
                configuration=far.AudioRecorderConfiguration(
                    encoder=far.AudioEncoder.WAV
                ),
                on_state_change=self._on_state_changed
            )
            self.page.overlay.append(self.audio_recorder)
            self.page.update()

            print("[AndroidBackend] AudioRecorder initialized successfully")
            return True
        except Exception as e:
            print(f"[AndroidBackend] Error initializing AudioRecorder: {e}")
            self.init_error = e
            self.audio_recorder = None
            return False

    def _on_state_changed(self, e):
        print(f"AudioRecorder state changed: {e.data}")

    def start_stt(self, on_silence=None, lang: str = "ko-KR") -> None:
        """
        녹음 시작
        Web: output_path 없이 호출 -> Blob URL 반환됨.
        Native: output_path 지정 -> 파일 저장됨.
        """
        self.on_silence_callback = on_silence
        print("[AndroidBackend] Starting recording...")
        
        # Lazy initialization
        if not self._ensure_recorder_initialized():
            print(f"[AndroidBackend] Cannot start: Recorder not initialized.")
            return

        try:
            # Web vs Native Check
            if self.page.web:
                # Web: No path argument
                self.audio_recorder.start_recording()
                print("[AndroidBackend] Web recording started (memory/blob)")
            else:
                # Native: Path argument
                self.audio_recorder.start_recording(self.output_filename)
                print(f"[AndroidBackend] Native recording started ({self.output_filename})")
                
        except Exception as e:
             print(f"[AndroidBackend] Start invalid config: {e}")
             pass
        self.is_recording = True

    def stop_stt(self) -> str:
        """
        녹음 종료 및 변환 수행
        Web: Blob URL -> Bytes -> SR
        Native: File Path -> SR
        """
        if self.audio_recorder is None:
             return f"초기화 오류: {self.init_error}"

        if not self.is_recording:
            return ""

        print("[AndroidBackend] Stopping recording...")
        try:
            # stop_recording() returns the output path or Blob URL
            result_url = self.audio_recorder.stop_recording()
            self.is_recording = False
            
            print(f"[AndroidBackend] Recording stopped. Result: {result_url}")
            
            if self.page.web:
                # Web Flow: Blob URL -> Memory
                return self._recognize_web_blob(result_url)
            else:
                # Native Flow: File Path
                # result_url might be None or the path. Use self.output_filename.
                target_file = self.output_filename
                if os.path.exists(target_file):
                    return self._recognize_file(target_file)
                else:
                     return "녹음 파일을 찾을 수 없습니다."
                
        except Exception as e:
            print(f"[AndroidBackend] Stop/Recognize Error: {e}")
            return f"오류: {e}"

    def _recognize_web_blob(self, blob_url: str) -> str:
        print(f"[AndroidBackend] Processing Web Blob: {blob_url}")
        try:
            import urllib.request
            import io
            
            # Fetch Blob content (Works in Pyodide/Flet Web)
            # Note: This might require specific Pyodide handling if urllib is not patched.
            # But standard Flet examples suggest typical requests work.
            with urllib.request.urlopen(blob_url) as response:
                audio_bytes = response.read()
                
            print(f"[AndroidBackend] Blob fetched. Size: {len(audio_bytes)} bytes")
            
            # Use BytesIO as file-like object for SpeechRecognition
            audio_source = io.BytesIO(audio_bytes)
            
            return self._recognize_source(audio_source)
            
        except Exception as e:
            print(f"[AndroidBackend] Blob processing failed: {e}")
            return f"웹 오디오 처리 오류: {e}"

    def _recognize_file(self, filename: str) -> str:
        # Native file wrapper
        return self._recognize_source(filename)

    def _recognize_source(self, source_obj) -> str:
        # Unified recognition logic
        print("[AndroidBackend] Recognizing...")
        try:
            with sr.AudioFile(source_obj) as source:
                audio_data = self.recognizer.record(source)
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
