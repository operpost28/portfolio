#!/usr/bin/env python3
"""Build the project (case) pages of the portfolio from one data table.

Run from the repository root:  python3 tools/build_projects.py
Writes prototype/<slug>.html for every project and prototype/projects-i18n.js.
To add a project's "visual approach" text, fill `task_ru` / `task_en` below and run again.
"""
import json
from html import escape
from pathlib import Path
from PIL import Image

SITE = Path(__file__).resolve().parent.parent / 'prototype'
DOMAIN = 'https://alexandergorulev.com'

# Labels shared by every project page.
LABELS = {
    'ru': {'allWorks': '← Все работы', 'projRole': 'Должность', 'projFormat': 'Формат', 'projYears': 'Год', 'projYearsRange': 'Годы', 'projStatus': 'Статус',
           'projDirector': 'Режиссёр', 'projChannel': 'Канал', 'projCompany': 'Производство',
           'projProducers': 'Продюсеры', 'projPremiere': 'Премьера', 'projTask': 'Визуальная задача',
           'projFrames': 'Кадры', 'projTrailer': 'Смотреть трейлер', 'projNext': 'Следующий проект',
           'projNoFrames': 'Кадры появятся после выхода проекта.',
           'projTaskDraft': 'Здесь будет текст: какую картинку хотели получить, что было самым сложным и как решали, на что снимали.',
           'roleDop': 'Оператор-постановщик', 'roleSecondUnit': 'Оператор-постановщик второго юнита'},
    'en': {'allWorks': '← All work', 'projRole': 'Role', 'projFormat': 'Format', 'projYears': 'Year', 'projYearsRange': 'Years', 'projStatus': 'Status',
           'projDirector': 'Director', 'projChannel': 'Network', 'projCompany': 'Production',
           'projProducers': 'Producers', 'projPremiere': 'Premiere', 'projTask': 'Visual approach',
           'projFrames': 'Frames', 'projTrailer': 'Watch trailer', 'projNext': 'Next project',
           'projNoFrames': 'Frames will be added after the release.',
           'projTaskDraft': 'Text to come: the look we were after, the hardest part and how we solved it, camera and lenses.',
           'roleDop': 'Director of Photography', 'roleSecondUnit': 'Second Unit Director of Photography'},
}

