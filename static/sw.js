const CACHE_NAME = 'mi-icfes-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/app/static/icon-192.png',
  '/app/static/icon-512.png',
];
 
// Instalar: guardar assets en cache
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});
 
// Activar: limpiar caches viejos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});
 
// Fetch: servir desde cache si disponible, si no desde red
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request).catch(() => {
        return caches.match('/');  // Fallback a pagina principal
      });
    })
  );
});