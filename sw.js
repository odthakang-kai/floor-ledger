/* Floor Ledger service worker.
   The page is network-first (updates show up when online, cached copy when not); everything else is cache-first.
   Bump VERSION when you change icons or the manifest. Your entries live in localStorage, never in this cache. */
const VERSION = "2026-11-10a";
const CACHE = "fl-" + VERSION;
const SHELL = ["./", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "apple-touch-icon.png"];
const FONT_HOSTS = ["fonts.googleapis.com", "fonts.gstatic.com"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL.map(u => new Request(u, {cache: "reload"})))).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("fl-") && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

async function pageFirst(req) {
  const cache = await caches.open(CACHE);
  const net = fetch(req, {cache: "no-store"}).then(r => { if (r && r.ok) cache.put("./", r.clone()); return r; });
  const timeout = new Promise(res => setTimeout(() => res(null), 3500));
  try { const r = await Promise.race([net, timeout]); if (r && r.ok) return r; } catch (e) {}
  const hit = await cache.match("./");
  return hit || net;
}

async function cacheFirst(req) {
  const hit = await caches.match(req, {ignoreSearch: true});
  if (hit) return hit;
  const r = await fetch(req);
  if (r && (r.ok || r.type === "opaque")) { const c = await caches.open(CACHE); c.put(req, r.clone()); }
  return r;
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin === location.origin) e.respondWith(req.mode === "navigate" || url.pathname.endsWith("/index.html") ? pageFirst(req) : cacheFirst(req));
  else if (FONT_HOSTS.includes(url.hostname)) e.respondWith(cacheFirst(req));
});
