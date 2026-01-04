import asyncio
import base64
import io
import json
import time
import flet as ft
from .speech_backend import SpeechBackend

# JavaScript Code to be injected
# Uses AudioContext to record RAW PCM and encode to WAV (to satisfy Python SpeechRecognition)
JS_CODE = """
window.audioContext = null;
window.mediaStream = null;
window.processor = null;
window.input = null;
window.audioData = [];

function writeWavHeader(sampleRate, dataLength) {
    const buffer = new ArrayBuffer(44);
    const view = new DataView(buffer);
    
    // RIFF identifier 'RIFF'
    view.setUint32(0, 1179011410, false);
    // file length minus RIFF identifier length and file description length
    view.setUint32(4, 36 + dataLength, true);
    // RIFF type 'WAVE'
    view.setUint32(8, 1163280727, false);
    // format chunk identifier 'fmt '
    view.setUint32(12, 544501094, false);
    // format chunk length
    view.setUint32(16, 16, true);
    // sample format (raw)
    view.setUint16(20, 1, true);
    // channel count
    view.setUint16(22, 1, true);
    // sample rate
    view.setUint32(24, sampleRate, true);
    // byte rate (sample rate * block align)
    view.setUint32(28, sampleRate * 2, true);
    // block align (channel count * bytes per sample)
    view.setUint16(32, 2, true);
    // bits per sample
    view.setUint16(34, 16, true);
    // data chunk identifier 'data'
    view.setUint32(36, 1635017060, false);
    // data chunk length
    view.setUint32(40, dataLength, true);

    return buffer;
}

function floatTo16BitPCM(output, offset, input) {
    for (let i = 0; i < input.length; i++, offset += 2) {
        let s = Math.max(-1, Math.min(1, input[i]));
        output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
}

window.startRecording = async function() {
    try {
        console.log("JS: Requesting microphone...");
        window.audioData = [];
        window.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        window.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        window.input = window.audioContext.createMediaStreamSource(window.mediaStream);
        
        // bufferSize: 4096, numInputChannels: 1, numOutputChannels: 1
        window.processor = window.audioContext.createScriptProcessor(4096, 1, 1);
        
        window.processor.onaudioprocess = function(e) {
            const channelData = e.inputBuffer.getChannelData(0);
            // Clone data because channelData is reused
            window.audioData.push(new Float32Array(channelData));
        };
        
        window.input.connect(window.processor);
        window.processor.connect(window.audioContext.destination);
        
        console.log("JS: Recording started");
        
    } catch (err) {
        console.error("JS: Error starting recording", err);
        window.location.hash = "error:" + err.message;
    }
}

window.stopRecording = function() {
    if (window.processor && window.audioContext) {
        window.processor.disconnect();
        window.input.disconnect();
        if (window.mediaStream) {
            window.mediaStream.getTracks().forEach(track => track.stop());
        }
        
        console.log("JS: Recording stopped. Processing WAV...");
        
        // Merge Buffers
        let bufferLength = 0;
        for (let i = 0; i < window.audioData.length; i++) {
            bufferLength += window.audioData[i].length;
        }
        
        const wavBuffer = new ArrayBuffer(44 + bufferLength * 2);
        const view = new DataView(wavBuffer);
        
        // Write Header
        const header = writeWavHeader(window.audioContext.sampleRate, bufferLength * 2);
        new Uint8Array(wavBuffer).set(new Uint8Array(header), 0);
        
        // Write PCM Data
        let offset = 44;
        for (let i = 0; i < window.audioData.length; i++) {
            floatTo16BitPCM(view, offset, window.audioData[i]);
            offset += window.audioData[i].length * 2;
        }
        
        // Convert to Base64
        const blob = new Blob([view], { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => {
             const base64data = reader.result;
             console.log("JS: WAV Ready, sending hash...");
             // Pass data to Flet via Hash
             window.location.hash = "audio_data:" + base64data.split(',')[1]; 
        };
        
        // Cleanup
        window.audioContext.close();
        window.audioContext = null;
        window.processor = null;
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
