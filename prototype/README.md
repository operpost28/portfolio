# Portfolio — visual prototype

Static homepage prototype for Alexander Gorulev. No build step or dependencies.

Open index.html directly, or serve this folder locally:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Then open http://127.0.0.1:4173.

## Scope

Responsive homepage, RU/EN UI, mobile navigation, accessible native showreel dialog. Escape closes the dialog and mobile menu. Language preference is saved locally when storage is available. The external Kinopoisk link is the user's supplied URL.

All SVG artwork is explicitly temporary abstract placeholder artwork, not footage or a representation of the listed productions. Project names stay in Russian pending approved English titles. Cards are deliberately non-interactive because project pages are outside this stage. No biography, dates, credits, contact details are invented. There is no CMS, backend, contact submission or production deployment.

Featured work layout is provisional. Real stills will inform its final arrangement. content.js holds interface copy and project names; styles.css holds layout. The font loads from Google Fonts, with local Arial/sans-serif fallback. Replacing the SVGs with actual media will not require changing the content structure.

Showreel: user-provided YouTube video oEOQJXaLBaw. The embed is created only on click and removed on dialog close to stop playback. A direct YouTube link remains available. Test over HTTP; file:// embedding may be rejected by YouTube.

The supplied MP4 is now the primary player source: assets/showreel.mp4. It is loaded only when the showreel dialog opens. Closing pauses playback and releases the source. YouTube remains an optional external link.
