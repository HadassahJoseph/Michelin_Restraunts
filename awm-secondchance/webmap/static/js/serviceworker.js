const CACHE_NAME = 'michelin-cache-v3';
const urlsToCache = [
  '/',
  '/manifest.json',  // Dynamic manifest
  '/static/images/icons/icon2.png',
  '/static/images/screenshots/screenshot1.png', 
  '/location_app',
  // Add other static assets here
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('Failed to cache:', error);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
      .catch(error => {
        console.error('Fetch failed:', error);
      })
  );
});