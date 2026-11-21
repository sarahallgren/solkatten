# Solkatten Skellefteå kattklubb – webbplatsen

Statisk HTML-webbplats för solkattenskelleftea.se. Inga databaser, inga tillägg, inget att uppdatera.
Webbansvarig skriver in texterna som styrelsen skickar, bygger om sidan och laddar upp den.

## Den färdiga webbplatsen

Mappen **`webbplats/`** är den färdiga sidan med alla bilder. Den byggs automatiskt på GitHub varje gång något ändras.
Det är **innehållet i den mappen** som laddas upp till one.com. Du behöver inte köra något själv.

Förhandsvisning: https://sarahallgren.github.io/solkatten/

## Bygga på egen dator (valfritt)

1. **Hämta bilder och typsnitt** (bara en gång, medan WordPress-testsidan ny.solkattenskelleftea.se finns kvar):
   - Windows: högerklicka på `hamta-bilder.ps1` → *Kör med PowerShell*
   - Mac/Linux: `sh hamta-bilder.sh`
2. **Bygg sidan:** `python3 bygg.py` (Windows: `python bygg.py`). Resultatet hamnar i mappen `dist/`.
3. **Titta på den lokalt:** `cd dist` och sedan `python3 -m http.server`. Öppna http://localhost:8000.

## Mappar

| Mapp / fil | Innehåll |
|---|---|
| `innehall/startsida.html` | Startsidan |
| `innehall/sidor/<avdelning>/index.html` | Huvudsidorna: Skaffa katt, Kattfakta, Utställning, Medlem, Om klubben, Kontakt |
| `innehall/sidor/<avdelning>/<sida>.html` | Undersidorna – sidans adress blir `/<avdelning>/<sida>/` |
| `innehall/nyheter/` | Nyheter, en fil per nyhet |
| `statiskt/` | Stilmall (`css/stil.css`), meny (`js/meny.js`), bilder, typsnitt och `.htaccess` |
| `bygg.py` | Bygger ihop allt till `dist/` – menyn och sidfoten finns här |
| `dist/` | Färdig webbplats som laddas upp. **Ändra aldrig här** – den skrivs över vid varje bygge |

## Vanliga uppgifter

### Lägga in en nyhet
Skapa en fil i `innehall/nyheter/` som heter `ÅÅÅÅ-MM-DD-kort-namn.html`, till exempel `2027-02-17-kattens-dag.html`:

```html
<!--
titel: Så firade vi Kattens dag
datum: 2027-02-17
ingress: En eller två meningar som syns i nyhetslistan.
-->
<p>Själva texten. Vanlig HTML: <strong>fet</strong>, <a href="/kontakt/">länkar</a>, listor.</p>
```

### Något som ska hända (aktivitet)
Skriv en vanlig nyhet och lägg till `när:` (dagen det händer) och gärna `plats:`:
```
<!--
titel: Kattens dag på Stadsbiblioteket
datum: 2027-01-20
när: 2027-02-17
plats: Stadsbiblioteket, Skellefteå
ingress: Kom och träffa katter och kattägare.
-->
```
Fram till dagen visas nyheten först på startsidan och under *På gång* på sidan Nyheter.
Sidan byggs om varje natt, så efteråt hamnar den automatiskt bland de vanliga nyheterna.

### Ändra en sida
Öppna filen i `innehall/sidor/…`, ändra texten, bygg om och ladda upp.
Gula rutor med `data-todo="1"` är påminnelser om text som saknas – ta bort hela stycket när texten är på plats.

### Ny undersida
Skapa en ny fil i rätt avdelningsmapp, till exempel `innehall/sidor/kattfakta/pälsvård.html` – men använd bara a–z, siffror och bindestreck i filnamnet (`palsvard.html`).
`ordning:` bestämmer platsen i menyn och `beskrivning:` blir texten på länkkortet. Menyn och länkkorten uppdateras automatiskt.

