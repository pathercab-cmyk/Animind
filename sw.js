// Service Worker básico para AniMind PWA
const CACHE_NAME = 'animind-v1';

self.addEventListener('install', (e) => {
  console.log('[Service Worker] Instalado');
});

self.addEventListener('fetch', (e) => {
  // Manejo estándar de peticiones
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});