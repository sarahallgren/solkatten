# Hämtar bilder och typsnitt från WordPress-testsidan till mappen statiskt\
# Kör i PowerShell, medan ny.solkattenskelleftea.se fortfarande finns:  .\hamta-bilder.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$K = "https://ny.solkattenskelleftea.se"
New-Item -ItemType Directory -Force statiskt\bilder, statiskt\fonter | Out-Null
Invoke-WebRequest "$K/wp-content/uploads/2026/11/logo-fife.jpg" -OutFile statiskt\bilder\logo-fife.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/logo-kopakatt.png" -OutFile statiskt\bilder\logo-kopakatt.png
Invoke-WebRequest "$K/wp-content/uploads/2026/11/logo-id-registret.png" -OutFile statiskt\bilder\logo-id-registret.png
Invoke-WebRequest "$K/wp-content/uploads/2026/11/logo-mina-katter.png" -OutFile statiskt\bilder\logo-mina-katter.png
Invoke-WebRequest "$K/wp-content/uploads/2026/11/logo-sverak.png" -OutFile statiskt\bilder\logo-sverak.png
Invoke-WebRequest "$K/wp-content/uploads/2026/11/katt-topp-om.jpg" -OutFile statiskt\bilder\katt-topp-om.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/katt-topp-medlem.jpg" -OutFile statiskt\bilder\katt-topp-medlem.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/katt-topp-utstallning.jpg" -OutFile statiskt\bilder\katt-topp-utstallning.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/katt-topp-fakta.jpg" -OutFile statiskt\bilder\katt-topp-fakta.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/katt-topp-skaffa.jpg" -OutFile statiskt\bilder\katt-topp-skaffa.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/katt-kattmamma.jpg" -OutFile statiskt\bilder\katt-kattmamma.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/katt-hero.jpg" -OutFile statiskt\bilder\katt-hero.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/sponsor-4pets.png" -OutFile statiskt\bilder\sponsor-4pets.png
Invoke-WebRequest "$K/wp-content/uploads/2026/11/sponsor-langford.png" -OutFile statiskt\bilder\sponsor-langford.png
Invoke-WebRequest "$K/wp-content/uploads/2026/11/sponsor-bjorkis.jpg" -OutFile statiskt\bilder\sponsor-bjorkis.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/sponsor-supercat.jpg" -OutFile statiskt\bilder\sponsor-supercat.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/sponsor-royal-canin.jpg" -OutFile statiskt\bilder\sponsor-royal-canin.jpg
Invoke-WebRequest "$K/wp-content/uploads/2026/11/sponsor-hills.png" -OutFile statiskt\bilder\sponsor-hills.png
Invoke-WebRequest "$K/wp-content/uploads/2026/11/sponsor-agria.png" -OutFile statiskt\bilder\sponsor-agria.png
Invoke-WebRequest "$K/wp-content/uploads/fonts/roboto-serif-latin.woff2" -OutFile statiskt\fonter\roboto-serif-latin.woff2
Invoke-WebRequest "$K/wp-content/uploads/fonts/roboto-serif-latin-ext.woff2" -OutFile statiskt\fonter\roboto-serif-latin-ext.woff2
Invoke-WebRequest "$K/wp-content/themes/twentytwentyfive/assets/fonts/manrope/Manrope-VariableFont_wght.woff2" -OutFile statiskt\fonter\manrope.woff2
Write-Host "Klart! Kör nu: python bygg.py"
