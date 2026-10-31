// Project pages: trailer in a dialog, frames open full size.
(() => {
  const page = document.querySelector('.project-page');
  if (!page) return;

  const trailerDialog = document.querySelector('#trailer-dialog');
  const trailerPlayer = document.querySelector('#trailer-player');
  const trailerButton = document.querySelector('[data-trailer]');
  trailerButton?.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = trailerButton.dataset.trailer;
    iframe.title = `${page.dataset.project} — трейлер`;
    iframe.allow = 'autoplay; fullscreen; picture-in-picture; encrypted-media';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    trailerPlayer.replaceChildren(iframe);
    trailerDialog.showModal();
    document.body.classList.add('modal-open');
  });
  trailerDialog?.querySelector('[data-trailer-close]').addEventListener('click', () => trailerDialog.close());
  // Removing the player on close stops the sound.
  trailerDialog?.addEventListener('close', () => { trailerPlayer.replaceChildren(); document.body.classList.remove('modal-open'); });

  const frameDialog = document.querySelector('#frame-dialog');
  const frameImage = frameDialog?.querySelector('img');
  document.querySelectorAll('.frame-grid button').forEach(button => button.addEventListener('click', () => {
    const img = button.querySelector('img');
    frameImage.src = img.currentSrc || img.src;
    frameImage.alt = img.alt;
    frameDialog.showModal();
    document.body.classList.add('modal-open');
  }));
  frameDialog?.querySelector('[data-frame-close]').addEventListener('click', () => frameDialog.close());
  frameDialog?.addEventListener('close', () => document.body.classList.remove('modal-open'));
  [trailerDialog, frameDialog].forEach(dialog => dialog?.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  }));
})();