# Same order as the cards on the Works page. Facts come from the site's filmography.
PROJECTS = [
    {'slug': 'lyubov-preodoleet-vse-2', 'title': ('Любовь преодолеет всё 2', 'Love Will Conquer All 2'),
     'type': ('Сериал · в производстве', 'TV series · in production'), 'role': 'roleDop',
     'facts': [('projFormat', '16 серий', '16 episodes'), ('projStatus', 'В производстве', 'In production'),
               ('projDirector', 'Роман Нестеренко', 'Roman Nesterenko'),
               ('projCompany', 'Кинокомпания TEAMFILMS', 'TEAMFILMS'),
               ('projProducers', 'Теймур Джафаров', 'Teymur Dzhafarov')],
     'hero': 'cover.webp', 'frames': [], 'trailer': None},
    {'slug': 'svoboda', 'title': ('Свобода', 'Freedom'),
     'type': ('Полнометражный фильм · 2025', 'Feature film · 2025'), 'role': 'roleDop',
     'facts': [('projFormat', 'Полнометражный фильм', 'Feature film'), ('projYears', '2025', '2025'),
               ('projDirector', 'Евгений Лаврентьев', 'Evgeny Lavrentyev'),
               ('projCompany', 'ИП Евгений Лаврентьев', 'Evgeny Lavrentyev (independent)'),
               ('projPremiere', 'Кинофестиваль «Зимний», декабрь 2025', 'Zimny Film Festival, December 2025')],
     'hero': 'frames/03.webp', 'frames': ['01', '02', '04', '05', '06'],
     'trailer': 'https://www.youtube.com/embed/CLNynwu95wI'},
    {'slug': 'ochen-drevnyaya-rus', 'title': ('Очень древняя Русь', 'Very Ancient Rus'),
     'type': ('Сериал · 2026', 'TV series · 2026'), 'role': 'roleDop',
     'facts': [('projFormat', '12 серий', '12 episodes'), ('projYears', '2026', '2026'),
               ('projDirector', 'Ашот Кещян', 'Ashot Keshchyan'),
               ('projCompany', 'Кинокомпания братьев Андреасян', 'Andreasyan Brothers Film Company')],
     'hero': 'frames/07.webp', 'frames': ['01', '02', '03', '04', '05', '06', '08'],
     'trailer': 'https://rutube.ru/play/embed/4a14ae7486a76adde6699c98e47e1798/'},
    {'slug': 'chastnaya-zhizn', 'title': ('Частная жизнь', 'Private Life'),
     'type': ('Сериал · 2021', 'TV series · 2021'), 'role': 'roleDop',
     'facts': [('projFormat', '16 серий', '16 episodes'), ('projYears', '2021', '2021'),
               ('projDirector', 'Евгений Лаврентьев', 'Evgeny Lavrentyev'),
               ('projCompany', 'Кинокомпания «Русское»', 'Russkoe Film Company'),
               ('projProducers', 'Александр Кушаев, Ирина Смирнова-Бейнарович', 'Alexander Kushaev, Irina Smirnova-Beynarovich')],
     'hero': 'frames/07.webp', 'frames': ['01', '02', '03', '04', '05', '06'],
     'trailer': 'https://www.youtube.com/embed/jsXJIHTceWY'},
    {'slug': 'i-snova-zdravstvuyte-2', 'title': ('И снова здравствуйте 2', 'Hello Again 2'),
     'type': ('Сериал · 2022', 'TV series · 2022'), 'role': 'roleSecondUnit',
     'facts': [('projYears', '2022', '2022'),
               ('projDirector', 'Егор Чичканов', 'Egor Chichkanov'),
               ('projCompany', '«Медиаслово»', 'Mediaslovo'),
               ('projProducers', 'Данила Шарапов, Пётр Ануров', 'Danila Sharapov, Pyotr Anurov')],
     'hero': 'frames/04.webp', 'frames': ['01', '02', '03', '05', '06'],
     'trailer': 'https://rutube.ru/play/embed/b9c6055252d8a825af04c0461179443d/'},
    {'slug': 'sklifosovsky', 'title': ('Склифосовский', 'Sklifosovsky'),
     'type': ('Сериал · 2012–2021', 'TV series · 2012–2021'), 'role': 'roleDop',
     'facts': [('projFormat', '10 сезонов по 16 серий', '10 seasons, 16 episodes each'),
               ('projYearsRange', '2012–2021', '2012–2021'),
               ('projDirector', 'Юлия Краснова', 'Yulia Krasnova'),
               ('projChannel', 'Россия-1', 'Russia-1'),
               ('projCompany', 'Кинокомпания «Русское»', 'Russkoe Film Company'),
               ('projProducers', 'Александр Кушаев, Ирина Смирнова-Бейнарович', 'Alexander Kushaev, Irina Smirnova-Beynarovich')],
     'hero': 'frames/01.webp', 'frames': ['02', '03', '04', '05', '06', '07'],
     'trailer': 'https://www.youtube.com/embed/Xc1z1KSlbRs'},
]
for p in PROJECTS:  # "visual approach" texts, filled in later
    p.setdefault('task_ru', '')
    p.setdefault('task_en', '')

