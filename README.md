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
| `innehall/aktiviteter/` | Aktiviteter – visas på startsidan och under Aktiviteter tills datumet har passerat |
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

### Lägga in en aktivitet
Samma sak i `innehall/aktiviteter/`, med `datum:` = dagen då aktiviteten sker och gärna `plats:`.
Aktiviteten syns på startsidan under *På gång* fram till datumet. Bygg om sidan någon gång efteråt så försvinner den.

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

## Medlemsrabatter (lösenordsskydd)

Sidan `/medlem/medlemsrabatter/` ska skyddas med lösenord **på servern**. Lösenord i JavaScript är inget riktigt skydd.
Sidan syns inte i menyn, i Google eller i webbplatskartan, men den är **inte** skyddad förrän stegen nedan är gjorda.

1. Skapa lösenordsfilen `.htpasswd` (användare `medlem`), till exempel med en htpasswd-generator.
   Lägg den **utanför** webbplatsens mappar om one.com tillåter det.
2. Lägg en fil `.htaccess` i `dist/medlem/medlemsrabatter/` efter bygget:
   ```
   AuthType Basic
   AuthName "Solkattens medlemssida"
   AuthUserFile /FULLSTÄNDIG/SÖKVÄG/TILL/.htpasswd
   Require valid-user
   ```
   Den fullständiga sökvägen får du av one.com:s support.
3. Byt lösenord varje år den 1 januari och skicka det nya till medlemmarna.

## Vid lanseringen

- [ ] Kör `hamta-bilder` och bygg sidan en sista gång
- [ ] Ladda upp innehållet i `webbplats/` inklusive `.htaccess` till solkattenskelleftea.se
- [ ] Testa några gamla adresser, t.ex. `/Medlemskap/` och `/Solkatten/Styrelse` – de ska leda till de nya sidorna
- [ ] Skicka in `https://solkattenskelleftea.se/sitemap.xml` i Google Search Console
- [ ] Skydda medlemsrabatterna (se ovan)
- [ ] Stäng WordPress-testsidan och peka `ny.solkattenskelleftea.se` till huvudadressen

## Om någon annan tar över

Allt som behövs finns i den här mappen. Spara den i Git (till exempel GitHub) så finns varje version kvar.
Inloggningen till one.com och den här mappen är de två saker en ny webbansvarig behöver få.
