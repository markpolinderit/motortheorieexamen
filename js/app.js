/* Motortheorie oefensite — vanilla JS, geen dependencies */
(function () {
  'use strict';

  var STORE_KEY = 'motortheorie_v1';
  var DATA = null;
  var app = document.getElementById('app');
  var session = null;      // actieve oefen- of examensessie
  var tickHandle = null;

  var CAT_LABEL = {
    gevaarherkenning: 'Gevaarherkenning',
    kennis: 'Kennis',
    inzicht: 'Inzicht'
  };

  /* ---------------- opslag ---------------- */

  function load() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) {}
    return { vragen: {}, examens: [] };
  }
  function save(p) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(p)); } catch (e) {}
  }
  var progress = load();

  function noteAnswer(id, good) {
    var v = progress.vragen[id] || { goed: 0, fout: 0 };
    if (good) v.goed++; else v.fout++;
    v.laatst = good ? 'goed' : 'fout';
    progress.vragen[id] = v;
    save(progress);
  }
  function foutenIds() {
    return Object.keys(progress.vragen).filter(function (id) {
      return progress.vragen[id].laatst === 'fout';
    });
  }

  /* ---------------- helpers ---------------- */

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function byCat(cat) {
    return DATA.vragen.filter(function (q) { return q.categorie === cat; });
  }
  function onderwerpen() {
    var map = {};
    DATA.vragen.forEach(function (q) {
      map[q.onderwerp] = (map[q.onderwerp] || 0) + 1;
    });
    return Object.keys(map).sort().map(function (k) { return { naam: k, aantal: map[k] }; });
  }
  function fmtTime(sec) {
    var m = Math.floor(sec / 60), s = sec % 60;
    return m + ':' + (s < 10 ? '0' : '') + s;
  }
  function stopTimer() {
    if (tickHandle) { clearInterval(tickHandle); tickHandle = null; }
  }

  /* Maakt een speelbare kopie van een vraag met geschudde antwoorden. */
  function prepare(q) {
    var idx = q.opties.map(function (_, i) { return i; });
    var order = shuffle(idx);
    return {
      id: q.id,
      categorie: q.categorie,
      onderwerp: q.onderwerp,
      vraag: q.vraag,
      afbeelding: q.afbeelding || null,
      opties: order.map(function (i) { return q.opties[i]; }),
      antwoord: order.indexOf(q.antwoord),
      uitleg: q.uitleg,
      keuze: null,
      vlag: false
    };
  }

  /* ---------------- router ---------------- */

  function route() {
    var h = (location.hash || '#/').replace(/^#/, '');
    var parts = h.split('/').filter(Boolean);
    document.querySelectorAll('.topnav a').forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('href') === '#/' + (parts[0] || ''));
    });
    window.scrollTo(0, 0);

    if (!DATA) return;
    if (parts.length === 0) return viewHome();
    if (parts[0] === 'oefenen') return viewOefenen(parts.slice(1));
    if (parts[0] === 'examen') return viewExamen(parts.slice(1));
    if (parts[0] === 'voortgang') return viewVoortgang();
    viewHome();
  }

  /* ---------------- views ---------------- */

  function viewHome() {
    stopTimer(); session = null;
    var ex = DATA.examen;
    var totaal = DATA.vragen.length;
    var laatste = progress.examens[progress.examens.length - 1];

    app.innerHTML =
      '<span class="tag">Rijbewijs A · A1 · A2</span>' +
      '<h1>Oefenen voor je motortheorie-examen</h1>' +
      '<p class="lead">' + totaal + ' oefenvragen over gevaarherkenning, verkeersregels en verkeersinzicht. ' +
      'Doe een volledige examensimulatie of oefen gericht per onderwerp.</p>' +
      '<div class="grid">' +
        tile('#/examen', '⏱️', 'Examensimulatie',
             ex.aantalVragen + ' vragen in ' + ex.tijdMinuten + ' minuten, of een los examen per onderdeel.') +
        tile('#/oefenen', '📚', 'Oefenen per onderwerp',
             'Vraag voor vraag oefenen met direct antwoord en uitleg.') +
        tile('#/voortgang', '📈', 'Mijn voortgang',
             'Zie je scores per categorie en oefen gericht je foute vragen opnieuw.') +
      '</div>' +
      (laatste
        ? '<div class="card"><strong>Laatste examen:</strong> ' + laatste.score + '/' + laatste.totaal +
          ' — <span class="' + (laatste.geslaagd ? 'verdict pass' : 'verdict fail') + '" style="font-size:1rem">' +
          (laatste.geslaagd ? 'geslaagd' : 'gezakt') + '</span>' +
          ' <span class="muted small">(' + new Date(laatste.datum).toLocaleDateString('nl-NL') + ')</span></div>'
        : '') +
      '<h2>Hoe ziet het echte examen eruit?</h2>' +
      '<div class="card small">' +
        '<p>Het CBR theorie-examen motor bestaat uit <strong>50 vragen</strong> die je in <strong>30 minuten</strong> beantwoordt. ' +
        'Je moet er <strong>41 of meer</strong> goed hebben om te slagen. Vooraf krijg je twee proefvragen die niet meetellen.</p>' +
        '<p class="muted">Deze site is oefenmateriaal en geen officieel CBR-product. De vragen zijn zelf geschreven en volgen de opzet van het examen.</p>' +
      '</div>';
  }

  function tile(href, ico, titel, tekst) {
    return '<a class="tile" href="' + href + '"><div class="ico">' + ico + '</div>' +
      '<h3>' + esc(titel) + '</h3><p>' + esc(tekst) + '</p></a>';
  }

  /* ----- oefenen ----- */

  function viewOefenen(rest) {
    if (rest.length === 0) { stopTimer(); return oefenMenu(); }
    var soort = decodeURIComponent(rest[0]);
    var waarde = rest[1] ? decodeURIComponent(rest[1]) : null;
    var set;

    if (soort === 'categorie') set = byCat(waarde);
    else if (soort === 'onderwerp') set = DATA.vragen.filter(function (q) { return q.onderwerp === waarde; });
    else if (soort === 'fouten') {
      var ids = foutenIds();
      set = DATA.vragen.filter(function (q) { return ids.indexOf(q.id) >= 0; });
      waarde = 'Mijn foute vragen';
    } else if (soort === 'alles') { set = DATA.vragen; waarde = 'Alle vragen'; }
    else return oefenMenu();

    if (!set.length) {
      app.innerHTML = '<h1>Niets te oefenen</h1><p class="lead">Er zijn geen vragen in deze selectie.</p>' +
        '<a class="btn" href="#/oefenen">Terug</a>';
      return;
    }

    if (!session || session.type !== 'oefen' || session.sleutel !== soort + '|' + waarde) {
      session = {
        type: 'oefen',
        sleutel: soort + '|' + waarde,
        titel: CAT_LABEL[waarde] || waarde,
        vragen: shuffle(set).map(prepare),
        i: 0,
        goed: 0
      };
    }
    renderOefenVraag();
  }

  function oefenMenu() {
    var fout = foutenIds().length;
    var cats = Object.keys(CAT_LABEL).map(function (c) {
      var n = byCat(c).length;
      return '<a class="tile" href="#/oefenen/categorie/' + c + '"><h3>' + CAT_LABEL[c] +
        '</h3><p>' + n + ' vragen</p></a>';
    }).join('');

    var onds = onderwerpen().map(function (o) {
      return '<a class="btn ghost small" href="#/oefenen/onderwerp/' + encodeURIComponent(o.naam) + '">' +
        esc(o.naam) + ' <span class="muted">(' + o.aantal + ')</span></a>';
    }).join(' ');

    app.innerHTML =
      '<h1>Oefenen</h1>' +
      '<p class="lead">Je krijgt na elke vraag meteen het juiste antwoord met uitleg.</p>' +
      '<div class="grid">' + cats + '</div>' +
      '<div class="btnrow">' +
        '<a class="btn primary" href="#/oefenen/alles">Alle ' + DATA.vragen.length + ' vragen door elkaar</a>' +
        (fout ? '<a class="btn" href="#/oefenen/fouten">Mijn foute vragen (' + fout + ')</a>' : '') +
      '</div>' +
      '<h2>Per onderwerp</h2><div class="btnrow">' + onds + '</div>';
  }

  function renderOefenVraag() {
    var s = session, q = s.vragen[s.i];
    var pct = Math.round((s.i / s.vragen.length) * 100);

    app.innerHTML =
      '<div class="quizbar"><div><span class="tag">' + esc(s.titel) + '</span></div>' +
      '<div class="muted small">Vraag ' + (s.i + 1) + ' van ' + s.vragen.length + ' · ' + s.goed + ' goed</div></div>' +
      '<div class="progress"><i style="width:' + pct + '%"></i></div>' +
      '<div class="card">' + questionHTML(q) + '<div id="fb"></div></div>' +
      '<div class="btnrow"><a class="btn ghost" href="#/oefenen">Stoppen</a></div>';

    bindOptions(function (keuze) {
      if (q.keuze !== null) return;
      q.keuze = keuze;
      var good = keuze === q.antwoord;
      if (good) s.goed++;
      noteAnswer(q.id, good);
      markOptions(q, true);
      document.getElementById('fb').innerHTML =
        '<div class="feedback ' + (good ? 'good' : 'bad') + '">' +
          '<h4>' + (good ? '✅ Goed' : '❌ Fout — juiste antwoord: ' + esc(q.opties[q.antwoord])) + '</h4>' +
          '<p class="small" style="margin:0">' + esc(q.uitleg) + '</p>' +
        '</div>' +
        '<div class="btnrow"><button class="btn primary" id="next">' +
          (s.i + 1 < s.vragen.length ? 'Volgende vraag' : 'Afronden') + '</button></div>';
      document.getElementById('next').onclick = function () {
        if (s.i + 1 < s.vragen.length) { s.i++; renderOefenVraag(); }
        else oefenKlaar();
      };
      document.getElementById('next').focus();
    });
  }

  function oefenKlaar() {
    var s = session;
    var pct = Math.round((s.goed / s.vragen.length) * 100);
    app.innerHTML =
      '<h1>Oefenronde afgerond</h1>' +
      '<div class="card score">' +
        '<div class="ring" style="--p:' + pct + '" data-label="' + pct + '%"></div>' +
        '<div><div class="verdict">' + s.goed + ' van de ' + s.vragen.length + ' goed</div>' +
        '<p class="muted">Onderdeel: ' + esc(s.titel) + '</p></div>' +
      '</div>' +
      '<div class="btnrow">' +
        '<a class="btn primary" href="#/oefenen">Nog een ronde</a>' +
        '<a class="btn" href="#/examen">Examensimulatie doen</a>' +
        '<a class="btn ghost" href="#/voortgang">Mijn voortgang</a>' +
      '</div>';
    session = null;
  }

  /* ----- examen ----- */

  function viewExamen(rest) {
    if (rest[0] === 'bezig' && session && session.type === 'examen') return renderExamenVraag();
    if (rest[0] === 'overzicht' && session && session.type === 'examen') return renderOverzicht();
    if (rest[0] === 'resultaat' && session && session.type === 'examen' && session.klaar) return renderExamenResultaat();
    stopTimer();
    session = null;
    var ex = DATA.examen;

    var deel = (DATA.deelexamens || []).map(function (d, i) {
      return '<div class="tile"><h3>' + (CAT_LABEL[d.categorie] || d.categorie) + '</h3>' +
        '<p>' + d.aantalVragen + ' vragen · ' + d.tijdMinuten + ' min · geslaagd vanaf ' + d.slaagnorm + '</p>' +
        '<div class="btnrow"><button class="btn" data-deel="' + i + '">Start</button></div></div>';
    }).join('');

    app.innerHTML =
      '<h1>Examensimulatie</h1>' +
      '<p class="lead">Zelfde opzet als het CBR-examen motor: alle onderdelen door elkaar.</p>' +
      '<div class="card">' +
        '<table><tbody>' +
          '<tr><th>Aantal vragen</th><td>' + ex.aantalVragen + '</td></tr>' +
          '<tr><th>Tijd</th><td>' + ex.tijdMinuten + ' minuten</td></tr>' +
          '<tr><th>Geslaagd vanaf</th><td>' + ex.slaagnorm + ' goede antwoorden</td></tr>' +
          '<tr><th>Verdeling</th><td>' +
            ex.verdeling.gevaarherkenning + ' gevaarherkenning · ' +
            ex.verdeling.kennis + ' kennis · ' + ex.verdeling.inzicht + ' inzicht</td></tr>' +
        '</tbody></table>' +
        '<p class="small muted" style="margin-bottom:0">Je kunt vragen markeren en later terugkomen. De uitslag met uitleg krijg je pas na het inleveren.</p>' +
      '</div>' +
      '<div class="btnrow"><button class="btn primary" id="start">Start het volledige examen</button></div>' +
      (deel
        ? '<h2>Examen per onderdeel</h2>' +
          '<p class="lead small">Één onderdeel onder examenomstandigheden, met eigen tijd en slaagnorm.</p>' +
          '<div class="grid">' + deel + '</div>'
        : '');

    document.getElementById('start').onclick = function () { startExamen(null); };
    app.querySelectorAll('[data-deel]').forEach(function (b) {
      b.onclick = function () { startExamen(DATA.deelexamens[parseInt(b.dataset.deel, 10)]); };
    });
  }

  /* cfg = null voor het volledige examen, anders een deelexamen uit DATA.deelexamens */
  function startExamen(cfg) {
    var gekozen = [], aantal, minuten, norm, titel;

    if (cfg) {
      aantal = Math.min(cfg.aantalVragen, byCat(cfg.categorie).length);
      minuten = cfg.tijdMinuten;
      norm = Math.min(cfg.slaagnorm, aantal);
      titel = 'Deelexamen ' + (CAT_LABEL[cfg.categorie] || cfg.categorie).toLowerCase();
      gekozen = shuffle(byCat(cfg.categorie)).slice(0, aantal);
    } else {
      var ex = DATA.examen;
      aantal = ex.aantalVragen; minuten = ex.tijdMinuten; norm = ex.slaagnorm;
      titel = 'Volledig examen';
      Object.keys(ex.verdeling).forEach(function (cat) {
        gekozen = gekozen.concat(shuffle(byCat(cat)).slice(0, ex.verdeling[cat]));
      });
      // aanvullen als een categorie te weinig vragen heeft
      if (gekozen.length < aantal) {
        var rest = DATA.vragen.filter(function (q) { return gekozen.indexOf(q) < 0; });
        gekozen = gekozen.concat(shuffle(rest).slice(0, aantal - gekozen.length));
      }
      gekozen = gekozen.slice(0, aantal);
    }

    session = {
      type: 'examen',
      titel: titel,
      norm: norm,
      cfg: cfg || null,
      vragen: shuffle(gekozen).map(prepare),
      i: 0,
      klaar: false,
      resterend: minuten * 60
    };
    startTimer();
    location.hash = '#/examen/bezig';
    renderExamenVraag();
  }

  function startTimer() {
    stopTimer();
    tickHandle = setInterval(function () {
      if (!session || session.type !== 'examen' || session.klaar) return stopTimer();
      session.resterend--;
      var el = document.getElementById('timer');
      if (el) {
        el.textContent = fmtTime(Math.max(0, session.resterend));
        el.className = 'timer' + (session.resterend <= 60 ? ' crit' : session.resterend <= 300 ? ' warn' : '');
      }
      if (session.resterend <= 0) { stopTimer(); leverIn(true); }
    }, 1000);
  }

  function renderExamenVraag() {
    var s = session, q = s.vragen[s.i];
    var beantwoord = s.vragen.filter(function (x) { return x.keuze !== null; }).length;

    app.innerHTML =
      '<div class="quizbar">' +
        '<div class="muted small"><span class="tag">' + esc(s.titel) + '</span> ' +
        'Vraag ' + (s.i + 1) + ' / ' + s.vragen.length + ' · ' + beantwoord + ' beantwoord</div>' +
        '<div><span class="timer" id="timer">' + fmtTime(Math.max(0, s.resterend)) + '</span></div>' +
      '</div>' +
      '<div class="progress"><i style="width:' + Math.round((beantwoord / s.vragen.length) * 100) + '%"></i></div>' +
      '<div class="card">' + questionHTML(q) + '</div>' +
      '<div class="btnrow">' +
        '<button class="btn ghost" id="prev"' + (s.i === 0 ? ' disabled' : '') + '>← Vorige</button>' +
        '<button class="btn ghost" id="flag">' + (q.vlag ? '★ Markering weg' : '☆ Markeer') + '</button>' +
        '<button class="btn" id="over">Overzicht</button>' +
        '<button class="btn primary" id="next">' + (s.i + 1 < s.vragen.length ? 'Volgende →' : 'Naar overzicht') + '</button>' +
      '</div>';

    markOptions(q, false);
    bindOptions(function (keuze) {
      q.keuze = keuze;
      markOptions(q, false);
      setTimeout(function () {
        if (s.i + 1 < s.vragen.length) { s.i++; renderExamenVraag(); }
        else renderOverzicht();
      }, 180);
    });

    document.getElementById('prev').onclick = function () { if (s.i > 0) { s.i--; renderExamenVraag(); } };
    document.getElementById('next').onclick = function () {
      if (s.i + 1 < s.vragen.length) { s.i++; renderExamenVraag(); } else renderOverzicht();
    };
    document.getElementById('flag').onclick = function () { q.vlag = !q.vlag; renderExamenVraag(); };
    document.getElementById('over').onclick = renderOverzicht;
  }

  function renderOverzicht() {
    var s = session;
    var open = s.vragen.filter(function (q) { return q.keuze === null; }).length;
    var cells = s.vragen.map(function (q, i) {
      return '<button data-i="' + i + '" class="' +
        (q.keuze !== null ? 'answered ' : '') + (q.vlag ? 'flag ' : '') + (i === s.i ? 'now' : '') + '">' + (i + 1) + '</button>';
    }).join('');

    app.innerHTML =
      '<div class="quizbar"><h1 style="margin:0;font-size:1.3rem">Overzicht</h1>' +
      '<div><span class="timer" id="timer">' + fmtTime(Math.max(0, s.resterend)) + '</span></div></div>' +
      '<p class="lead small">Klik op een nummer om terug te gaan. ' +
      (open ? '<strong>' + open + '</strong> vragen zijn nog niet beantwoord.' : 'Alle vragen zijn beantwoord.') + '</p>' +
      '<div class="card"><div class="qgrid" id="grid">' + cells + '</div>' +
      '<p class="small muted" style="margin-bottom:0">★ = door jou gemarkeerd · oranje = beantwoord</p></div>' +
      '<div class="btnrow">' +
        '<button class="btn" id="terug">Terug naar vraag ' + (s.i + 1) + '</button>' +
        '<button class="btn primary" id="lever">Examen inleveren</button>' +
      '</div>';

    document.getElementById('grid').onclick = function (e) {
      var b = e.target.closest('button[data-i]');
      if (!b) return;
      s.i = parseInt(b.dataset.i, 10);
      renderExamenVraag();
    };
    document.getElementById('terug').onclick = renderExamenVraag;
    document.getElementById('lever').onclick = function () {
      if (open && !confirm(open + ' vraag(en) zijn nog niet beantwoord. Toch inleveren?')) return;
      leverIn(false);
    };
  }

  function leverIn(tijdOp) {
    stopTimer();
    var s = session;
    s.klaar = true;
    s.tijdOp = !!tijdOp;
    s.goed = 0;
    s.perCat = {};
    s.vragen.forEach(function (q) {
      var c = s.perCat[q.categorie] || (s.perCat[q.categorie] = { goed: 0, totaal: 0 });
      c.totaal++;
      var good = q.keuze === q.antwoord;
      if (good) { s.goed++; c.goed++; }
      if (q.keuze !== null) noteAnswer(q.id, good); else noteAnswer(q.id, false);
    });
    s.geslaagd = s.goed >= s.norm;
    progress.examens.push({
      datum: Date.now(), score: s.goed, totaal: s.vragen.length,
      geslaagd: s.geslaagd, soort: s.titel || 'Examen'
    });
    save(progress);
    renderExamenResultaat();
  }

  function renderExamenResultaat() {
    var s = session;
    var pct = Math.round((s.goed / s.vragen.length) * 100);
    var catRows = Object.keys(s.perCat).map(function (c) {
      var d = s.perCat[c];
      return '<tr><th>' + (CAT_LABEL[c] || c) + '</th><td>' + d.goed + '/' + d.totaal + '</td>' +
        '<td><div class="bar"><i style="width:' + Math.round((d.goed / d.totaal) * 100) + '%"></i></div></td></tr>';
    }).join('');

    var fouten = s.vragen.filter(function (q) { return q.keuze !== q.antwoord; });
    var reviewHTML = fouten.length
      ? fouten.map(function (q) {
          return '<div class="review">' +
            '<p style="margin:.2em 0"><strong>' + esc(q.vraag) + '</strong></p>' +
            (q.afbeelding ? '<img class="qimg thumb" src="' + esc(q.afbeelding) + '" alt="Afbeelding bij de vraag">' : '') +
            '<p class="small" style="margin:.2em 0">Jouw antwoord: ' +
              (q.keuze === null ? '<em>niet beantwoord</em>' : esc(q.opties[q.keuze])) + '<br>' +
              'Juiste antwoord: <strong>' + esc(q.opties[q.antwoord]) + '</strong></p>' +
            '<p class="small muted" style="margin:.2em 0">' + esc(q.uitleg) + '</p></div>';
        }).join('')
      : '<p class="muted">Je had alles goed. Netjes.</p>';

    app.innerHTML =
      '<span class="tag">' + esc(s.titel || 'Examen') + '</span>' +
      '<h1>Uitslag</h1>' +
      (s.tijdOp ? '<p class="lead">De tijd was op — het examen is automatisch ingeleverd.</p>' : '') +
      '<div class="card score">' +
        '<div class="ring" style="--p:' + pct + '" data-label="' + s.goed + '/' + s.vragen.length + '"></div>' +
        '<div>' +
          '<div class="verdict ' + (s.geslaagd ? 'pass' : 'fail') + '">' + (s.geslaagd ? 'Geslaagd 🎉' : 'Gezakt') + '</div>' +
          '<p class="muted">Je hebt ' + s.norm + ' van de ' + s.vragen.length + ' goede antwoorden nodig.</p>' +
        '</div>' +
      '</div>' +
      '<div class="card"><h2 style="margin-top:0">Per onderdeel</h2><table><tbody>' + catRows + '</tbody></table></div>' +
      '<div class="card"><h2 style="margin-top:0">Fout beantwoord (' + fouten.length + ')</h2>' + reviewHTML + '</div>' +
      '<div class="btnrow">' +
        '<button class="btn primary" id="opnieuw">Opnieuw</button>' +
        '<a class="btn" href="#/oefenen/fouten">Foute vragen oefenen</a>' +
        '<a class="btn ghost" href="#/examen">Ander examen kiezen</a>' +
      '</div>';
    document.getElementById('opnieuw').onclick = function () { startExamen(s.cfg); };
  }

  /* ----- voortgang ----- */

  function viewVoortgang() {
    stopTimer(); session = null;
    var ids = Object.keys(progress.vragen);
    var totGoed = 0, totFout = 0;
    ids.forEach(function (id) { totGoed += progress.vragen[id].goed; totFout += progress.vragen[id].fout; });
    var pogingen = totGoed + totFout;

    var catRows = Object.keys(CAT_LABEL).map(function (c) {
      var g = 0, f = 0;
      byCat(c).forEach(function (q) {
        var v = progress.vragen[q.id]; if (v) { g += v.goed; f += v.fout; }
      });
      var t = g + f;
      return '<tr><th>' + CAT_LABEL[c] + '</th><td>' + (t ? Math.round((g / t) * 100) + '%' : '—') + '</td>' +
        '<td><div class="bar"><i style="width:' + (t ? Math.round((g / t) * 100) : 0) + '%"></i></div></td>' +
        '<td class="muted small">' + t + ' pogingen</td></tr>';
    }).join('');

    var exRows = progress.examens.slice().reverse().slice(0, 10).map(function (e) {
      return '<tr><td>' + new Date(e.datum).toLocaleString('nl-NL', { dateStyle: 'short', timeStyle: 'short' }) + '</td>' +
        '<td class="small">' + esc(e.soort || 'Examen') + '</td>' +
        '<td>' + e.score + '/' + e.totaal + '</td>' +
        '<td class="' + (e.geslaagd ? 'verdict pass' : 'verdict fail') + '" style="font-size:.9rem">' +
        (e.geslaagd ? 'geslaagd' : 'gezakt') + '</td></tr>';
    }).join('');

    var fout = foutenIds().length;

    app.innerHTML =
      '<h1>Mijn voortgang</h1>' +
      '<p class="lead">Alles wordt alleen in deze browser opgeslagen.</p>' +
      (pogingen === 0
        ? '<div class="card"><p style="margin:0">Je hebt nog geen vragen beantwoord. <a href="#/oefenen">Begin met oefenen</a>.</p></div>'
        : '<div class="card"><h2 style="margin-top:0">Score per categorie</h2>' +
          '<table><tbody>' + catRows + '</tbody></table>' +
          '<p class="small muted" style="margin-bottom:0">Totaal ' + pogingen + ' beantwoorde vragen, waarvan ' + totGoed + ' goed.</p></div>') +
      (fout ? '<div class="btnrow"><a class="btn primary" href="#/oefenen/fouten">Oefen je ' + fout + ' foute vragen</a></div>' : '') +
      (progress.examens.length
        ? '<div class="card"><h2 style="margin-top:0">Examengeschiedenis</h2><table>' +
          '<thead><tr><th>Datum</th><th>Examen</th><th>Score</th><th>Uitslag</th></tr></thead><tbody>' + exRows + '</tbody></table></div>'
        : '') +
      '<div class="btnrow"><button class="btn ghost" id="wis">Voortgang wissen</button></div>';

    document.getElementById('wis').onclick = function () {
      if (!confirm('Weet je zeker dat je al je voortgang wilt wissen?')) return;
      progress = { vragen: {}, examens: [] };
      save(progress);
      viewVoortgang();
    };
  }

  /* ---------------- vraag-rendering ---------------- */

  function questionHTML(q) {
    var letters = 'ABCDEFG';
    return (q.afbeelding ? '<img class="qimg" src="' + esc(q.afbeelding) + '" alt="Verkeerssituatie bij de vraag">' : '') +
      '<span class="tag">' + esc(CAT_LABEL[q.categorie] || q.categorie) + ' · ' + esc(q.onderwerp) + '</span>' +
      '<p class="qtext">' + esc(q.vraag) + '</p>' +
      '<div class="options" id="opts">' +
        q.opties.map(function (o, i) {
          return '<button class="opt" data-i="' + i + '"><span class="letter">' + letters[i] + '</span>' +
            '<span>' + esc(o) + '</span></button>';
        }).join('') +
      '</div>';
  }

  function bindOptions(cb) {
    var box = document.getElementById('opts');
    if (!box) return;
    box.onclick = function (e) {
      var b = e.target.closest('.opt');
      if (!b || b.disabled) return;
      cb(parseInt(b.dataset.i, 10));
    };
  }

  function markOptions(q, onthul) {
    var nodes = document.querySelectorAll('#opts .opt');
    nodes.forEach(function (n, i) {
      n.classList.remove('selected', 'correct', 'wrong');
      if (onthul) {
        n.disabled = true;
        if (i === q.antwoord) n.classList.add('correct');
        else if (i === q.keuze) n.classList.add('wrong');
      } else if (i === q.keuze) {
        n.classList.add('selected');
      }
    });
  }

  /* ---------------- start ---------------- */

  window.addEventListener('hashchange', route);
  window.addEventListener('beforeunload', function (e) {
    if (session && session.type === 'examen' && !session.klaar) {
      e.preventDefault(); e.returnValue = '';
    }
  });

  fetch('data/questions.json', { cache: 'no-cache' })
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (json) {
      DATA = json;
      route();
    })
    .catch(function (err) {
      app.innerHTML = '<h1>Kon de vragen niet laden</h1>' +
        '<p class="lead">Open de site via een webserver (of GitHub Pages), niet rechtstreeks vanaf je harde schijf.</p>' +
        '<p class="small muted">' + esc(err.message) + '</p>';
    });
})();
