/* ==========================================================================
   Lomanikaya — site behaviour
   Vanilla, no dependencies, ~4kb. Everything degrades gracefully: with JS off
   the page is still readable, navigable and the form still submits by email.
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Header state ----------------------------------------------------- */
  var head = document.getElementById('head');
  var dock = document.getElementById('dock');

  function onScroll() {
    var y = window.scrollY;
    if (head) head.classList.toggle('is-stuck', y > 40);
    // The mobile dock appears once the hero's own CTAs have scrolled away.
    if (dock) dock.classList.toggle('is-on', y > window.innerHeight * 0.7);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* --- Mobile navigation ------------------------------------------------ */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  function closeNav() {
    if (!nav || !burger) return;
    nav.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('is-locked');
  }

  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('is-locked', open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeNav();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeNav();
    });
  }

  /* --- Reveal on scroll ------------------------------------------------- */
  var reveals = document.querySelectorAll('.reveal');

  if (reduced || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* --- Countdown to the first retreat ----------------------------------- */
  var cd = document.getElementById('countdown');
  if (cd) {
    var target = new Date(cd.getAttribute('data-target')).getTime();
    var cells = {
      days: cd.querySelector('[data-cd="days"]'),
      hours: cd.querySelector('[data-cd="hours"]'),
      minutes: cd.querySelector('[data-cd="minutes"]'),
      seconds: cd.querySelector('[data-cd="seconds"]')
    };

    var pad = function (n) { return n < 10 ? '0' + n : String(n); };

    var tick = function () {
      var left = target - Date.now();
      if (isNaN(target) || left <= 0) { cd.hidden = true; return; }
      cd.hidden = false;
      var s = Math.floor(left / 1000);
      cells.days.textContent = Math.floor(s / 86400);
      cells.hours.textContent = pad(Math.floor(s / 3600) % 24);
      cells.minutes.textContent = pad(Math.floor(s / 60) % 60);
      cells.seconds.textContent = pad(s % 60);
    };
    tick();
    setInterval(tick, 1000);
  }

  /* --- Retreat CTAs preselect the right option in the form -------------- */
  var retreatSelect = document.getElementById('f-retreat');
  document.querySelectorAll('[data-retreat]').forEach(function (link) {
    link.addEventListener('click', function () {
      if (!retreatSelect) return;
      var want = link.getAttribute('data-retreat');
      Array.prototype.forEach.call(retreatSelect.options, function (opt) {
        if (opt.text.trim() === want.trim()) retreatSelect.value = opt.value || opt.text;
      });
    });
  });

  /* --- Film facades ----------------------------------------------------- */
  /* Nothing is requested from YouTube until the visitor clicks play. */
  document.querySelectorAll('.film__play').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-yt');
      var title = btn.getAttribute('data-title') || 'Lomanikaya film';

      if (!id || id.indexOf('REPLACE_ID') === 0) {
        if (btn.parentNode.querySelector('.film__missing')) return;
        var msg = document.createElement('p');
        msg.className = 'film__missing';
        msg.textContent =
          'This film is not linked yet — add its YouTube video ID to data-yt in index.html.';
        btn.parentNode.insertBefore(msg, btn.nextSibling);
        return;
      }

      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
                  '?autoplay=1&rel=0&modestbranding=1';
      frame.title = title;
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      frame.allowFullscreen = true;
      frame.loading = 'lazy';
      btn.replaceWith(frame);
    });
  });

  /* --- Enquiry form ----------------------------------------------------- */
  var form = document.getElementById('claim-form');
  var note = document.getElementById('form-note');

  function say(text, state) {
    if (!note) return;
    note.textContent = text;
    note.classList.remove('is-ok', 'is-bad');
    if (state) note.classList.add(state);
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var data = new FormData(form);
      var name = (data.get('name') || '').trim();
      var email = (data.get('email') || '').trim();

      var bad = null;
      if (!name) bad = form.querySelector('#f-name');
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) bad = form.querySelector('#f-email');

      form.querySelectorAll('[aria-invalid]').forEach(function (el) {
        el.removeAttribute('aria-invalid');
      });

      if (bad) {
        bad.setAttribute('aria-invalid', 'true');
        bad.focus();
        say('Please add your name and a valid email so we can reply.', 'is-bad');
        return;
      }

      var endpoint = form.getAttribute('data-endpoint');

      if (endpoint) {
        say('Sending…');
        fetch(endpoint, {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: data
        }).then(function (res) {
          if (!res.ok) throw new Error('bad status');
          form.reset();
          say('Thank you — your request is with us. We reply personally, usually within two working days.', 'is-ok');
        }).catch(function () {
          say('That did not send. Please call +679 927 2354 or email us directly.', 'is-bad');
        });
        return;
      }

      /* No endpoint configured: hand off to the visitor's mail client so the
         enquiry still reaches the resort on plain static hosting. */
      var to = form.getAttribute('data-mailto');
      var lines = [
        'Name: ' + name,
        'Email: ' + email,
        'Phone: ' + ((data.get('phone') || '').trim() || '—'),
        'Retreat: ' + data.get('retreat'),
        'Places: ' + data.get('guests'),
        '',
        (data.get('message') || '').trim() || '(no message)'
      ];
      var href = 'mailto:' + to +
        '?subject=' + encodeURIComponent('Claim a spot — ' + data.get('retreat')) +
        '&body=' + encodeURIComponent(lines.join('\n'));

      window.location.href = href;
      say('Opening your email app with the details filled in. If nothing happens, call +679 927 2354.', 'is-ok');
    });
  }

  /* --- Footer year ------------------------------------------------------ */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
