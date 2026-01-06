// db.js - IndexedDB 데이터베이스 관리
const DB_NAME = 'TalkLandDB';
const DB_VERSION = 1;

// ==========================================
// DB 열기 및 초기화
// ==========================================

function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onerror = () => {
            console.error('[DB] Error opening database:', request.error);
            reject(request.error);
        };

        request.onsuccess = () => {
            console.log('[DB] Database opened successfully');
            resolve(request.result);
        };

        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            console.log('[DB] Upgrading database...');

            // 1. 학습 기록 저장소
            if (!db.objectStoreNames.contains('studyRecords')) {
                const store = db.createObjectStore('studyRecords', {
                    keyPath: 'id',
                    autoIncrement: true
                });
                store.createIndex('date', 'date', { unique: false });
                store.createIndex('sourceLang', 'sourceLang', { unique: false });
                store.createIndex('targetLang', 'targetLang', { unique: false });
                console.log('[DB] Created studyRecords store');
            }

            // 2. 번역 캐시
            if (!db.objectStoreNames.contains('translations')) {
                db.createObjectStore('translations', { keyPath: 'key' });
                console.log('[DB] Created translations store');
            }

            // 3. TTS 음성 캐시
            if (!db.objectStoreNames.contains('audioCache')) {
                db.createObjectStore('audioCache', { keyPath: 'textHash' });
                console.log('[DB] Created audioCache store');
            }
        };
    });
}

// ==========================================
// 학습 기록 (studyRecords)
// ==========================================

async function saveStudyRecord(record) {
    try {
        const db = await openDB();
        const tx = db.transaction('studyRecords', 'readwrite');
        const store = tx.objectStore('studyRecords');

        const data = {
            sourceText: record.sourceText,
            translatedText: record.translatedText,
            sourceLang: record.sourceLang,
            targetLang: record.targetLang,
            date: new Date().toISOString(),
            reviewCount: 0,
            lastReviewed: null
        };

        await store.add(data);
        console.log('[DB] Study record saved:', data);
        return true;
    } catch (error) {
        console.error('[DB] Error saving study record:', error);
        return false;
    }
}

async function getAllStudyRecords() {
    try {
        const db = await openDB();
        const tx = db.transaction('studyRecords', 'readonly');
        const store = tx.objectStore('studyRecords');

        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => {
                console.log(`[DB] Retrieved ${request.result.length} study records`);
                resolve(request.result);
            };
            request.onerror = () => reject(request.error);
        });
    } catch (error) {
        console.error('[DB] Error getting study records:', error);
        return [];
    }
}

async function updateReviewCount(id) {
    try {
        const db = await openDB();
        const tx = db.transaction('studyRecords', 'readwrite');
        const store = tx.objectStore('studyRecords');

        const record = await store.get(id);
        if (record) {
            record.reviewCount = (record.reviewCount || 0) + 1;
            record.lastReviewed = new Date().toISOString();
            await store.put(record);
            console.log(`[DB] Updated review count for record ${id}`);
        }
    } catch (error) {
        console.error('[DB] Error updating review count:', error);
    }
}

// ==========================================
// 번역 캐시 (translations)
// ==========================================

async function cacheTranslation(key, translation) {
    try {
        const db = await openDB();
        const tx = db.transaction('translations', 'readwrite');
        const store = tx.objectStore('translations');

        await store.put({
            key,
            translation,
            timestamp: Date.now()
        });
        console.log('[DB] Translation cached:', key);
    } catch (error) {
        console.error('[DB] Error caching translation:', error);
    }
}

async function getCachedTranslation(key) {
    try {
        const db = await openDB();
        const tx = db.transaction('translations', 'readonly');
        const store = tx.objectStore('translations');

        return new Promise((resolve, reject) => {
            const request = store.get(key);
            request.onsuccess = () => {
                const result = request.result;
                if (result) {
                    console.log('[DB] Translation cache hit:', key);
                    resolve(result.translation);
                } else {
                    console.log('[DB] Translation cache miss:', key);
                    resolve(null);
                }
            };
            request.onerror = () => reject(request.error);
        });
    } catch (error) {
        console.error('[DB] Error getting cached translation:', error);
        return null;
    }
}

// ==========================================
// TTS 음성 캐시 (audioCache)
// ==========================================

async function saveAudioCache(textHash, audioBlob, voice) {
    try {
        const db = await openDB();
        const tx = db.transaction('audioCache', 'readwrite');
        const store = tx.objectStore('audioCache');

        await store.put({
            textHash,
            audioBlob,
            voice,
            timestamp: Date.now()
        });
        console.log('[DB] Audio cached:', textHash);
    } catch (error) {
        console.error('[DB] Error saving audio cache:', error);
    }
}

async function getAudioCache(textHash) {
    try {
        const db = await openDB();
        const tx = db.transaction('audioCache', 'readonly');
        const store = tx.objectStore('audioCache');

        return new Promise((resolve, reject) => {
            const request = store.get(textHash);
            request.onsuccess = () => {
                const result = request.result;
                if (result) {
                    console.log('[DB] Audio cache hit:', textHash);
                    resolve(result.audioBlob);
                } else {
                    console.log('[DB] Audio cache miss:', textHash);
                    resolve(null);
                }
            };
            request.onerror = () => reject(request.error);
        });
    } catch (error) {
        console.error('[DB] Error getting audio cache:', error);
        return null;
    }
}

// ==========================================
// 유틸리티 함수
// ==========================================

function generateTextHash(text) {
    // 간단한 해시 생성 (Base64)
    return btoa(encodeURIComponent(text)).substring(0, 32);
}

// 초기화
console.log('[DB] IndexedDB module loaded');
