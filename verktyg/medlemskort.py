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
x0 = (sw - 2 * B) / 2
y0 = sh - 40 * mm - 70 * mm - H

# Instruktioner
c.setFillColor(MORK)
c.setFont('Rubrik', 26)
c.drawString(x0, sh - 30 * mm, f'Medlemskort {AR}')
c.setFont('Brod', 11)
rader = [
    '1. Skriv ditt namn och medlemsnummer i fälten på kortet (eller för hand efter utskrift).',
    '2. Skriv ut i verklig storlek (100 %). Välj inte "Anpassa till sida".',
    '3. Klipp ut längs den yttre linjen och vik på den streckade mittlinjen.',
    '4. Tejpa ihop eller laminera. Visa kortet i butiken för att få rabatten.',
]
for i, r in enumerate(rader):
    c.drawString(x0, sh - 42 * mm - i * 6.5 * mm, r)

# ---- Framsida (vänster) ----
c.saveState()
klipp = c.beginPath()
klipp.roundRect(x0, y0, 2 * B, H, 3 * mm)
c.clipPath(klipp, stroke=0, fill=0)
c.setFillColor(MORK)
c.rect(x0, y0, B, H, stroke=0, fill=1)
c.setFillColor(GUL)
c.rect(x0, y0, B, 2.2 * mm, stroke=0, fill=1)
lh = 30 * mm
c.drawImage(vit_p, x0 + 6 * mm, y0 + (H - lh) / 2 + 2 * mm, width=lh * 253.75 / 263.75, height=lh, mask='auto')
tx = x0 + 42 * mm
c.setFillColor(GUL)
c.setFont('BrodFet', 7.5)
c.drawString(tx, y0 + 38 * mm, 'MEDLEMSKORT')
c.setFont('Rubrik', 40)
c.drawString(tx, y0 + 24 * mm, AR)
c.setFillColor(white)
c.setFont('BrodFet', 8)
c.drawString(tx, y0 + 15 * mm, 'Solkatten')
c.setFont('Brod', 7)
c.drawString(tx, y0 + 11 * mm, 'Skellefteå kattklubb')

# ---- Baksida (höger) ----
bx = x0 + B
c.setFillColor(white)
c.rect(bx, y0, B, H, stroke=0, fill=1)
c.setFillColor(GUL)
c.rect(bx, y0 + H - 2.2 * mm, B, 2.2 * mm, stroke=0, fill=1)
c.restoreState()
pad = 6 * mm
c.setFillColor(DAMPAD)
c.setFont('BrodFet', 6.5)
c.drawString(bx + pad, y0 + 44 * mm, 'NAMN')
c.drawString(bx + pad, y0 + 30 * mm, 'MEDLEMSNUMMER')
c.setStrokeColor(KANT)
c.setLineWidth(0.5)
for yy in (37 * mm, 23 * mm):
    c.line(bx + pad, y0 + yy, bx + B - pad, y0 + yy)
form = c.acroForm
form.textfield(name='namn', tooltip='Namn', x=bx + pad, y=y0 + 37.5 * mm, width=B - 2 * pad, height=5.5 * mm,
               fontName='Helvetica-Bold', fontSize=10, borderWidth=0, fillColor=white, textColor=MORK, forceBorder=False)
form.textfield(name='medlemsnummer', tooltip='Medlemsnummer', x=bx + pad, y=y0 + 23.5 * mm, width=B - 2 * pad, height=5.5 * mm,
               fontName='Helvetica-Bold', fontSize=10, borderWidth=0, fillColor=white, textColor=MORK, forceBorder=False)
c.setFillColor(MORK)
c.setFont('BrodFet', 8)
c.drawString(bx + pad, y0 + 14 * mm, f'Giltigt till och med 31 december {AR}')
c.setFillColor(DAMPAD)
c.setFont('Brod', 6.5)
c.drawString(bx + pad, y0 + 9.5 * mm, 'Ansluten till Sverak och FIFe')
c.drawString(bx + pad, y0 + 5.5 * mm, 'solkattenskelleftea.se')
c.drawImage(svart_liten, bx + B - pad - 11 * mm, y0 + 4 * mm, width=11 * mm * 253.75 / 263.75, height=11 * mm, mask='auto')

# Klipp- och viklinjer
c.setStrokeColor(KANT)
c.setLineWidth(0.4)
c.roundRect(x0, y0, 2 * B, H, 3 * mm, stroke=1, fill=0)
c.setDash(2, 2)
c.line(x0 + B, y0 - 4 * mm, x0 + B, y0 + H + 4 * mm)
c.setDash()
c.setFillColor(DAMPAD)
c.setFont('Brod', 8)
c.drawCentredString(x0 + B, y0 + H + 6 * mm, 'vik här')
c.drawString(x0, y0 - 8 * mm, 'Klipp längs den yttre linjen')
c.showPage()
c.save()
print('Klart:', ut)
