# app/desktop_speech/desktop_speech_backend.py
"""
DesktopSpeechBackend

- Windows / macOS / Linux 전용
- STT: Google Web Speech API (온라인)
- TTS: Edge TTS (외부 프로세스)
- Android/Web 빌드에서 import 금지
"""

from __future__ import annotations
from typing import Optional, List
import time
import tempfile
import subprocess
import sys

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

from .speech_backend import SpeechBackend
import speech_recognition as sr



import os

class DesktopSpeechBackend(SpeechBackend):
    """데스크탑 전용 STT / TTS 백엔드"""

    def __init__(self) -> None:
        self._fs: int = 16000
        self._recording: List[np.ndarray] = []
        self._stream: Optional[sd.InputStream] = None
        self._recognizer = sr.Recognizer()

    # -------------------------
    # STT
    # -------------------------

    def start_stt(self, on_silence: Optional[callable] = None) -> None:
        """
        마이크 녹음을 시작한다.
        on_silence: 10초 이상 무음 시 호출될 콜백 함수
        """
        self._recording.clear()
        self._on_silence = on_silence
        self._last_speech_time = time.time()
        self._silence_limit = 10.0  # 초
        self._energy_threshold = 0.01  # 적당한 임계값 (조정 필요)

        def callback(indata, frames, time_info, status):
            if status:
                print("Audio status:", status)
            
            # 오디오 데이터 복사 및 저장
            data_copy = indata.copy()
            self._recording.append(data_copy)
            
            # 에너지(RMS) 계산
            rms = np.sqrt(np.mean(data_copy**2))
            
            # 말하고 있으면 시간 갱신
            if rms > self._energy_threshold:
                self._last_speech_time = time.time()
            
            # 무음 지속 시간 체크
            silence_duration = time.time() - self._last_speech_time
            if silence_duration > self._silence_limit:
                if self._on_silence:
                     # 콜백 호출 (주의: 별도 스레드에서 실행됨)
                    self._on_silence()
                    # 중복 호출 방지를 위해 콜백 제거
                    self._on_silence = None

        self._stream = sd.InputStream(
            samplerate=self._fs,
            channels=1,
            callback=callback,
        )
        self._stream.start()

    def stop_stt(self) -> Optional[str]:
        """
        녹음을 종료하고 Google Web Speech API로 음성을 텍스트로 변환한다.
        """
        if not self._stream:
            return None

        self._stream.stop()
        self._stream.close()
        self._stream = None

        if not self._recording:
            return None

        audio = np.concatenate(self._recording, axis=0)
        
        # float32 -> int16 변환 (SpeechRecognition 호환성)
        audio_int16 = np.int16(audio * 32767)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav.write(f.name, self._fs, audio_int16)
            wav_path = f.name
            
        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = self._recognizer.record(source)
                # 한국어 인식 (fallback to English if needed, but fixing to ko-KR as per request)
                text = self._recognizer.recognize_google(audio_data, language="ko-KR")
                return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"STT Error: {e}")
            return None
        finally:
            if os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except:
                    pass

    # -------------------------
    # TTS
    # -------------------------

    def speak(self, text: str, lang: str = "ko", slow: bool = False) -> None:
        """
        외부 프로세스를 통해 음성을 재생한다. (Edge TTS 사용)
        lang: 'ko' | 'es'
        """
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "tts_play.py")
        
        # args: [python, script_path, text, lang, slow]
        args = [sys.executable, script_path, text, lang]
        if slow:
            args.append("slow")
        subprocess.Popen(args)
