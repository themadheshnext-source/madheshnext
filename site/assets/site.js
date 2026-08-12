/* Madhesh Next — shared behaviour: language switch, mobile nav, table filter */
(function () {
  'use strict';

  var KEY = 'mn-lang';
  var current = 'en';

  function store(v) { try { window.localStorage.setItem(KEY, v); } catch (e) {} }
  function recall() { try { return window.localStorage.getItem(KEY); } catch (e) { return null; } }

  function apply(lang) {
    current = (lang === 'ne') ? 'ne' : 'en';
    document.documentElement.setAttribute('data-lang', current);

    // Block-level swap: <x data-lang="en"> / <x data-lang="ne">
    var blocks = document.querySelectorAll('[data-lang]');
    for (var i = 0; i < blocks.length; i++) {
      var el = blocks[i];
      var on = el.getAttribute('data-lang') === current;
      if (on) { el.removeAttribute('hidden'); } else { el.setAttribute('hidden', ''); }
    }

    // Inline swap: <x class="t" data-en="..." data-ne="...">
    var inline = document.querySelectorAll('.t[data-en]');
    for (var j = 0; j < inline.length; j++) {
      var n = inline[j];
      var txt = (current === 'ne' && n.getAttribute('data-ne')) ? n.getAttribute('data-ne') : n.getAttribute('data-en');
      n.textContent = txt;
      n.setAttribute('lang', current);
    }

    // Buttons
    var btns = document.querySelectorAll('.langswitch button');
    for (var k = 0; k < btns.length; k++) {
      var b = btns[k];
      if (b.getAttribute('data-set') === current) { b.classList.add('is-on'); }
      else { b.classList.remove('is-on'); }
    }
    store(current);
  }

  function initLang() {
    var saved = recall();
    apply(saved === 'ne' ? 'ne' : 'en');
    document.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.langswitch button') : null;
      if (b) { e.preventDefault(); apply(b.getAttribute('data-set')); }
    });
  }

  function initNav() {
    var t = document.querySelector('.navtoggle');
    var l = document.querySelector('.nav__links');
    if (t && l) {
      t.addEventListener('click', function () {
        l.classList.toggle('is-open');
        t.setAttribute('aria-expanded', l.classList.contains('is-open') ? 'true' : 'false');
      });
    }
    // Mark active link
    var here = location.pathname.split('/').pop() || 'index.html';
    var links = document.querySelectorAll('.nav__links a');
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute('href') || '';
      if (href.split('/').pop() === here) { links[i].classList.add('is-active'); }
    }
  }

  function initFilter() {
    var box = document.querySelector('[data-filter-input]');
    var typeSel = document.querySelector('[data-filter-type]');
    var distSel = document.querySelector('[data-filter-district]');
    var table = document.querySelector('table.lgs');
    var countEl = document.querySelector('[data-filter-count]');
    if (!table) return;

    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));

    function run() {
      var q = (box && box.value || '').trim().toLowerCase();
      var ty = typeSel && typeSel.value || '';
      var di = distSel && distSel.value || '';
      var shown = 0;
      for (var i = 0; i < rows.length; i++) {
        var r = rows[i];
        var hay = (r.getAttribute('data-search') || '').toLowerCase();
        var ok = (!q || hay.indexOf(q) !== -1) &&
                 (!ty || r.getAttribute('data-type') === ty) &&
                 (!di || r.getAttribute('data-district') === di);
        r.hidden = !ok;
        if (ok) shown++;
      }
      if (countEl) {
        countEl.textContent = shown + ' of ' + rows.length +
          (current === 'ne' ? ' स्थानीय तह' : ' local levels');
      }
    }

    if (box) box.addEventListener('input', run);
    if (typeSel) typeSel.addEventListener('change', run);
    if (distSel) distSel.addEventListener('change', run);
    run();
    document.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('.langswitch button')) { setTimeout(run, 0); }
    });
  }

  function initForm() {
    var f = document.querySelector('[data-demo-form]');
    if (!f) return;
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var out = f.querySelector('[data-form-msg]');
      if (out) {
        out.hidden = false;
        out.textContent = (current === 'ne')
          ? 'धन्यवाद। यो फारम अहिले डेमो हो — पठाउने ठेगाना जोडेपछि सक्रिय हुनेछ।'
          : 'Thank you. This form is a demo — it will go live once a form endpoint is connected.';
      }
    });
  }

  function boot() { initLang(); initNav(); initFilter(); initForm(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();
