/* ==========================================================================
   Duurkracht Kozijnen — Main JavaScript
   ========================================================================== */

(function () {
  'use strict';

  // --- Sticky nav shadow ---
  var nav = document.querySelector('.site-nav');
  if (nav) {
    var onScroll = function () {
      if (window.scrollY > 80) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // --- Mobile hamburger ---
  var hamburger = document.querySelector('.btn-hamburger');
  var sidebar = document.querySelector('.mobile-sidebar');
  var overlay = document.querySelector('.mobile-sidebar-overlay');
  var closeBtn = document.querySelector('.mobile-sidebar-close');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('open');
    if (overlay) overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
  if (hamburger) hamburger.addEventListener('click', openSidebar);
  if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
  if (overlay) overlay.addEventListener('click', closeSidebar);

  // --- Dropdown click toggle for mobile/touch ---
  document.querySelectorAll('.nav-menu .has-dropdown > .dropdown-toggle').forEach(function (toggle) {
    toggle.addEventListener('click', function (e) {
      if (window.innerWidth <= 980) {
        e.preventDefault();
        toggle.parentElement.classList.toggle('open');
      }
    });
  });

  // --- Mobile sidebar submenu toggles ---
  document.querySelectorAll('.mobile-sidebar .submenu-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var sub = btn.nextElementSibling;
      if (sub) sub.style.display = sub.style.display === 'block' ? 'none' : 'block';
    });
  });

  // --- Scroll to top ---
  var scrollTop = document.querySelector('.scroll-top');
  if (scrollTop) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 400) scrollTop.classList.add('visible');
      else scrollTop.classList.remove('visible');
    }, { passive: true });
    scrollTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- FAQ accordion ---
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var question = item.querySelector('.faq-question');
    if (!question) return;
    question.addEventListener('click', function () {
      item.classList.toggle('open');
      var expanded = item.classList.contains('open');
      question.setAttribute('aria-expanded', expanded);
    });
  });

  // --- Project filter ---
  var filterBtns = document.querySelectorAll('.filter-btn');
  var projects = document.querySelectorAll('.project-card[data-category]');
  if (filterBtns.length && projects.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.getAttribute('data-filter');
        filterBtns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        projects.forEach(function (card) {
          var cardCat = card.getAttribute('data-category');
          if (cat === 'all' || cardCat === cat) card.classList.remove('hidden');
          else card.classList.add('hidden');
        });
      });
    });
  }

  // --- Load more (simulated lazy load) ---
  var loadMoreBtn = document.querySelector('.load-more-btn');
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function () {
      document.querySelectorAll('.project-card[data-hidden="true"]').forEach(function (card) {
        card.removeAttribute('data-hidden');
        card.classList.remove('hidden');
      });
      loadMoreBtn.style.display = 'none';
    });
  }

  // --- Contact form validation ---
  var form = document.querySelector('.contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var valid = true;
      form.querySelectorAll('[required]').forEach(function (field) {
        var wrap = field.closest('.form-field') || field.closest('.form-checkbox');
        if (!wrap) return;
        var isEmpty = field.type === 'checkbox' ? !field.checked : !field.value.trim();
        if (isEmpty) {
          wrap.classList.add('invalid');
          valid = false;
        } else {
          wrap.classList.remove('invalid');
        }
        if (field.type === 'email' && field.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(field.value)) {
          wrap.classList.add('invalid'); valid = false;
        }
      });
      if (valid) {
        var success = form.parentElement.querySelector('.form-success');
        if (success) {
          success.classList.add('show');
          success.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        form.reset();
      }
    });

    form.querySelectorAll('input, select, textarea').forEach(function (field) {
      field.addEventListener('input', function () {
        var wrap = field.closest('.form-field') || field.closest('.form-checkbox');
        if (wrap) wrap.classList.remove('invalid');
      });
    });
  }

  // --- Counter animation via IntersectionObserver ---
  var counters = document.querySelectorAll('[data-counter]');
  if (counters.length && 'IntersectionObserver' in window) {
    var animateCounter = function (el) {
      var target = parseInt(el.getAttribute('data-counter'), 10);
      var suffix = el.getAttribute('data-suffix') || '';
      var duration = 1600;
      var start = 0, startTime = null;
      function step(ts) {
        if (!startTime) startTime = ts;
        var progress = Math.min((ts - startTime) / duration, 1);
        var ease = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(start + (target - start) * ease) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    };
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { obs.observe(c); });
  }

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = this.getAttribute('href');
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        var offset = target.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: offset, behavior: 'smooth' });
      }
    });
  });

})();
