// app/speech/web/web_speech.js

let recognition = null;

// =========================
// STT
// =========================
function startSTT(lang = 'ko-KR') {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        flet.sendEvent("stt-result", { text: "" });
        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    recognition = new SpeechRecognition();
    recognition.lang = lang;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        flet.sendEvent("stt-result", { text });
    };

    recognition.onerror = () => {
        flet.sendEvent("stt-result", { text: "" });
    };

    recognition.start();
}

function stopSTT() {
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
}

// =========================
// TTS
// =========================
function speak(text, slow = false, lang = 'ko-KR') {
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = lang;
    utter.rate = slow ? 0.7 : 1.0;
    speechSynthesis.speak(utter);
}
