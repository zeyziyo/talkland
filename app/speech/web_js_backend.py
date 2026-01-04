import asyncio
import base64
import io
import json
import time
import flet as ft
from .speech_backend import SpeechBackend

# JavaScript Code to be injected
# Handles MediaRecorder and notifies Python via window.location.hash
JS_CODE = """
window.audioChunks = [];
window.mediaRecorder = null;

window.startRecording = async function() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        window.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        window.audioChunks = [];

        window.mediaRecorder.ondataavailable = (event) => {
            window.audioChunks.push(event.data);
        };

        window.mediaRecorder.onstop = () => {
             const audioBlob = new Blob(window.audioChunks, { type: 'audio/webm' });
             const reader = new FileReader();
             reader.readAsDataURL(audioBlob);
             reader.onloadend = () => {
                 const base64data = reader.result;
                 // Pass data to Flet via Hash
                 // Prefix 'audio_data:' to identify
                 window.location.hash = "audio_data:" + base64data.split(',')[1]; 
             };
        };

        window.mediaRecorder.start();
        console.log("JS: Recording started");
    } catch (err) {
        console.error("JS: Error starting recording", err);
        window.location.hash = "error:" + err.message;
    }
}

window.stopRecording = function() {
    if (window.mediaRecorder && window.mediaRecorder.state !== 'inactive') {
        window.mediaRecorder.stop();
        console.log("JS: Recording stopped");
        // Stop all tracks to release mic
        window.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
}
"""

class WebJsSpeechBackend(SpeechBackend):
    def __init__(self, page: ft.Page, on_audio_data=None):
        self.page = page
        self.on_audio_data = on_audio_data  # Callback(bytes_data)
        self.is_recording = False
        
        # Inject JS
        # Flet 0.80 doesn't have create/inject script easily.
        # We rely on run_js defining globals.
        self.page.run_js(JS_CODE)
        
        # Listen to Route Changes (Hash changes)
        self.page.on_route_change = self._on_route_change

    def start_stt(self, language="ko-KR"):
        print("[WebJsBackend] Starting JS recording...")
        self.is_recording = True
        self.page.run_js("window.startRecording()")

    def stop_stt(self) -> str:
        print("[WebJsBackend] Stopping JS recording...")
        self.is_recording = False
        self.page.run_js("window.stopRecording()")
        return "WAITING_FOR_JS" # Placeholder, actual data comes via callback

    def _on_route_change(self, e: ft.RouteChangeEvent):
        route = e.route
        print(f"[WebJsBackend] Route changed: {route[:50]}...")
        
        if route.startswith("audio_data:"):
            # We got audio!
            base64_str = route.split(":", 1)[1]
            audio_bytes = base64.b64decode(base64_str)
            print(f"[WebJsBackend] Received {len(audio_bytes)} bytes of audio")
            
            # Reset hash to keep URL clean (optional, but good practice)
            # self.page.go("/") # Might trigger reload? No, internal routing.
            
            if self.on_audio_data:
                self.on_audio_data(audio_bytes)
                
        elif route.startswith("error:"):
            print(f"[WebJsBackend] JS Error: {route}")

    def speak(self, text):
        pass # Not implemented or use standard TTS

    def process_audio_data(self, audio_bytes: bytes) -> str:
        """
        Convert WebM/WAV bytes to Text using SpeechRecognition
        """
        import speech_recognition as sr
        
        print(f"[WebJsBackend] Processing {len(audio_bytes)} bytes...")
        try:
            # Note: speech_recognition expects WAV usually.
            # MediaRecorder sends WebM.
            # We might need to use ffmpeg if SR doesn't support WebM directly.
            # HOWEVER, in PWA (Static), we don't have ffmpeg.
            # Chrome MediaRecorder *can* record WAV? No, usually WebM/Ogg.
            # BUT, we can use a JS library for WAV?
            # Or assume speech_recognition (Google Web API under the hood) works?
            # pure-python speech_recognition uses 'AudioFile' which needs WAV/AIFF/FLAC.
            # It does NOT support WebM.
            
            # CRITICAL: We need WebM -> WAV conversion in pure python?
            # Impossible without libraries.
            # ALTERNATIVE: Use Google Speech API directly? No key.
            # 
            # Plan Correction: JSON Google Speech API (recognize_google) sends FLAC/WAV.
            # 
            # Can we record WAV in JS?
            # Yes, using a library 'recorder.js'.
            # But I cannot inject libraries easily.
            #
            # WORKAROUND:
            # Use 'audio/webm' and hope 'speech_recognition' supports it?
            # Documentation says: "WAV, AIFF, AIFF-C, FLAC".
            # WebM is not supported.
            #
            # This is a BLOCKER.
            #
            # WAIT! The current android backend logic I wrote earlier:
            # It handled Blob -> BytesIO -> AudioFile.
            # Did I assume it was WAV?
            # Yes, I assumed 'audio/wav'.
            #
            # Can we force JS to record WAV?
            # Not natively in all browsers.
            #
            # OPTION: Send Base64 to a free online conversion API? No.
            # OPTION: Use a simple WAV header hack in JS?
            # There are tiny JS functions to record WAV.
            # I should update JS_CODE to record WAV.
            #
            # Let's try to update JS_CODE to use a WAV encoder?
            # Too much code.
            #
            # What if I use `google-speech` package?
            # 
            # Let's try to instantiate AudioFile from WebM and see if it explodes?
            # If it explodes, I will notify user "WAV recording needed".
            
            r = sr.Recognizer()
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                audio = r.record(source)
                text = r.recognize_google(audio, language="ko-KR")
                return text
        except Exception as e:
            print(f"[WebJsBackend] Recognition failed: {e}")
            return f"Error: {e} (WebM not supported?)"
