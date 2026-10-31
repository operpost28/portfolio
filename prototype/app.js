(() => {
  const content = window.portfolioContent;
  const grid = document.querySelector('#project-grid');
  if (grid) grid.innerHTML = content.projects.map((title, index) => {
    const cover = content.covers?.[index];
    const src = cover ? encodeURI(cover.src) : `assets/project-placeholder-0${index + 1}.svg`;
    return `<article class="project"><div class="project-image${cover ? ' has-cover' : ''}"><img src="${src}" alt="${cover ? title : ''}" loading="lazy" width="${cover?.width || 1200}" height="${cover?.height || 750}">${cover ? '' : '<span class="image-label" data-i18n="frame">Временное изображение</span>'}</div><div class="project-caption"><h3 lang="ru">${title}</h3><span class="project-number">0${index + 1}</span></div></article>`;
  }).join('');
  // Hero background loop: stay on the still poster for visitors who ask for reduced motion.
  const heroVideo = document.querySelector('.hero-video');
  if (heroVideo && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    heroVideo.removeAttribute('autoplay');
    heroVideo.pause();
  }
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
    const pageTitle = document.body.dataset.pageTitle || 'home';
    const seoTitles = {
      ru: {
        home: 'Александр Горулёв — оператор-постановщик кино и сериалов',
        work: 'Работы Александра Горулёва — оператор-постановщик кино и сериалов',
        filmographyTitle: 'Фильмография Александра Горулёва — фильмы и сериалы',
        about: 'Александр Горулёв — биография оператора-постановщика'
      },
      en: {
        home: 'Alexander Gorulev — Director of Photography',
        work: 'Selected Work — Alexander Gorulev | Director of Photography',
        filmographyTitle: 'Filmography — Alexander Gorulev | Director of Photography',
        about: 'Alexander Gorulev — Biography & Contact'
      }
    };
    document.title = seoTitles[lang][pageTitle];
    document.querySelector('.wordmark').setAttribute('aria-label', content[lang].home);
    document.querySelector('.desktop-nav').setAttribute('aria-label', content[lang].nav);
    mobileNav.setAttribute('aria-label', content[lang].mobileNav);
    document.querySelector('[data-close]')?.setAttribute('aria-label', content[lang].close);
    setMenu(false);
    try { localStorage.setItem('portfolio-language', lang); } catch (_) {}
  }
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.lang)));
  menuButton.addEventListener('click', () => setMenu(mobileNav.hidden));
  mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.querySelectorAll('[data-showreel]').forEach(button => button.addEventListener('click', () => {
    setMenu(false);
    dialog.showModal();
    document.body.classList.add('modal-open');
    const player = document.querySelector('#showreel-player');
    player.replaceChildren();
    const iframe = document.createElement('iframe');
    iframe.src = 'https://player.vimeo.com/video/1230723196?autoplay=1&title=0&byline=0&portrait=0';
    iframe.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture');
    iframe.setAttribute('allowfullscreen', '');
    iframe.setAttribute('title', 'Alexander Gorulev — Showreel');
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = '0';
    player.appendChild(iframe);
  }));
  document.querySelector('[data-close]')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  dialog?.addEventListener('close', () => { document.body.classList.remove('modal-open'); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && !mobileNav.hidden) { setMenu(false); menuButton.focus(); } });
  window.matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) setMenu(false); });
  try { const saved = localStorage.getItem('portfolio-language'); if (saved === 'en') setLanguage(saved); } catch (_) {}
})();
