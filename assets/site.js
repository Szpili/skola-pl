/* Role chips + szkoła/uczelnia nouns. Visitor strings are Polish. */
(function () {
  var COPY = {
    szkola: {
      lesson: 'lekcji',
      person: 'uczeń',
      adult: 'nauczyciel',
      place: 'szkoła'
    },
    uczelnia: {
      lesson: 'zajęć',
      person: 'student',
      adult: 'wykładowca',
      place: 'uczelnia'
    }
  };
  var ROLES = {
    uczen: {
      track: 'szkola',
      you: 'Skanujesz kod QR po lekcji i stukasz w jedno pole kwadratu. Bez konta, bez nazwiska, kilka sekund.',
      then: 'Nauczyciel widzi obrazek klasy, nie Twoje imię. Jedno kliknięcie nic nie znaczy — liczy się, gdy ktoś odpowiada tak samo wiele razy.'
    },
    rodzic: {
      track: 'szkola',
      you: 'Dziecko głosuje bez logowania. Głosy nie mają trwałego identyfikatora, więc nie powstaje lista „kto co kliknął”.',
      then: 'Szkoła może pokazać obrazek klasy. Domyślnie nie da się śledzić jednego dziecka w czasie — to świadomy kompromis, nie brak funkcji.'
    },
    nauczyciel: {
      track: 'szkola',
      you: 'Drukujesz arkusz z kodem QR na przedmiot albo na jedną lekcję. Po lekcji patrzysz na kwadrat.',
      then: 'Kolor mówi o nastawieniu, wysokość o nauce. Lewy górny róg (uczą się, nie lubią) to sygnał do pytania — nie do kary.'
    },
    dyrektor: {
      track: 'szkola',
      you: 'Ustalasz częstotliwość: po lekcji, raz dziennie albo raz w semestrze. Patrzą tu dyrektor i pedagog.',
      then: 'Widać, gdzie warto zapytać, co się dzieje. To nie jest narzędzie do rozliczania nauczycieli. Pojedynczy zły głos to szum.'
    },
    student: {
      track: 'uczelnia',
      you: 'Po zajęciach stukasz w jedno pole: ile się nauczyłem i na ile mi się podobało. Nic więcej.',
      then: 'Wykładowca i osoba od jakości kształcenia widzą rozkład, nie jedną gwiazdkę. Wymagające zajęcia, z których dużo wynosisz, nie zlewają się ze słabymi.'
    }
  };

  function apply(roleId) {
    var role = ROLES[roleId] || ROLES.uczen;
    var track = COPY[role.track];
    document.querySelectorAll('[data-role]').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-role') === roleId);
    });
    document.querySelectorAll('[data-track]').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-track') === role.track);
    });
    var box = document.getElementById('role-copy');
    if (box) {
      box.innerHTML =
        '<p><span class="k">Ty</span><br>' + role.you + '</p>' +
        '<p><span class="k">Co potem widać</span><br>' + role.then + '</p>';
    }
    document.querySelectorAll('[data-noun]').forEach(function (el) {
      var key = el.getAttribute('data-noun');
      if (track[key]) el.textContent = track[key];
    });
  }

  document.querySelectorAll('[data-role]').forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-role')); });
  });
  document.querySelectorAll('[data-track]').forEach(function (b) {
    b.addEventListener('click', function () {
      var track = b.getAttribute('data-track');
      var first = Object.keys(ROLES).find(function (k) { return ROLES[k].track === track; });
      apply(first);
    });
  });
  apply('uczen');
})();
