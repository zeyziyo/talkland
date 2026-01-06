// mode2.js - 복습 모드 UI 및 기능
// IndexedDB와 UI를 연결하여 복습 모드 구현

// ==========================================
// 페이지 로드 시 초기화
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('[Mode2] Initializing review mode...');
    injectMode2UI();
    updateReviewCount();
});

// ==========================================
// Mode 2 UI 동적 생성
// ==========================================

function injectMode2UI() {
    const container = document.querySelector('.container');
    const h1 = container.querySelector('h1');

    // 탭 메뉴 생성
    const tabs = document.createElement('div');
    tabs.className = 'tabs';
    tabs.innerHTML = `
        <button id="tab-search" class="tab active" onclick="showMode(1)">
            검색
        </button>
        <button id="tab-review" class="tab" onclick="showMode(2)">
            복습 (0)
        </button>
    `;

    // h1 다음에 탭 삽입
    h1.after(tabs);

    // 기존 UI를 Mode 1로 감싸기
    const existingContent = Array.from(container.children).slice(2); // h1, tabs 제외
    const mode1 = document.createElement('div');
    mode1.id = 'mode1';
    mode1.className = 'mode-content';
    existingContent.forEach(child => mode1.appendChild(child));
    container.appendChild(mode1);

    // Mode 2 UI 생성
    const mode2 = document.createElement('div');
    mode2.id = 'mode2';
    mode2.className = 'mode-content hidden';
    mode2.innerHTML = `
        <div class="review-header">
            <h2>📚 학습 기록</h2>
            <button class="btn-primary" onclick="loadReviewCards()" style="padding: 8px 16px;">
                새로고침
            </button>
        </div>
        <div id="reviewCards"></div>
    `;
    container.appendChild(mode2);

    console.log('[Mode2] UI injected successfully');
}

// ==========================================
// 모드 전환
// ==========================================

function showMode(modeNum) {
    const mode1 = document.getElementById('mode1');
    const mode2 = document.getElementById('mode2');
    const tabSearch = document.getElementById('tab-search');
    const tabReview = document.getElementById('tab-review');

    if (modeNum === 1) {
        mode1.classList.remove('hidden');
        mode2.classList.add('hidden');
        tabSearch.classList.add('active');
        tabReview.classList.remove('active');
    } else {
        mode1.classList.add('hidden');
        mode2.classList.remove('hidden');
        tabSearch.classList.remove('active');
        tabReview.classList.add('active');
        loadReviewCards();
    }
}

// ==========================================
// 복습 카드 로드
// ==========================================

async function loadReviewCards() {
    const records = await getAllStudyRecords();
    const container = document.getElementById('reviewCards');

    if (records.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>아직 학습 기록이 없습니다</h3>
                <p>검색 모드에서 번역을 하면 자동으로 저장됩니다.</p>
            </div>
        `;
        return;
    }

    // 최신순 정렬
    records.sort((a, b) => new Date(b.date) - new Date(a.date));

    container.innerHTML = records.map(record => `
        <div class="review-card" data-id="${record.id}">
            <div class="source">${escapeHtml(record.sourceText)}</div>
            <div class="translated hidden" id="trans-${record.id}">
                ${escapeHtml(record.translatedText)}
            </div>
            <div class="buttons">
                <button class="btn-primary" onclick="toggleTranslation(${record.id})">
                    뒤집기
                </button>
                <button class="btn-secondary" onclick="playFromCache('${escapeHtml(record.translatedText)}', '${record.targetLang}', ${record.id})">
                    🔊 듣기
                </button>
            </div>
            <div class="meta">
                ${getLangName(record.sourceLang)} → ${getLangName(record.targetLang)} | 
                ${formatDate(record.date)}
                ${record.reviewCount > 0 ? ` | 복습 ${record.reviewCount}회` : ''}
            </div>
        </div>
    `).join('');

    updateReviewCount();
}

// ==========================================
// 복습 카드 동작
// ==========================================

function toggle Translation(id) {
    const transEl = document.getElementById(`trans-${id}`);
    transEl.classList.toggle('hidden');

    // 복습 카운트 증가
    if (!transEl.classList.contains('hidden')) {
        updateReviewCount(id);
    }
}

async function playFromCache(text, lang, recordId) {
    const textHash = generateTextHash(text);
    let audioBlob = await getAudioCache(textHash);

    if (audioBlob) {
        // 캐시에서 재생
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        showStatus('오프라인 재생 중 ✓', 'success');

        // 복습 카운트 증가
        if (recordId) {
            await updateReviewCount(recordId);
        }
    } else {
        showStatus('음성 캐시 없음. 검색 모드에서 먼저 들어보세요.', 'warning');
    }
}

async function updateReviewCount(id = null) {
    if (id) {
        const db = await openDB();
        const tx = db.transaction('studyRecords', 'readwrite');
        const store = tx.objectStore('studyRecords');
        const record = await store.get(id);

        if (record) {
            record.reviewCount = (record.reviewCount || 0) + 1;
            record.lastReviewed = new Date().toISOString();
            await store.put(record);
        }
    }

    // 탭 카운트 업데이트
    const records = await getAllStudyRecords();
    const tabReview = document.getElementById('tab-review');
    if (tabReview) {
        tabReview.textContent = `복습 (${records.length})`;
    }
}

// ==========================================
// 유틸리티 함수
// ==========================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getLangName(code) {
    const names = {
        'ko': '한국어',
        'en': 'English',
        'ja': '日本語',
        'es': 'Español',
        'zh-CN': '中文'
    };
    return names[code] || code;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return '오늘';
    if (days === 1) return '어제';
    if (days < 7) return `${days}일 전`;

    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

console.log('[Mode2] Module loaded');
