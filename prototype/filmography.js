(() => {
  const content = window.portfolioContent;
  // Page-specific translations; project titles remain in Russian.
  content.ru.filmographyTitle = 'Фильмография';
  content.en.filmographyTitle = 'Filmography';
  content.ru.filmographySkip = 'Перейти к фильмографии';
  content.en.filmographySkip = 'Skip to filmography';
  let lang = 'ru';
  const menuButton = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('#mobile-nav');
  const dialog = document.querySelector('#showreel-dialog');
  function setMenu(open) {
    mobileNav.hidden = !open;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', content[lang][open ? 'menuClose' : 'menuOpen']);
  }
  function setLanguage(value) {
    lang = value;
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el => { el.innerHTML = content[lang][el.dataset.i18n]; });
    document.querySelectorAll('[data-lang]').forEach(el => el.setAttribute('aria-pressed', String(el.dataset.lang === lang)));
    document.title = `${content[lang].filmographyTitle} — ${content[lang].fullName}`;
    document.querySelector('.wordmark').setAttribute('aria-label', content[lang].home);
    document.querySelector('.desktop-nav').setAttribute('aria-label', content[lang].nav);
    mobileNav.setAttribute('aria-label', content[lang].mobileNav);
    document.querySelector('[data-close]').setAttribute('aria-label', content[lang].close);
    setMenu(false);
    try { localStorage.setItem('portfolio-language', lang); } catch (_) {}
  }
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.lang)));
  menuButton.addEventListener('click', () => setMenu(mobileNav.hidden));
  mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.querySelectorAll('[data-showreel]').forEach(button => button.addEventListener('click', () => { setMenu(false); dialog.showModal(); document.body.classList.add('modal-open');
    const video = document.createElement('video');
    video.src = content.showreelSrc;
    video.controls = true;
    video.playsInline = true;
    video.preload = 'metadata';
    video.setAttribute('aria-label', 'Alexander Gorulev — Showreel');
    document.querySelector('#showreel-player').replaceChildren(video);
    video.play().catch(() => { /* Native controls remain available if playback is blocked. */ }); }));
  document.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  dialog.addEventListener('close', () => { document.body.classList.remove('modal-open'); const video = dialog.querySelector('video'); if (video) { video.pause(); video.removeAttribute('src'); video.load(); } document.querySelector('#showreel-player').replaceChildren(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && !mobileNav.hidden) { setMenu(false); menuButton.focus(); } });
  window.matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) setMenu(false); });
  try { const saved = localStorage.getItem('portfolio-language'); if (saved === 'en') setLanguage(saved); } catch (_) {}
})();