### Byta sponsor eller logotyp
Lägg bilden i `statiskt/bilder/` och ändra listan under *Samarbeten* i `bygg.py` (sök efter `sponsor-`).

### Bilder
- Förminska till cirka 1600 px bredd innan de läggs i `statiskt/bilder/`.
- Skriv alltid en `alt`-text som beskriver vad bilden visar.
- Egna foton från medlemmar: fråga om lov och skriv fotografens namn under bilden.

## Ladda upp till one.com

Ladda upp **innehållet** i `webbplats/` (inte själva mappen) till webbplatsens rotmapp, med SFTP eller one.com:s filhanterare.
Glöm inte den dolda filen `.htaccess` – den sköter omdirigeringar från de gamla adresserna, https och felsidan.

Inställningar för SFTP finns i one.com:s kontrollpanel under *SSH & SFTP*.

## Medlemsrabatter och rabattkoder (lösenordsskydd)

- **`/medlem/medlemsrabatter/`** är öppen för alla. Den visar förmånerna men **inga koder**.
- **`/medlem/rabattkoder/`** är lösenordsskyddad på servern. Där finns koderna och medlemskortet.
  Utan lösenord skickar servern inte sidan alls, så koderna syns inte i F12.

**Koderna får aldrig skrivas in i GitHub.** Repot är öppet för alla. I GitHub står bara `SKRIV-KODEN-HÄR`.

### Första gången (på one.com)
1. Ladda upp innehållet i mappen `medlemssida/` till webbplatsens rot, så att filerna hamnar i `medlem/rabattkoder/`.
2. Öppna **File Manager** i one.com:s kontrollpanel och gå till mappen `medlem/rabattkoder`.
3. Klicka på pilen bredvid **+ Upload** och välj **Secure directory**.
4. Markera filen **.htpasswd**, klicka på den stora filikonen till höger och skriv användarnamn (till exempel `medlem`) och lösenord. Spara.
5. Öppna `medlem/rabattkoder/index.html` i File Manager, byt ut `SKRIV-KODEN-HÄR` mot de riktiga koderna och spara.
6. Testa: öppna solkattenskelleftea.se/medlem/rabattkoder/ i ett privat fönster. En inloggningsruta ska visas.

### Sedan
- **Ny kod:** ändra direkt i `medlem/rabattkoder/index.html` på one.com.
- **Ladda inte upp `medlemssida/` igen**, då skrivs de riktiga koderna över. (Mappen `webbplats/` påverkar inte den skyddade sidan.)
- **Nytt medlemsår:** byt lösenord i `.htpasswd` och skapa ett nytt kort: `python3 verktyg/medlemskort.py 2028`.
  Ladda upp den nya PDF:en till `medlem/rabattkoder/` och ändra årtalet i länken på sidan.

## Vid lanseringen

- [ ] **Öppna för Google:** ändra `OPPEN_FOR_GOOGLE = False` till `True` i `bygg.py` (annars försvinner sidan ur Google när den gamla byts ut)
- [ ] Kör `hamta-bilder` och bygg sidan en sista gång
- [ ] Ladda upp innehållet i `webbplats/` inklusive `.htaccess` till solkattenskelleftea.se
- [ ] Testa några gamla adresser, t.ex. `/Medlemskap/` och `/Solkatten/Styrelse` – de ska leda till de nya sidorna
- [ ] Skicka in `https://solkattenskelleftea.se/sitemap.xml` i Google Search Console
- [ ] Skydda medlemsrabatterna (se ovan)
- [ ] Stäng WordPress-testsidan och peka `ny.solkattenskelleftea.se` till huvudadressen

## Om någon annan tar över

Allt som behövs finns i den här mappen. Spara den i Git (till exempel GitHub) så finns varje version kvar.
Inloggningen till one.com och den här mappen är de två saker en ny webbansvarig behöver få.
