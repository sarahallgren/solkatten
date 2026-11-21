#!/usr/bin/env python3
"""
Bygger Solkattens webbplats till mappen dist/.

Kör:  python3 bygg.py
Kräver bara Python 3 (inga tillägg behövs).

Innehållet ligger i mappen innehall/:
  startsida.html                 startsidan
  sidor/<avdelning>/index.html   huvudsidorna (Skaffa katt, Kattfakta ...)
  sidor/<avdelning>/<sida>.html  undersidorna
  nyheter/ÅÅÅÅ-MM-DD-namn.html   nyheter
  aktiviteter/ÅÅÅÅ-MM-DD-namn.html  aktiviteter (visas tills datumet passerat)

Varje fil börjar med en informationsruta:
  <!--
  titel: Rubriken på sidan
  ordning: 1            (bestämmer ordningen i menyn)
  beskrivning: ...      (kort text på länkkortet och i Google)
  -->
"""
import os, re, shutil, datetime, html

ROT = os.path.dirname(os.path.abspath(__file__))
INN = os.path.join(ROT, 'innehall')
DIST = os.path.join(ROT, 'dist')
# Den lösenordsskyddade medlemssidan byggs separat, så att den aldrig skrivs över på servern
DIST_MEDLEM = os.path.join(ROT, 'dist-medlemssida')
DOMAN = 'https://solkattenskelleftea.se'
KLUBB = 'Solkatten Skellefteå kattklubb'
IDAG = datetime.date.today()
# För förhandsvisning på GitHub Pages: BAS=/solkatten python3 bygg.py
# BAS läggs före alla interna länkar. Förhandsvisningen stängs ute från Google.
BAS = os.environ.get('BAS', '').rstrip('/')
# Stängd för Google tills lanseringen. Ändra till True den dag sidan ska bli sökbar.
OPPEN_FOR_GOOGLE = False
FORHANDSVISNING = bool(BAS) or os.environ.get('FORHANDSVISNING') == '1' or not OPPEN_FOR_GOOGLE

# Menyns huvudval i ordning. 'typ': sida = mapp under innehall/sidor, lank = fast länk
MENY = [
    {'typ': 'sida', 'namn': 'skaffa-katt'},
    {'typ': 'sida', 'namn': 'kattfakta'},
    {'typ': 'sida', 'namn': 'utstallning'},
    {'typ': 'lank', 'titel': 'Aktiviteter', 'url': '/aktiviteter/'},
    {'typ': 'sida', 'namn': 'medlem'},
    {'typ': 'sida', 'namn': 'om-klubben', 'extra': [('Nyheter', '/nyheter/')]},
]