HEAD_NAV = '''  <a class="skip-link" href="#main" data-i18n="skipContent">Перейти к содержанию</a>
  <header class="header">
    <a class="wordmark" href="index.html" aria-label="На главную">AG<span class="wordmark-dot">.</span></a>
    <nav class="desktop-nav" aria-label="Основная навигация">
      <a href="index.html" data-i18n="homeNav">Главная</a>
      <a href="works.html" data-i18n="work">Работы</a>
      <a href="filmography.html" data-i18n="filmographyTitle">Фильмография</a>
      <a href="about.html" data-i18n="about">Обо мне</a>
    </nav>
    <div class="header-actions">
      <div class="languages" aria-label="Language"><button data-lang="ru" aria-pressed="true">RU</button><span>/</span><button data-lang="en" aria-pressed="false">EN</button></div>
      <button class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Открыть меню"><span></span><span></span></button>
    </div>
    <nav id="mobile-nav" class="mobile-nav" aria-label="Мобильная навигация" hidden>
      <a href="index.html" data-i18n="homeNav">Главная</a>
      <a href="works.html" data-i18n="work">Работы</a>
      <a href="filmography.html" data-i18n="filmographyTitle">Фильмография</a>
      <a href="about.html" data-i18n="about">Обо мне</a>
    </nav>
  </header>'''


def size(rel):
    with Image.open(SITE / rel) as im:
        return im.size


def page(i, p):
    slug, (t_ru, t_en) = p['slug'], p['title']
    k = slug.replace('-', '_')
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    nk = nxt['slug'].replace('-', '_')
    e = escape
    hero = f"assets/{slug}/{p['hero']}"
    hw, hh = size(hero)
    facts = [f'          <dt data-i18n="projRole">Должность</dt><dd data-i18n="{p["role"]}">{e(LABELS["ru"][p["role"]])}</dd>']
    for key, ru, _ in p['facts']:
        facts.append(f'          <dt data-i18n="{key}">{e(LABELS["ru"][key])}</dt><dd data-i18n="{k}_{key}">{e(ru)}</dd>')
    if p['task_ru']:
        task = f'          <p data-i18n="{k}_task">{e(p["task_ru"])}</p>'
    else:
        task = ('          <!-- DRAFT: Alexander will provide this text (RU + EN) -->\n'
                '          <p class="draft-note" data-i18n="projTaskDraft">' + e(LABELS['ru']['projTaskDraft']) + '</p>')
    trailer = ''
    if p['trailer']:
        trailer = (f'\n          <button class="trailer-button" type="button" data-trailer="{p["trailer"]}" aria-haspopup="dialog">'
                   '<span class="play-icon" aria-hidden="true">▶</span><span data-i18n="projTrailer">Смотреть трейлер</span></button>')
    if p['frames']:
        items = []
        for n, f in enumerate(p['frames'], 1):
            rel = f'assets/{slug}/frames/{f}.webp'
            w, h = size(rel)
            items.append(f'          <button type="button"><img src="{rel}" alt="«{e(t_ru)}», кадр {n}" width="{w}" height="{h}" loading="lazy"></button>')
        gallery = ('      <section class="project-frames" aria-labelledby="frames-title">\n'
                   '        <h2 id="frames-title" data-i18n="projFrames">Кадры</h2>\n'
                   '        <div class="frame-grid">\n' + '\n'.join(items) + '\n        </div>\n      </section>\n')
    else:
        gallery = ('      <section class="project-frames">\n'
                   '        <p class="frames-note" data-i18n="projNoFrames">' + e(LABELS['ru']['projNoFrames']) + '</p>\n      </section>\n')
    dialogs = ''
    if p['trailer']:
        dialogs += f'''
  <dialog id="trailer-dialog" aria-label="Трейлер / Trailer">
    <div class="dialog-top">
      <p class="eyebrow" data-i18n="{k}_title">{e(t_ru)}</p>
      <button class="close-button" type="button" aria-label="Закрыть / Close" data-trailer-close>×</button>
    </div>
    <div id="trailer-player"></div>
  </dialog>'''
    if p['frames']:
        dialogs += f'''
  <dialog id="frame-dialog" aria-label="Кадр / Frame">
    <div class="dialog-top">
      <p class="eyebrow" data-i18n="{k}_title">{e(t_ru)}</p>
      <button class="close-button" type="button" aria-label="Закрыть / Close" data-frame-close>×</button>
    </div>
    <img alt="">
  </dialog>'''
    title_ru = f'«{t_ru}» — оператор-постановщик Александр Горулёв'
    title_en = f'{t_en} — Alexander Gorulev, Director of Photography'
    year = p['type'][0].split('·')[-1].strip()
    desc = f'«{t_ru}» ({year.lower()}): оператор-постановщик Александр Горулёв. Кадры, трейлер и визуальное решение проекта.'
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{e(desc)}">
  <title>{e(title_ru)}</title>
  <link rel="canonical" href="{DOMAIN}/{slug}">
  <link rel="stylesheet" href="styles.css?v=shared-nav-1">
  <link rel="stylesheet" href="works-trailers.css">
  <link rel="stylesheet" href="project.css?v=2">
  <script src="content.js?v=pages-3" defer></script>
  <script src="projects-i18n.js?v=1" defer></script>
  <script src="app.js?v=pages-4" defer></script>
  <script src="project.js?v=1" defer></script>
