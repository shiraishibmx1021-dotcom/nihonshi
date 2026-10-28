// 日本史 演習帖 オフライン用
// ネットがあれば最新版を取得して保存、なければ保存済みの版を使う
const CACHE = 'nihonshi-v2';

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(['./', './index.html'])));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    // no-cache：ブラウザに残った古い版を使わず、毎回サーバーに新しい版がないか確かめる
    fetch(e.request, { cache: 'no-cache' })
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() =>
        caches.match(e.request, { ignoreSearch: true })
          .then(hit => hit || (e.request.mode === 'navigate' ? caches.match('./index.html') : undefined))
      )
  );
});
