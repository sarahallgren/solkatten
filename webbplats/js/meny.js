// Meny: öppna/stäng mobilmenyn och undermenyer. Fungerar med tangentbord och skärmläsare.
(function () {
  var knapp = document.querySelector('.meny-knapp');
  var meny = document.getElementById('huvudmeny');
  if (knapp && meny) {
    knapp.addEventListener('click', function () {
      var oppen = knapp.getAttribute('aria-expanded') === 'true';
      knapp.setAttribute('aria-expanded', String(!oppen));
      meny.classList.toggle('oppen', !oppen);
    });
  }
  document.querySelectorAll('.undermeny-knapp').forEach(function (b) {
    b.addEventListener('click', function () {
      var lista = document.getElementById(b.getAttribute('aria-controls'));
      var oppen = b.getAttribute('aria-expanded') === 'true';
      b.setAttribute('aria-expanded', String(!oppen));
      lista.classList.toggle('oppen', !oppen);
    });
  });
  function stangUndermenyer(utom) {
    document.querySelectorAll('.undermeny-knapp[aria-expanded="true"]').forEach(function (b) {
      if (b === utom) return;
      b.setAttribute('aria-expanded', 'false');
      document.getElementById(b.getAttribute('aria-controls')).classList.remove('oppen');
    });
  }
  // Bara en undermeny öppen åt gången
  document.querySelectorAll('.undermeny-knapp').forEach(function (b) {
    b.addEventListener('click', function () { stangUndermenyer(b); });
  });
  // Klick utanför menyn stänger öppna undermenyer
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.huvudmeny')) stangUndermenyer(null);
  });
  // Esc stänger den undermeny eller meny man är i och flyttar tillbaka fokus till knappen
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var oppenUnder = document.querySelector('.undermeny-knapp[aria-expanded="true"]');
    if (oppenUnder) {
      stangUndermenyer(null);
      oppenUnder.focus();
      return;
    }
    if (knapp && knapp.getAttribute('aria-expanded') === 'true') {
      knapp.setAttribute('aria-expanded', 'false');
      meny.classList.remove('oppen');
      knapp.focus();
    }
  });
  // Sidhuvudet får vit bakgrund och skugga när man har scrollat
  var huvud = document.querySelector('.sidhuvud');
  if (huvud) {
    var kolla = function () { huvud.classList.toggle('rullad', window.scrollY > 20); };
    window.addEventListener('scroll', kolla, { passive: true });
    kolla();
  }
})();