# ------------------------------------------------------------------ läs innehåll
def las(fil):
    text = open(fil, encoding='utf-8').read()
    meta = {}
    m = re.match(r'\s*<!--(.*?)-->\s*', text, re.S)
    if m:
        for rad in m.group(1).strip().splitlines():
            if ':' in rad:
                k, v = rad.split(':', 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text.strip()

def avdelningar():
    avd = {}
    for namn in sorted(os.listdir(os.path.join(INN, 'sidor'))):
        mapp = os.path.join(INN, 'sidor', namn)
        meta, inneh = las(os.path.join(mapp, 'index.html'))
        barn = []
        for f in sorted(os.listdir(mapp)):
            if f == 'index.html' or not f.endswith('.html'):
                continue
            bm, bi = las(os.path.join(mapp, f))
            slug = f[:-5]
            barn.append({'slug': slug, 'url': f'/{namn}/{slug}/', 'meta': bm, 'html': bi})
        barn.sort(key=lambda b: int(b['meta'].get('ordning', 99)))
        avd[namn] = {'url': f'/{namn}/', 'meta': meta, 'html': inneh, 'barn': barn}
    return avd

def inlagg(mapp, prefix):
    ut = []
    p = os.path.join(INN, mapp)
    for f in sorted(os.listdir(p)):
        if not f.endswith('.html'):
            continue
        meta, inneh = las(os.path.join(p, f))
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', f[:-5])
        datum = datetime.date.fromisoformat(meta['datum'])
        ut.append({'slug': slug, 'url': f'/{prefix}/{slug}/', 'meta': meta, 'html': inneh, 'datum': datum})
    return ut

MANADER = ['januari', 'februari', 'mars', 'april', 'maj', 'juni', 'juli', 'augusti', 'september', 'oktober', 'november', 'december']
def svdatum(d):
    return f'{d.day} {MANADER[d.month - 1]} {d.year}'

# ------------------------------------------------------------------ delar
PIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

def meny_html(avd, aktuell):
    rader = []
    for i, post in enumerate(MENY):
        if post['typ'] == 'lank':
            akt = ' class="aktiv"' if aktuell.startswith(post['url']) else ''
            cur = ' aria-current="page"' if aktuell == post['url'] else ''
            rader.append(f'<li{akt}><a href="{post["url"]}"{cur}>{post["titel"]}</a></li>')
            continue
        a = avd[post['namn']]
        titel = a['meta']['titel']
        lankar = [(b['meta']['titel'], b['url']) for b in a['barn'] if b['meta'].get('skyddad') != 'ja']
        lankar += post.get('extra', [])
        uid = f'under-{post["namn"]}'
        akt = ' class="aktiv"' if aktuell.startswith(a['url']) or any(aktuell.startswith(u) for _, u in post.get('extra', [])) else ''
        cur = ' aria-current="page"' if aktuell == a['url'] else ''
        ac = ' aria-current="page"'
        under = ''.join(f'<li><a href="{u}"{ac if aktuell == u else ""}>{t}</a></li>' for t, u in lankar)
        rader.append(
            f'<li{akt}><a href="{a["url"]}"{cur}>{titel}</a>'
            f'<button class="undermeny-knapp" type="button" aria-expanded="false" aria-controls="{uid}"><span class="dold">Visa undersidor till {titel}</span>{PIL}</button>'
            f'<ul class="undermeny" id="{uid}">{under}</ul></li>')
    cur = ' aria-current="page"' if aktuell == '/kontakt/' else ''
    rader.append(f'<li><a class="kontakt-knapp" href="/kontakt/"{cur}>Kontakt</a></li>')
    return '<ul>' + ''.join(rader) + '</ul>'

def sidhuvud(avd, aktuell):
    return f'''<a class="hoppa" href="#innehall">Hoppa till innehållet</a>
<header class="sidhuvud">
  <div class="bredd sidhuvud-inre">
    <a class="logga" href="/"><img src="/bilder/solkatten-logotyp.svg" alt="Solkatten – till startsidan" width="96" height="100"></a>
    <button class="meny-knapp" type="button" aria-expanded="false" aria-controls="huvudmeny"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Meny</button>
    <nav class="huvudmeny" id="huvudmeny" aria-label="Huvudmeny">{meny_html(avd, aktuell)}</nav>
  </div>
</header>'''

def logoruta(bild, alt, url, liten=False):
    k = ' class="liten"' if liten else ''
    img = f'<img src="/bilder/{bild}" alt="{alt}" loading="lazy">'
    return f'<li{k}><a href="{url}">{img}</a></li>' if url else f'<li{k}>{img}</li>'

SIDFOT = f'''<footer class="sidfot">
  <div class="bredd">
    <div class="sidfot-kolumner">
      <div>
        <h2 class="fot-rubrik">Kontakt</h2>
        <ul>
          <li><a href="mailto:solkatten@solkattenskelleftea.se">solkatten@solkattenskelleftea.se</a></li>
          <li>Bankgiro 5083-2054</li>
          <li>BIC SWEDSESS</li>
          <li><a href="/kontakt/">Vem ska ha vad?</a></li>
        </ul>
      </div>
      <div>
        <h2 class="fot-rubrik">Snabblänkar</h2>
        <ul>
          <li><a href="/medlem/bli-medlem/">Bli medlem</a></li>
          <li><a href="/medlem/rabattkoder/">Logga in för medlemmar</a></li>
          <li><a href="https://www.sverak.se/avel-och-uppfodning/stambokfor-kattkull/">Stambokför kattkull</a></li>
          <li><a href="https://www.sverak.se/avel-och-uppfodning/agarandring-i-sveraks-stambok/">Ägarändra katt</a></li>
          <li><a href="https://www.sverak.se/faq/">Frågor och svar</a></li>
        </ul>
      </div>
      <div>
        <h2 class="fot-rubrik">Sociala medier</h2>
        <ul>
          <li><a href="https://facebook.com/solkattenskelleftea/">Facebook</a></li>
          <li><a href="https://instagram.com/solkattenskelleftea">Instagram</a></li>
          <li><a href="https://www.facebook.com/groups/171588874295492/">Medlemsgruppen</a></li>
        </ul>
      </div>
    </div>
    <div class="fot-avdelning">
      <h2 class="fot-rubrik">Kattförbundet</h2>
      <ul class="logorutor">
        {logoruta('logo-sverak.png', 'Kattförbundet Sverak', 'https://www.sverak.se/')}
        {logoruta('logo-fife.jpg', 'FIFe – Fédération Internationale Féline', 'https://fifeweb.org/')}
        {logoruta('logo-mina-katter.png', 'Mina sidor – Kattförbundet Sverak', 'https://minakatter.sverak.se/', True)}
        {logoruta('logo-id-registret.png', 'ID-registret.se', 'https://www.id-registret.se/', True)}
        {logoruta('logo-kopakatt.png', 'Köpakatt.se', 'https://köpakatt.se/', True)}
      </ul>
    </div>
    <div class="fot-avdelning">
      <h2 class="fot-rubrik">Samarbeten</h2>
      <ul class="logorutor">
        {logoruta('sponsor-royal-canin.jpg', 'Royal Canin', 'https://www.royalcanin.se/')}
        {logoruta('sponsor-agria.png', 'Agria', 'https://www.agria.se/')}
        {logoruta('sponsor-hills.png', 'Hill’s', 'https://www.hillspet.se/')}
        {logoruta('sponsor-bjorkis.jpg', 'Björkis', 'https://www.bjorkis.com/')}
        {logoruta('sponsor-supercat.jpg', 'Supercat', 'https://www.supercat.se/')}
        {logoruta('sponsor-langford.png', 'Langford Vets', 'https://www.langfordvets.co.uk/diagnostic-laboratories')}
        {logoruta('sponsor-4pets.png', '4Pets', '')}
      </ul>
    </div>
    <hr class="fot-linje">
    <p class="fot-sist">© {KLUBB} · Ideell kattklubb sedan 1990, ansluten till Sverak och FIFe · <a href="/om-klubben/stadgar-och-personuppgifter/">Stadgar och personuppgifter</a></p>
  </div>
</footer>'''

def text_av(html_text, n=155):
    t = re.sub(r'<[^>]+>', ' ', html_text)
    t = re.sub(r'\[[^\]]*\]', '', t)
    t = html.unescape(re.sub(r'\s+', ' ', t)).strip()
    return (t[:n - 1].rsplit(' ', 1)[0] + '…') if len(t) > n else t

def skal(titel, beskrivning, kropp, aktuell, avd, hem=False, noindex=False):
    sidtitel = f'{KLUBB} – {titel}' if hem else f'{titel} – {KLUBB}'
    robots = '\n<meta name="robots" content="noindex">' if noindex else ''
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{sidtitel}</title>
<meta name="description" content="{html.escape(beskrivning)}">{robots}
<link rel="canonical" href="{DOMAN}{aktuell}">
<link rel="icon" href="/bilder/solkatten-logotyp.svg" type="image/svg+xml">
<link rel="preload" href="/fonter/roboto-serif-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/stil.css">
<script src="/js/meny.js" defer></script>
</head>
<body{' class="hem"' if hem else ''}>
{sidhuvud(avd, aktuell)}
<main id="innehall">
{kropp}
</main>
{SIDFOT}
</body>
</html>
'''

def brodsmulor(led):
    delar = []
    for i, (t, u) in enumerate(led):
        if i == len(led) - 1:
            delar.append(f'<li aria-current="page">{t}</li>')
        else:
            delar.append(f'<li><a href="{u}">{t}</a></li>')
    return f'<nav class="brodsmulor" aria-label="Du är här"><ol>{"".join(delar)}</ol></nav>'

def kort(titel, url, text, rubriknivå='h2'):
    return f'<li class="kort kort-lank"><{rubriknivå}><a href="{url}">{titel}</a></{rubriknivå}><p>{text}</p></li>'

# ------------------------------------------------------------------ bygg
def skriv(url, innehall):
    mapp = os.path.join(DIST, url.strip('/'))
    os.makedirs(mapp, exist_ok=True)
    with open(os.path.join(mapp, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(innehall)

def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROT, 'statiskt'), DIST)
    avd = avdelningar()
    nyheter = sorted(inlagg('nyheter', 'nyheter'), key=lambda x: x['datum'], reverse=True)
    aktiviteter = sorted(inlagg('aktiviteter', 'aktiviteter'), key=lambda x: x['datum'])
    kommande = [a for a in aktiviteter if a['datum'] >= IDAG]
    sitemap = ['/']

    # Startsida
    meta, start = las(os.path.join(INN, 'startsida.html'))
    if kommande:
        pg = ''.join(kort(a['meta']['titel'], a['url'], f'<span class="datum">{svdatum(a["datum"])}</span><br>{a["meta"].get("ingress", "")}', 'h3') for a in kommande[:3])
        pg = f'<section class="bredd sektion pagang" aria-labelledby="pagang"><h2 id="pagang">På gång</h2><ul class="kortlista">{pg}</ul><p><a href="/aktiviteter/">Alla aktiviteter</a></p></section>'
    else:
        pg = ''
    start = start.replace('<!--PAGANG-->', pg)
    skriv('/', skal(meta['titel'], meta['beskrivning'], start, '/', avd, hem=True))

    # Huvudsidor och undersidor
    for namn, a in avd.items():
        m = a['meta']
        bild = f'<img class="toppbild" src="/bilder/{m["bild"]}" alt="{m.get("bild-alt", "")}" width="1600" height="686">' if m.get('bild') else ''
        barnkort = ''.join(kort(b['meta']['titel'], b['url'], b['meta'].get('beskrivning', '')) for b in a['barn'])
        if namn == 'om-klubben':
            barnkort += kort('Nyheter', '/nyheter/', 'Nytt från klubben och från Sverak.')
        undersidor = f'<ul class="kortlista undersidor">{barnkort}</ul>' if barnkort else ''
        kropp = f'''<div class="bredd sida">
{brodsmulor([("Hem", "/"), (m["titel"], a["url"])])}
<h1>{m["titel"]}</h1>
{bild}
<div class="sida-text{' ingress' if a["barn"] else ''}">{a["html"]}</div>
{undersidor}
</div>'''
        skriv(a['url'], skal(m['titel'], m.get('beskrivning') or text_av(a['html']), kropp, a['url'], avd))
        sitemap.append(a['url'])
        for b in a['barn']:
            bm = b['meta']
            skyddad = bm.get('skyddad') == 'ja'
            kropp = f'''<div class="bredd sida">
{brodsmulor([("Hem", "/"), (m["titel"], a["url"]), (bm["titel"], b["url"])])}
<div class="sida-text">
<h1>{bm["titel"]}</h1>
{b["html"]}
</div>
</div>'''
            skriv(b['url'], skal(bm['titel'], bm.get('beskrivning') or text_av(b['html']), kropp, b['url'], avd, noindex=skyddad))
            if not skyddad:
                sitemap.append(b['url'])

    # Nyheter
    lista = ''.join(kort(n['meta']['titel'], n['url'], f'<span class="datum">{svdatum(n["datum"])}</span><br>{n["meta"].get("ingress", "")}') for n in nyheter)
    kropp = f'''<div class="bredd sida">
{brodsmulor([("Hem", "/"), ("Om klubben", "/om-klubben/"), ("Nyheter", "/nyheter/")])}
<h1>Nyheter</h1>
<p class="ingress sida-text">Nytt från klubben och från Sverak.</p>
{f'<ul class="kortlista undersidor">{lista}</ul>' if lista else '<p class="tom">Inga nyheter just nu.</p>'}
</div>'''
    skriv('/nyheter/', skal('Nyheter', 'Nytt från Solkatten och från Sverak.', kropp, '/nyheter/', avd))
    sitemap.append('/nyheter/')
    for n in nyheter:
        kropp = f'''<div class="bredd sida">
{brodsmulor([("Hem", "/"), ("Nyheter", "/nyheter/"), (n["meta"]["titel"], n["url"])])}
<article class="sida-text">
<h1>{n["meta"]["titel"]}</h1>
<p class="datum"><time datetime="{n["datum"].isoformat()}">{svdatum(n["datum"])}</time></p>
<p class="ingress">{n["meta"].get("ingress", "")}</p>
{n["html"]}
</article>
</div>'''
        skriv(n['url'], skal(n['meta']['titel'], n['meta'].get('ingress') or text_av(n['html']), kropp, n['url'], avd))
        sitemap.append(n['url'])

    # Aktiviteter
    lista = ''.join(kort(a['meta']['titel'], a['url'], f'<span class="datum">{svdatum(a["datum"])}{" · " + a["meta"]["plats"] if a["meta"].get("plats") else ""}</span><br>{a["meta"].get("ingress", "")}') for a in kommande)
    kropp = f'''<div class="bredd sida">
{brodsmulor([("Hem", "/"), ("Aktiviteter", "/aktiviteter/")])}
<h1>Aktiviteter</h1>
<p class="ingress sida-text">Utställningar, föreläsningar och träffar som är på gång i Solkatten.</p>
{f'<ul class="kortlista undersidor">{lista}</ul>' if lista else '<p class="tom">Inga aktiviteter är inplanerade just nu. Har du en idé? Mejla <a href="mailto:aktivitetsgrupp@solkattenskelleftea.se">aktivitetsgruppen</a>.</p>'}
</div>'''
    skriv('/aktiviteter/', skal('Aktiviteter', 'Utställningar, föreläsningar och träffar i Solkatten.', kropp, '/aktiviteter/', avd))
    sitemap.append('/aktiviteter/')
    for a in aktiviteter:
        passerad = a['datum'] < IDAG
        kropp = f'''<div class="bredd sida">
{brodsmulor([("Hem", "/"), ("Aktiviteter", "/aktiviteter/"), (a["meta"]["titel"], a["url"])])}
<article class="sida-text">
<h1>{a["meta"]["titel"]}</h1>
<p class="datum"><time datetime="{a["datum"].isoformat()}">{svdatum(a["datum"])}</time>{" · " + a["meta"]["plats"] if a["meta"].get("plats") else ""}{" · Har redan varit" if passerad else ""}</p>
<p class="ingress">{a["meta"].get("ingress", "")}</p>
{a["html"]}
</article>
</div>'''
        skriv(a['url'], skal(a['meta']['titel'], a['meta'].get('ingress') or text_av(a['html']), kropp, a['url'], avd, noindex=passerad))
        if not passerad:
            sitemap.append(a['url'])

    # 404
    kropp = '''<div class="bredd sida sida-text">
<h1>Sidan finns inte</h1>
<p class="ingress">Sidan du letar efter kan ha flyttats när vi gjorde om webbplatsen.</p>
<p><a class="knapp knapp-gul" href="/">Till startsidan</a></p>
<p>Hittar du inte det du söker? <a href="/kontakt/">Kontakta oss</a>.</p>
</div>'''
    with open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8') as f:
        f.write(skal('Sidan finns inte', 'Sidan finns inte.', kropp, '/404.html', avd, noindex=True))

    # sitemap och robots
    with open(os.path.join(DIST, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in sitemap:
            f.write(f'  <url><loc>{DOMAN}{u}</loc><lastmod>{IDAG.isoformat()}</lastmod></url>\n')
        f.write('</urlset>\n')
    with open(os.path.join(DIST, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(f'User-agent: *\nDisallow: /medlem/rabattkoder/\n\nSitemap: {DOMAN}/sitemap.xml\n')

    # Lösenordsskyddad medlemssida (läggs i egen mapp, laddas upp separat till /medlem/rabattkoder/)
    if not BAS:
        fil = os.path.join(INN, 'medlemssida', 'rabattkoder.html')
        if os.path.exists(fil):
            mm, mhtml = las(fil)
            if os.path.exists(DIST_MEDLEM):
                shutil.rmtree(DIST_MEDLEM)
            mal = os.path.join(DIST_MEDLEM, 'medlem', 'rabattkoder')
            os.makedirs(mal)
            kropp = f'''<div class="bredd sida">
{brodsmulor([("Hem", "/"), ("Medlem", "/medlem/"), (mm["titel"], "/medlem/rabattkoder/")])}
<div class="sida-text">
<h1>{mm["titel"]}</h1>
{mhtml}
</div>
</div>'''
            with open(os.path.join(mal, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(skal(mm['titel'], mm['beskrivning'], kropp, '/medlem/rabattkoder/', avd, noindex=True))
            for pdf in os.listdir(os.path.join(ROT, 'medlemskort')):
                if pdf.endswith('.pdf'):
                    shutil.copy(os.path.join(ROT, 'medlemskort', pdf), mal)

    if BAS or FORHANDSVISNING:
        for d, _, fs in os.walk(DIST):
            for f in fs:
                if not f.endswith(('.html', '.css')):
                    continue
                fp = os.path.join(d, f)
                t = open(fp, encoding='utf-8').read()
                if BAS:
                    t = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{BAS}/', t)
                    t = t.replace('url("/', f'url("{BAS}/')
                if FORHANDSVISNING and f.endswith('.html'):
                    t = t.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
                open(fp, 'w', encoding='utf-8').write(t)
        with open(os.path.join(DIST, 'robots.txt'), 'w', encoding='utf-8') as f:
            f.write('User-agent: *\nDisallow: /\n')
        print(f'Länkar börjar med "{BAS or "/"}". Sidan är stängd för Google (noindex och robots.txt).')
    print(f'Klart! {len(sitemap)} sidor i sitemap, {len(nyheter)} nyheter, {len(kommande)} kommande aktiviteter.')
    print('Webbplatsen ligger i mappen dist/')

if __name__ == '__main__':
    main()
