#!/bin/sh
# Hämtar bilder och typsnitt från WordPress-testsidan till mappen statiskt/.
# Kör en gång, medan ny.solkattenskelleftea.se fortfarande finns:  sh hamta-bilder.sh
set -e
cd "$(dirname "$0")"
K=https://ny.solkattenskelleftea.se
mkdir -p statiskt/bilder statiskt/fonter
curl -fsSL "$K/wp-content/uploads/2026/11/logo-fife.jpg" -o statiskt/bilder/logo-fife.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/logo-kopakatt.png" -o statiskt/bilder/logo-kopakatt.png
curl -fsSL "$K/wp-content/uploads/2026/11/logo-id-registret.png" -o statiskt/bilder/logo-id-registret.png
curl -fsSL "$K/wp-content/uploads/2026/11/logo-mina-katter.png" -o statiskt/bilder/logo-mina-katter.png
curl -fsSL "$K/wp-content/uploads/2026/11/logo-sverak.png" -o statiskt/bilder/logo-sverak.png
curl -fsSL "$K/wp-content/uploads/2026/11/katt-topp-om.jpg" -o statiskt/bilder/katt-topp-om.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/katt-topp-medlem.jpg" -o statiskt/bilder/katt-topp-medlem.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/katt-topp-utstallning.jpg" -o statiskt/bilder/katt-topp-utstallning.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/katt-topp-fakta.jpg" -o statiskt/bilder/katt-topp-fakta.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/katt-topp-skaffa.jpg" -o statiskt/bilder/katt-topp-skaffa.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/katt-kattmamma.jpg" -o statiskt/bilder/katt-kattmamma.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/katt-hero.jpg" -o statiskt/bilder/katt-hero.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/sponsor-4pets.png" -o statiskt/bilder/sponsor-4pets.png
curl -fsSL "$K/wp-content/uploads/2026/11/sponsor-langford.png" -o statiskt/bilder/sponsor-langford.png
curl -fsSL "$K/wp-content/uploads/2026/11/sponsor-bjorkis.jpg" -o statiskt/bilder/sponsor-bjorkis.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/sponsor-supercat.jpg" -o statiskt/bilder/sponsor-supercat.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/sponsor-royal-canin.jpg" -o statiskt/bilder/sponsor-royal-canin.jpg
curl -fsSL "$K/wp-content/uploads/2026/11/sponsor-hills.png" -o statiskt/bilder/sponsor-hills.png
curl -fsSL "$K/wp-content/uploads/2026/11/sponsor-agria.png" -o statiskt/bilder/sponsor-agria.png
curl -fsSL "$K/wp-content/uploads/fonts/roboto-serif-latin.woff2" -o statiskt/fonter/roboto-serif-latin.woff2
curl -fsSL "$K/wp-content/uploads/fonts/roboto-serif-latin-ext.woff2" -o statiskt/fonter/roboto-serif-latin-ext.woff2
curl -fsSL "$K/wp-content/themes/twentytwentyfive/assets/fonts/manrope/Manrope-VariableFont_wght.woff2" -o statiskt/fonter/manrope.woff2
echo "Klart! Kör nu: python3 bygg.py"
