// auto-save.js - 자동 저장 기능
// 번역 및 TTS 실행 시 자동으로 IndexedDB에 저장

// ==========================================
// 기존 doTranslate 함수 확장
// ==========================================

// 원래 doTranslate 함수를 저장
const originalDoTranslate = window.doTranslate;

// 새로운 doTranslate 함수로 덮어쓰기
window.doTranslate = async function () {
    const sourceText = document.getElementById('sourceText').value.trim();
    if (!sourceText) {
        showStatus('번역할 텍스트를 입력하세요', 'error');
        return;
    }

    // 언어 코드 매핑
    const langMap = {
        'ko-KR': 'ko',
        'en-US': 'en',
        'es-ES': 'es',
        'ja-JP': 'ja',
        'zh-CN': 'zh-CN',
        'fr-FR': 'fr',
        'de-DE': 'de'
    };

    const sourceLangFull = document.getElementById('sourceLang').value;
    const targetLangFull = document.getElementById('targetLang').value;

    const sourceLang = langMap[sourceLangFull] || sourceLangFull.split('-')[0];
    const targetLang = langMap[targetLangFull] || targetLangFull.split('-')[0];

    console.log('Translation request:', { sourceText, sourceLang, targetLang });
    showStatus('번역 중...', 'info');

    try {
        const requestBody = {
            text: sourceText,
            source_lang: sourceLang,
            target_lang: targetLang
        };

        console.log('Sending to /api/translate:', requestBody);

        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Translation result:', data);

        if (data.error) {
            showStatus('번역 실패: ' + data.error, 'error');
            alert(data.error);
        } else {
            const translatedText = data.translated_text;
            document.getElementById('translatedText').value = translatedText;
            showStatus('번역 완료!', 'success');

            // ========================================
            // IndexedDB에 자동 저장
            // ========================================
            await saveStudyRecord({
                sourceText,
                translatedText,
                sourceLang,
                targetLang
            });
            console.log('[AutoSave] Study record saved');

            // 번역 캐시
            const cacheKey = `${sourceLang}-${targetLang}-${sourceText}`;
            await cacheTranslation(cacheKey, translatedText);
            console.log('[AutoSave] Translation cached');

            // 복습 카운트 업데이트
            if (window.updateReviewCount) {
                await updateReviewCount();
            }
        }
    } catch (error) {
        console.error('Translation error:', error);
        showStatus('번역 실패: ' + error.message, 'error');
        alert('번역 오류: ' + error.message + '\n\n브라우저 콘솔(F12)을 확인하세요.');
    }
};

// ==========================================
// 기존 playTTS 함수 확장
// ==========================================

const originalPlayTTS = window.playTTS;

window.playTTS = async function () {
    const text = document.getElementById('translatedText').value.trim();
    if (!text) {
        showStatus('재생할 텍스트가 없습니다', 'error');
        return;
    }

    const targetLang = document.getElementById('targetLang').value;
    const voice = window.voiceMap[targetLang];
    const textHash = generateTextHash(text);

    showStatus('음성 생성 중...', 'info');

    try {
        // 1. 캐시 확인
        let audioBlob = await getAudioCache(textHash);

        if (audioBlob) {
            console.log('[AutoSave] Using cached audio');
            showStatus('캐시에서 재생 중...', 'info');
        } else {
            // 2. 서버에서 다운로드
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    voice: voice,
                    rate: '+0%'
                })
            });

            if (!response.ok) {
                throw new Error('TTS failed');
            }

            audioBlob = await response.blob();

            // 3. 캐시에 저장
            await saveAudioCache(textHash, audioBlob, voice);
            console.log('[AutoSave] Audio cached');
        }

        // 4. 재생
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);

        audio.onended = () => {
            URL.revokeObjectURL(audioUrl);
            showStatus('재생 완료', 'success');
        };

        audio.onerror = () => {
            showStatus('재생 실패', 'error');
        };

        audio.play();
        showStatus('재생 중...', 'info');

    } catch (error) {
        console.error('TTS error:', error);
        showStatus('음성 생성 실패', 'error');
    }
};

console.log('[AutoSave] Module loaded - doTranslate and playTTS extended with auto-save');
