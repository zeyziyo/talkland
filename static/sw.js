const CACHE_NAME = 'talkland-v1';
const urlsToCache = [
    '/',
    '/static/manifest.json'
];

// 설치: 앱 파일 캐시
self.addEventListener('install', event => {
    console.log('[SW] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[SW] Caching app shell');
                return cache.addAll(urlsToCache);
            })
    );
    self.skipWaiting();
});

// 활성화: 이전 캐시 삭제
self.addEventListener('activate', event => {
    console.log('[SW] Activating...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Removing old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch: 네트워크 우선, 실패 시 캐시
self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // API 요청은 캐시 안 함
                if (event.request.url.includes('/api/')) {
                    return response;
                }

                // 성공한 응답을 캐시에 복사
                if (response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseClone);
                    });
                }

                return response;
            })
            .catch(() => {
                // 네트워크 실패 시 캐시 반환
                return caches.match(event.request)
                    .then(response => {
                        if (response) {
                            return response;
                        }
                        // 캐시도 없으면 오프라인 페이지 (선택사항)
                        return new Response('오프라인 상태입니다', {
                            status: 503,
                            statusText: 'Service Unavailable'
                        });
                    });
            })
    );
});
