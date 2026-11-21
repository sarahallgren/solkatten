#!/bin/sh
# Hämtar dokument och vinnarbilder från den gamla one.com-webbplatsen innan den byts ut.
# Körs automatiskt av GitHub om filerna saknas. Kan också köras själv:  sh hamta-gamla-filer.sh
cd "$(dirname "$0")"
G=https://www.solkattenskelleftea.se/onewebmedia
mkdir -p statiskt/dokument statiskt/bilder/km2026
hamta() { [ -s "$2" ] || curl -fsSL "$G/$1" -o "$2" || echo "Kunde inte hämta $1"; }
hamta "Solkattens%20stadgar.pdf"                        statiskt/dokument/solkattens-stadgar.pdf
hamta "SOLResultat_l%C3%B6rdag_2016-05-14Rev1.pdf"      statiskt/dokument/resultat-2016-05-14.pdf
hamta "SOLResultat_s%C3%B6ndag_2016-05-15.pdf"          statiskt/dokument/resultat-2016-05-15.pdf
hamta "Resultat_2015-05-23_Ver%202.pdf"                 statiskt/dokument/resultat-2015-05-23.pdf
hamta "Resultat_2015-05-24.pdf"                         statiskt/dokument/resultat-2015-05-24.pdf
hamta "SolResultat%20l%C3%B6rdag%202014.pdf"            statiskt/dokument/resultat-2014-05-17.pdf
hamta "SolResultat%20s%C3%B6ndag%202014.pdf"            statiskt/dokument/resultat-2014-05-18.pdf
hamta "Klintskogensgretaklubbm%C3%A4stare2026.JPG"      statiskt/bilder/km2026/klubbmastare.jpg
hamta "bkattungehane2026.jpg"                           statiskt/bilder/km2026/kattunge-hane.jpg
hamta "bkattungehona2026.jpg"                           statiskt/bilder/km2026/kattunge-hona.jpg
hamta "888618217_2044473096256838_4879513941457766560_n.jpg" statiskt/bilder/km2026/junior-hona.jpg
hamta "bvuxnahane2026.jpg"                              statiskt/bilder/km2026/vuxen-hane.jpg
hamta "bvuxnahona2026.jpg"                              statiskt/bilder/km2026/vuxen-hona.jpg
hamta "bkastrathona2026.jpg"                            statiskt/bilder/km2026/kastrat-hona.jpg
hamta "bkastrathane2026.jpg"                            statiskt/bilder/km2026/kastrat-hane.jpg
hamta "B%C3%84STA%20UTSTR%C3%85LNINGkm2026.jpg"         statiskt/bilder/km2026/basta-utstralning.jpg
hamta "B%C3%84STA%20HUVUD%20KM2026.jpg"                 statiskt/bilder/km2026/basta-huvud.jpg
hamta "B%C3%84STA%20P%C3%84LSkm2026.jpg"                statiskt/bilder/km2026/basta-pals.jpg
hamta "b%C3%A4sta%20svans.jpeg"                         statiskt/bilder/km2026/basta-svans.jpg
ls -la statiskt/dokument statiskt/bilder/km2026
