(() => {
  const trailers = new Map([
    ['Свобода', 'https://www.youtube.com/embed/CLNynwu95wI'],
    ['Очень древняя Русь', 'https://rutube.ru/play/embed/4a14ae7486a76adde6699c98e47e1798/'],
    ['Частная жизнь', 'https://www.youtube.com/embed/jsXJIHTceWY'],
    ['И снова здравствуйте 2', 'https://rutube.ru/play/embed/b9c6055252d8a825af04c0461179443d/'],
    ['Склифосовский', 'https://www.youtube.com/embed/Xc1z1KSlbRs']
  ]);
  const dialog = document.querySelector('#trailer-dialog');
  const player = document.querySelector('#trailer-player');
  const title = document.querySelector('#trailer-title');
  document.querySelectorAll('#project-grid .project').forEach(project => {
    const name = project.querySelector('h3').textContent;
    const src = trailers.get(name);
    if (!src) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'trailer-link';
    button.textContent = 'WATCH TRAILER →';
    button.setAttribute('aria-label', `WATCH TRAILER — ${name}`);
    button.setAttribute('aria-haspopup', 'dialog');
    button.addEventListener('click', () => {
      const iframe = document.createElement('iframe');
      iframe.src = src;
      iframe.title = `${name} — трейлер`;
      iframe.allow = 'autoplay; fullscreen; picture-in-picture; encrypted-media';
      iframe.allowFullscreen = true;
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      title.textContent = name;
      player.replaceChildren(iframe);
      dialog.showModal();
      document.body.classList.add('modal-open');
    });
    project.appendChild(button);
  });
  dialog.querySelector('[data-trailer-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    player.replaceChildren();
    document.body.classList.remove('modal-open');
  });
})();
