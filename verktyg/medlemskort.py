#!/usr/bin/env python3
"""Skapar Solkattens utskrivbara medlemskort (kreditkortsstorlek, 85,6 x 54 mm).

Kör:  python3 verktyg/medlemskort.py 2028
Kräver: pip install reportlab fonttools brotli   samt rsvg-convert (för logotypen)
Resultat: medlemskort/medlemskort-<år>.pdf
"""
import os, sys, subprocess, tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image

AR = sys.argv[1] if len(sys.argv) > 1 else '2027'
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTER = os.path.join(ROT, 'statiskt', 'fonter')
TMP = tempfile.mkdtemp()
MORK, GUL, DAMPAD, KANT = HexColor('#1C1A17'), HexColor('#F5B800'), HexColor('#57534E'), HexColor('#A8A29E')

def fast_font(woff, ut, axlar):
    f = TTFont(os.path.join(FONTER, woff))
    loc = {a.axisTag: a.defaultValue for a in f['fvar'].axes}
    loc.update(axlar)
    i = instancer.instantiateVariableFont(f, loc)
    i.flavor = None
    p = os.path.join(TMP, ut)
    i.save(p)
    return p

pdfmetrics.registerFont(RLFont('Rubrik', fast_font('roboto-serif-latin.woff2', 'r.ttf', {'wght': 900, 'wdth': 50})))
pdfmetrics.registerFont(RLFont('Brod', fast_font('manrope.woff2', 'm5.ttf', {'wght': 500})))
pdfmetrics.registerFont(RLFont('BrodFet', fast_font('manrope.woff2', 'm8.ttf', {'wght': 800})))

# Vit logotyp till framsidan
svart = os.path.join(TMP, 'logo.png')
subprocess.run(['rsvg-convert', '-w', '1000', os.path.join(ROT, 'statiskt', 'bilder', 'solkatten-logotyp.svg'), '-o', svart], check=True)
im = Image.open(svart).convert('RGBA')
vit = Image.new('RGBA', im.size, (255, 255, 255, 0))
vit.putalpha(im.split()[3])
vit_p = os.path.join(TMP, 'logo-vit.png')
vit.save(vit_p)
svart_liten = svart

os.makedirs(os.path.join(ROT, 'medlemskort'), exist_ok=True)
ut = os.path.join(ROT, 'medlemskort', f'medlemskort-{AR}.pdf')
c = canvas.Canvas(ut, pagesize=A4)
c.setTitle(f'Medlemskort Solkatten {AR}')
c.setAuthor('Solkatten Skellefteå kattklubb')
c.setSubject('Utskrivbart medlemskort i kreditkortsstorlek')
B, H = 85.6 * mm, 54 * mm
sw, sh = A4
x0 = 25 * mm
y0 = sh - 80 * mm - H

# Instruktioner
c.setFillColor(MORK)
c.setFont('Rubrik', 26)
c.drawString(x0, sh - 30 * mm, f'Medlemskort {AR}')
c.setFont('Brod', 11)
rader = [
    '1. Skriv ditt namn och medlemsnummer i fälten på kortet (eller för hand efter utskrift).',
    '2. Skriv ut i verklig storlek (100 %). Välj inte "Anpassa till sida".',
    '3. Klipp ut kortet längs den tunna grå linjen.',
    '4. Laminera gärna. Visa kortet i butiken för att få rabatten.',
]
for i, r in enumerate(rader):
    c.drawString(x0, sh - 42 * mm - i * 6.5 * mm, r)

# ---- Kortet: en sida, vit bakgrund, gul rand ----
c.saveState()
klipp = c.beginPath()
klipp.roundRect(x0, y0, B, H, 3 * mm)
c.clipPath(klipp, stroke=0, fill=0)
c.setFillColor(GUL)
c.rect(x0, y0 + H - 3 * mm, B, 3 * mm, stroke=0, fill=1)
c.restoreState()

pad = 5 * mm
lh = 19 * mm
c.drawImage(svart_liten, x0 + pad, y0 + 29 * mm, width=lh * 253.75 / 263.75, height=lh, mask='auto')
tx = x0 + 31 * mm
c.setFillColor(DAMPAD)
c.setFont('BrodFet', 7)
c.drawString(tx, y0 + 43 * mm, 'MEDLEMSKORT')
c.setFillColor(MORK)
c.setFont('Rubrik', 30)
c.drawString(tx, y0 + 33 * mm, AR)
c.setFont('Brod', 7)
c.drawString(tx, y0 + 28.5 * mm, 'Solkatten Skellefteå kattklubb')

c.setFillColor(DAMPAD)
c.setFont('BrodFet', 6)
c.drawString(x0 + pad, y0 + 23.5 * mm, 'NAMN')
c.drawString(x0 + pad, y0 + 12.5 * mm, 'MEDLEMSNUMMER')
c.drawString(x0 + 47 * mm, y0 + 12.5 * mm, 'GILTIGT TILL OCH MED')
c.setStrokeColor(KANT)
c.setLineWidth(0.5)
c.line(x0 + pad, y0 + 16.5 * mm, x0 + B - pad, y0 + 16.5 * mm)
c.line(x0 + pad, y0 + 6.5 * mm, x0 + 42 * mm, y0 + 6.5 * mm)
c.setFillColor(MORK)
c.setFont('BrodFet', 8.5)
c.drawString(x0 + 47 * mm, y0 + 7.5 * mm, f'31 december {AR}')
form = c.acroForm
form.textfield(name='namn', tooltip='Namn', x=x0 + pad, y=y0 + 17 * mm, width=B - 2 * pad, height=5.5 * mm,
               fontName='Helvetica-Bold', fontSize=10, borderWidth=0, fillColor=white, textColor=MORK, forceBorder=False)
form.textfield(name='medlemsnummer', tooltip='Medlemsnummer', x=x0 + pad, y=y0 + 7 * mm, width=37 * mm, height=5 * mm,
               fontName='Helvetica-Bold', fontSize=10, borderWidth=0, fillColor=white, textColor=MORK, forceBorder=False)
c.setFillColor(DAMPAD)
c.setFont('Brod', 5.5)
c.drawString(x0 + pad, y0 + 2.6 * mm, 'Ansluten till Sverak och FIFe  ·  solkattenskelleftea.se')

# Klipplinje
c.setStrokeColor(KANT)
c.setLineWidth(0.4)
c.roundRect(x0, y0, B, H, 3 * mm, stroke=1, fill=0)
c.setFillColor(DAMPAD)
c.setFont('Brod', 8)
c.drawString(x0, y0 - 6 * mm, 'Klipp längs den grå linjen')
c.showPage()
c.save()
print('Klart:', ut)
