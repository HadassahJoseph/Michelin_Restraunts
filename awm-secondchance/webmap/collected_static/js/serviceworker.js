const CACHE_NAME = 'michelin-cache-v1';
const urlsToCache = [
  '/',
  '/manifest.json',  // Dynamic manifest
  '/static/images/icons/icon2.png',
  "static/images/screenshots/screenshot1.png", 
  '/location_app',
  // Add other static assets here
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});
