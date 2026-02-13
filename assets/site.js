(() => {
  /* ── Dynamic Year ── */
  const year = new Date().getFullYear();
  document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = String(year);
  });

  /* ── Scroll Reveal ── */
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16 }
    );

    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('in'));
  }

  /* ── Active Navigation ── */
  const fileName = (p) => {
    const clean = p.split('/').pop() || '';
    return clean || 'index.html';
  };
  const currentUrl = new URL(window.location.href);
  const currentPath = currentUrl.pathname;
  const rawCurrentFile = fileName(currentPath);
  const currentFile = rawCurrentFile === 'about.html' ? 'index.html' : rawCurrentFile;
  const currentHash = currentUrl.hash || '';

  const navEntries = Array.from(document.querySelectorAll('[data-nav]'))
    .map((link) => {
      const href = link.getAttribute('href') || '';
      if (!href) return null;
      const url = new URL(href, currentUrl.href);
      return {
        link,
        targetFile: fileName(url.pathname),
        targetHash: url.hash || '',
      };
    })
    .filter(Boolean);

  // Pass 1: exact hash match (e.g. services.html#products)
  if (currentHash) {
    navEntries.forEach((entry) => {
      if (entry.targetFile === currentFile && entry.targetHash === currentHash) {
        entry.link.classList.add('is-active');
      }
    });
  }

  // Pass 2: fallback to file-level match (non-hash links only)
  if (!document.querySelector('[data-nav].is-active')) {
    navEntries.forEach((entry) => {
      if (entry.targetFile === currentFile && !entry.targetHash) {
        entry.link.classList.add('is-active');
      }
    });
  }

  /* ── Mobile Menu ── */
  const btn = document.querySelector('[data-menu-btn]');
  const panel = document.querySelector('[data-menu-panel]');
  if (btn && panel) {
    // Remove hidden class so CSS transition can work
    panel.classList.remove('hidden');

    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      panel.classList.toggle('menu-open');
    });

    panel.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        panel.classList.remove('menu-open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ── Desktop Dropdown (hover + keyboard; touch click opens) ── */
  document.querySelectorAll('[data-dropdown]').forEach((wrapper) => {
    const trigger = wrapper.querySelector('[data-dropdown-trigger]');
    const menu = wrapper.querySelector('[data-dropdown-menu]');
    if (!trigger || !menu) return;

    const open = () => {
      menu.classList.remove('hidden');
      trigger.setAttribute('aria-expanded', 'true');
    };
    const close = () => {
      menu.classList.add('hidden');
      trigger.setAttribute('aria-expanded', 'false');
    };

    trigger.addEventListener('click', (e) => {
      const isOpen = trigger.getAttribute('aria-expanded') === 'true';
      const isTouchMode = window.matchMedia('(pointer: coarse)').matches || window.innerWidth < 1024;

      // On touch/mobile: first tap opens dropdown, second tap follows the link.
      if (isTouchMode) {
        if (!isOpen) {
          e.preventDefault();
          closeAllDropdowns();
          open();
        } else {
          closeAllDropdowns();
        }
      }
      // On desktop: keep default link navigation behavior.
    });

    trigger.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        trigger.click();
      }
      if (e.key === 'Escape') close();
    });

    menu.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        close();
        trigger.focus();
      }
    });

    // Keep hover behavior for desktop mouse users
    let hoverTimeout;
    wrapper.addEventListener('mouseenter', () => {
      clearTimeout(hoverTimeout);
      open();
    });
    wrapper.addEventListener('mouseleave', () => {
      hoverTimeout = setTimeout(close, 200);
    });
  });

  function closeAllDropdowns() {
    document.querySelectorAll('[data-dropdown]').forEach((w) => {
      const t = w.querySelector('[data-dropdown-trigger]');
      const m = w.querySelector('[data-dropdown-menu]');
      if (t) t.setAttribute('aria-expanded', 'false');
      if (m) m.classList.add('hidden');
    });
  }

  document.addEventListener('click', (e) => {
    if (!e.target.closest('[data-dropdown]')) closeAllDropdowns();
  });

  /* ── Mobile Dropdown Toggles ── */
  document.querySelectorAll('[data-mobile-toggle]').forEach((toggle) => {
    toggle.addEventListener('click', () => {
      const target = toggle.nextElementSibling;
      if (!target) return;
      const isOpen = !target.classList.contains('hidden');
      target.classList.toggle('hidden');
      toggle.setAttribute('aria-expanded', isOpen ? 'false' : 'true');
      const chevron = toggle.querySelector('svg');
      if (chevron) chevron.style.transform = isOpen ? '' : 'rotate(180deg)';
    });
  });

  /* ── Contact Form Validation ── */
  const form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const errors = [];
      const name = form.querySelector('#name');
      const phone = form.querySelector('#phone');
      const service = form.querySelector('#service');
      const status = document.getElementById('form-status');
      const submitBtn = document.getElementById('contact-submit');

      // Reset errors
      form.querySelectorAll('.form-error').forEach((el) => el.classList.add('hidden'));
      form.querySelectorAll('input, select, textarea').forEach((el) => {
        el.classList.remove('border-joy-red');
      });

      // Validate
      if (!name.value.trim()) {
        showFieldError(name);
        errors.push('name');
      }
      if (!phone.value.trim() || !/^[0-9+\s\-]{10,15}$/.test(phone.value.trim())) {
        showFieldError(phone);
        errors.push('phone');
      }
      if (!service.value) {
        showFieldError(service);
        errors.push('service');
      }

      if (errors.length > 0) {
        form.querySelector('#' + errors[0]).focus();
        return;
      }

      // Submit via WhatsApp message (no backend needed)
      const message = encodeURIComponent(
        `Hi, I'd like to book an appointment.\n\n` +
        `Name: ${name.value.trim()}\n` +
        `Phone: ${phone.value.trim()}\n` +
        `Service: ${service.options[service.selectedIndex].text}\n` +
        `Message: ${form.querySelector('#message').value.trim() || 'N/A'}`
      );

      // Show success
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      if (status) {
        status.classList.remove('hidden', 'bg-red-50', 'text-red-700');
        status.classList.add('bg-green-50', 'text-green-700');
        status.textContent = 'Redirecting to WhatsApp to confirm your appointment...';
      }

      setTimeout(() => {
        window.open(`https://wa.me/918240516775?text=${message}`, '_blank');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
        form.reset();
        if (status) {
          status.textContent = 'Message prepared! Please send it via WhatsApp to confirm.';
        }
      }, 600);
    });
  }

  function showFieldError(field) {
    field.classList.add('border-joy-red');
    const error = field.parentElement.querySelector('.form-error');
    if (error) error.classList.remove('hidden');
  }

  /* ── Smooth Scroll ── */
  document.querySelectorAll('a[href*="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;
      const hashIndex = href.indexOf('#');
      const hash = href.substring(hashIndex);
      const page = href.substring(0, hashIndex);
      // Only smooth-scroll if link is to same page or no page specified
      if (!page || page === currentFile || page === './' || page === '') {
        const target = document.querySelector(hash);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  /* ── Back to Top Button ── */
  const topBtn = document.getElementById('back-to-top');
  if (topBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 600) {
        topBtn.classList.remove('opacity-0', 'pointer-events-none');
        topBtn.classList.add('opacity-100');
      } else {
        topBtn.classList.add('opacity-0', 'pointer-events-none');
        topBtn.classList.remove('opacity-100');
      }
    });
    topBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── Toast Notification ── */
  window.showToast = (message, type = 'success') => {
    const toast = document.createElement('div');
    toast.className = `fixed top-6 right-6 z-[100] px-6 py-3 rounded-xl shadow-2xl text-sm font-semibold transition-all transform translate-x-full ${
      type === 'success' ? 'bg-green-600 text-white' : 'bg-joy-red text-white'
    }`;
    toast.textContent = message;
    document.body.appendChild(toast);
    requestAnimationFrame(() => {
      toast.classList.remove('translate-x-full');
      toast.classList.add('translate-x-0');
    });
    setTimeout(() => {
      toast.classList.add('translate-x-full');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  };
})();