</head>
<body id="top" class="inner-page" data-page-title="work"
      data-title-ru="{e(title_ru)}"
      data-title-en="{e(title_en)}">
{HEAD_NAV}

  <main id="main" class="page-content">
    <article class="project-page section-pad" data-project="{e(t_ru)}">
      <a class="back-link" href="works.html" data-i18n="allWorks">← Все работы</a>

      <header class="project-head">
        <p class="eyebrow" data-i18n="{k}_type">{e(p['type'][0])}</p>
        <h1 data-i18n="{k}_title">{e(t_ru)}</h1>
      </header>

      <figure class="project-hero">
        <img src="{hero}" alt="«{e(t_ru)}»" width="{hw}" height="{hh}" fetchpriority="high">
      </figure>

      <section class="project-info">
        <dl class="project-facts">
{chr(10).join(facts)}
        </dl>
        <div class="project-task">
          <h2 data-i18n="projTask">Визуальная задача</h2>
{task}{trailer}
        </div>
      </section>

{gallery}
      <nav class="project-next" aria-label="Проекты">
        <a href="works.html" data-i18n="allWorks">← Все работы</a>
        <a href="{nxt['slug']}.html"><span data-i18n="projNext">Следующий проект</span>: <span data-i18n="{nk}_title">{e(nxt['title'][0])}</span> →</a>
      </nav>
    </article>
  </main>
{dialogs}
</body>
</html>
'''


def i18n():
    out = {'ru': dict(LABELS['ru']), 'en': dict(LABELS['en'])}
    for p in PROJECTS:
        k = p['slug'].replace('-', '_')
        for li, lang in enumerate(('ru', 'en')):
            out[lang][f'{k}_title'] = p['title'][li]
            out[lang][f'{k}_type'] = p['type'][li]
            for key, ru, en in p['facts']:
                out[lang][f'{k}_{key}'] = (ru, en)[li]
            if p['task_ru']:
                out[lang][f'{k}_task'] = p['task_ru'] if lang == 'ru' else (p['task_en'] or p['task_ru'])
    body = json.dumps(out, ensure_ascii=False, indent=1)
    return ('// Generated by tools/build_projects.py — edit the data there, not here.\n'
            f'(() => {{ const t = {body};\n'
            '  Object.assign(window.portfolioContent.ru, t.ru);\n'
            '  Object.assign(window.portfolioContent.en, t.en);\n})();\n')


if __name__ == '__main__':
    for i, p in enumerate(PROJECTS):
        (SITE / f"{p['slug']}.html").write_text(page(i, p), encoding='utf-8')
        print('wrote', p['slug'] + '.html')
    (SITE / 'projects-i18n.js').write_text(i18n(), encoding='utf-8')
    print('wrote projects-i18n.js')
