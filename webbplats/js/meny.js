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
  // Esc stänger allt
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('[aria-expanded="true"]').forEach(function (b) {
      b.setAttribute('aria-expanded', 'false');
      var id = b.getAttribute('aria-controls');
      if (id) document.getElementById(id).classList.remove('oppen');
    });
    if (knapp) knapp.focus();
  });
})();
