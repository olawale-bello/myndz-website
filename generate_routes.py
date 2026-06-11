# Generates per-route HTML files from index.html so every page has a real URL
# with its own <title>, meta description, canonical, and OG tags.
# Re-run after any edit to index.html:  python generate_routes.py
import os, re

SITE = 'https://myndz.net'
BRAND = 'Myndzone Media — Brand Strategy & Creative Direction'
HOME_TITLE = BRAND
HOME_DESC = 'Creative studio in Lagos and Tallinn building brand strategy, identity, and motion design for startups and global brands like UBA, GTBank, and Divest.'

# path, page-id, title, description, og image
ROUTES = [
    ('work', 'work', f'Work | {BRAND}',
     'Selected work from Myndzone Media — brand identity, motion design, and digital campaigns for UBA, GTBank, Reloc8, Guava Homes, Mavie, and more.',
     '/og-image.jpg'),
    ('studio', 'about', f'Studio | {BRAND}',
     'Meet Myndzone Media — a creative studio founded in 2017, working from Lagos and Tallinn on brand strategy, identity systems, and motion design.',
     '/og-image.jpg'),
    ('contact', 'contact', f'Contact | {BRAND}',
     "Start a project with Myndzone Media. Tell us about your brand and we'll come back with how we can help — strategy, identity, or motion.",
     '/og-image.jpg'),
    ('work/impact-in-leadership', 'cs-impact', f'Impact in Leadership | {BRAND}',
     'Nonprofit rebrand for Impact in Leadership Foundation — brand identity, visual system, and social media design by Myndzone Media.',
     '/og/impact-in-leadership.jpg'),
    ('work/divest', 'cs-divest', f'Divest | {BRAND}',
     'Digital marketing and campaign design for Divest, the crypto exchange making conversion simple across Nigeria, South Africa, and Ghana.',
     '/og/divest.jpg'),
    ('work/reloc8', 'cs-reloc8', f'Reloc8 | {BRAND}',
     'Brand identity for Reloc8, the Kigali startup combining ride-hailing with short-let apartments and real estate — one cohesive visual system.',
     '/og/reloc8.jpg'),
    ('work/fund-727', 'cs-fund727', f'Fund 727 | {BRAND}',
     "Explainer animation for GTBank's Fund 727 — motion design that makes investing feel clear, accessible, and trustworthy.",
     '/og/fund-727.jpg'),
    ('work/nano-banana', 'cs-nanobanana', f'Nano Banana | {BRAND}',
     'Nano Banana — a personal project exploring AI-directed automotive visuals with cinematic art direction by Myndzone Media.',
     '/og/nano-banana.jpg'),
    ('work/guava', 'cs-guava', f'Guava | {BRAND}',
     'Luxury real estate branding for Guava Homes — identity, print, packaging, and web design positioning refined living, by Myndzone Media.',
     '/og/guava.jpg'),
    ('work/mavie', 'cs-mavie', f'Mavie | {BRAND}',
     'Product launch video for Mavie, the wellness membership app for modern mothers — motion design and animation by Myndzone Media.',
     '/og/mavie.jpg'),
    ('work/uba-mobile-app', 'cs-uba', f'UBA Mobile App | {BRAND}',
     'Video ad for the UBA mobile app — motion design making digital banking feel effortless for a pan-African audience of 22M+.',
     '/og/uba-mobile-app.jpg'),
]

with open('index.html', encoding='utf-8') as f:
    base = f.read()

assert 'class="pg on" id="p-home"' in base, 'index.html must have p-home active'

for path, pid, title, desc, og in ROUTES:
    head, sep, body = base.partition('</head>')

    head = head.replace(f'<title>{HOME_TITLE}</title>', f'<title>{title}</title>')
    head = head.replace(f'content="{HOME_TITLE}"', f'content="{title}"')
    head = head.replace(HOME_DESC, desc)
    head = head.replace('href="https://myndz.net/"', f'href="{SITE}/{path}"')
    head = head.replace('content="https://myndz.net/"', f'content="{SITE}/{path}"')
    head = head.replace('content="https://myndz.net/og-image.jpg"', f'content="{SITE}{og}"')

    # show this route's page instead of home
    body = body.replace('class="pg on" id="p-home"', 'class="pg" id="p-home"')
    body = body.replace(f'class="pg" id="p-{pid}"', f'class="pg on" id="p-{pid}"')

    # hero video must not auto-download on non-home routes
    body = body.replace(' autoplay muted loop playsinline poster=',
                        ' muted loop playsinline preload="none" data-autoplay="1" poster=')

    # demote homepage h1, promote this page's main heading to h1
    body = re.sub(r'<h1 (style="font-family: var\(--df\); font-size: 42px;[^"]*">We Build<br>Brands That<br><em[^>]*>Move People</em>)</h1>',
                  r'<h2 \1</h2>', body, count=1)
    sec = body.index(f'id="p-{pid}"')
    m = re.compile(r'<h2 class="(dt|cs-hero-title)"([^>]*)>').search(body, sec)
    if m:
        close = body.index('</h2>', m.end())
        body = (body[:m.start()] + f'<h1 class="{m.group(1)}"{m.group(2)}>' +
                body[m.end():close] + '</h1>' + body[close + 5:])

    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(head + sep + body)
    print(f'wrote {path}/index.html')

# ---------- sitemap ----------
urls = [('', '1.0'), ('/work', '0.9'), ('/studio', '0.6'), ('/contact', '0.6')] + \
       [(f'/{p}', '0.8') for p, *_ in ROUTES if p.startswith('work/')]
items = '\n'.join(
    f'  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>2026-06-11</lastmod>\n'
    f'    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>'
    for u, pr in urls)
with open('sitemap.xml', 'w', encoding='utf-8', newline='\n') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'{items}\n</urlset>\n')
print(f'wrote sitemap.xml ({len(urls)} urls)')
