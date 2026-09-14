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

  /* ── Contact Form Validation + Email Delivery ── */
  const form = document.getElementById('contact-form');
  if (form) {
    const CONTACT_EMAIL_ENDPOINT = 'https://formsubmit.co/ajax/ashishbharti.joyfulhearing@gmail.com';
    const CONTACT_WHATSAPP_FALLBACK = 'https://wa.me/918240516775';

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

      // Prepare payload for email delivery
      const nameValue = name.value.trim();
      const phoneValue = phone.value.trim();
      const serviceValue = service.options[service.selectedIndex].text;
      const messageValue = form.querySelector('#message').value.trim() || 'N/A';

      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      if (status) {
        status.classList.remove('hidden', 'bg-red-50', 'text-red-700', 'bg-green-50', 'text-green-700');
        status.classList.add('bg-slate-100', 'text-slate-700');
        status.textContent = 'Sending your message to the clinic...';
      }

      const payload = new FormData();
      payload.append('name', nameValue);
      payload.append('phone', phoneValue);
      payload.append('service', serviceValue);
      payload.append('message', messageValue);
      payload.append('_subject', `New website inquiry: ${serviceValue}`);
      payload.append('_template', 'table');
      payload.append('_captcha', 'false');

      fetch(CONTACT_EMAIL_ENDPOINT, {
        method: 'POST',
        body: payload,
        headers: { Accept: 'application/json' },
      })
        .then((res) => {
          if (!res.ok) throw new Error(`Email request failed with status ${res.status}`);
          return res.json();
        })
        .then(() => {
          if (status) {
            status.classList.remove('bg-slate-100', 'text-slate-700');
            status.classList.add('bg-green-50', 'text-green-700');
            status.textContent = 'Message sent successfully. The clinic will contact you shortly.';
          }
          form.reset();
        })
        .catch(() => {
          if (status) {
            status.classList.remove('bg-slate-100', 'text-slate-700');
            status.classList.add('bg-red-50', 'text-red-700');
            status.innerHTML =
              'Could not send email right now. Please use WhatsApp immediately: ' +
              `<a class="underline font-semibold" href="${CONTACT_WHATSAPP_FALLBACK}" target="_blank" rel="noreferrer">Chat on WhatsApp</a>.`;
          }
        })
        .finally(() => {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Send Message';
        });
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

  /* ── Floating Hearing Quiz CTA ── */
  function mountFloatingQuizButton() {
    if (currentFile === 'hearing-screening.html') return;
    if (document.getElementById('floating-hearing-quiz')) return;

    const quizBtn = document.createElement('a');
    quizBtn.id = 'floating-hearing-quiz';
    quizBtn.href = 'hearing-screening.html';
    quizBtn.className = 'floating-quiz-btn';
    quizBtn.setAttribute('aria-label', 'Take the 2-minute hearing screening quiz');
    quizBtn.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 12a5 5 0 0 0-10 0"/><path d="M12 17.5a5.5 5.5 0 0 1-5.5-5.5V9a5.5 5.5 0 0 1 11 0v3a7.5 7.5 0 0 1-15 0V9"/><path d="M9.5 21h5"/></svg><span>Take 2-min Hearing Quiz</span>';
    document.body.appendChild(quizBtn);
  }

  mountFloatingQuizButton();

  /* ── Hearing Screening Questionnaire ── */
  const screeningForm = document.getElementById('hearing-screening-form');
  if (screeningForm) {
    const progressText = document.getElementById('screening-progress-text');
    const progressBar = document.getElementById('screening-progress-bar');
    const submitBtn = document.getElementById('screening-submit');
    const resetBtn = document.getElementById('screening-reset');
    const resultSection = document.getElementById('screening-result');
    const scoreValue = document.getElementById('screening-score');
    const scoreBand = document.getElementById('screening-band');
    const scoreSummary = document.getElementById('screening-summary');
    const nextStep = document.getElementById('screening-next-step');
    const severityBadge = document.getElementById('screening-severity');
    const whatsappBtn = document.getElementById('screening-whatsapp-btn');
    const bookBtn = document.getElementById('screening-book-btn');

    const questionNames = Array.from(
      new Set(
        Array.from(screeningForm.querySelectorAll('input[type="radio"]'))
          .map((input) => input.name)
          .filter(Boolean)
      )
    );
    const totalQuestions = questionNames.length;

    const bands = [
      {
        min: 0,
        max: 4,
        label: '0-4 (Within normal limits)',
        summary: 'Hearing appears within normal limits. Continue monitoring yearly.',
        next: 'Low current risk. Maintain annual hearing check-ups, especially if you are exposed to loud noise.',
        cta: 'Book Preventive Screening',
        severityClass: 'bg-emerald-100 text-emerald-700',
      },
      {
        min: 5,
        max: 10,
        label: '5-10 (Possible mild difficulty)',
        summary: 'Possible mild hearing difficulty detected. A screening test is recommended.',
        next: 'You may benefit from a baseline hearing test to catch early changes and avoid progression.',
        cta: 'Book Screening Test',
        severityClass: 'bg-amber-100 text-amber-700',
      },
      {
        min: 11,
        max: 16,
        label: '11-16 (Likely impairment)',
        summary: 'Likely hearing impairment. A complete diagnostic evaluation is recommended.',
        next: 'A full audiological evaluation will help identify degree and type of hearing issue for treatment planning.',
        cta: 'Book Diagnostic Evaluation',
        severityClass: 'bg-orange-100 text-orange-700',
      },
      {
        min: 17,
        max: 24,
        label: '17-24 (Significant difficulty)',
        summary: 'Significant hearing difficulty indicated. Immediate audiological assessment is advised.',
        next: 'Please contact the clinic as soon as possible for priority assessment and a personalized care plan.',
        cta: 'Book Priority Assessment',
        severityClass: 'bg-red-100 text-red-700',
      },
    ];

    const getBandForScore = (score) =>
      bands.find((band) => score >= band.min && score <= band.max) || bands[0];

    const getAnsweredCount = () =>
      questionNames.filter((name) => screeningForm.querySelector(`input[name="${name}"]:checked`)).length;

    const updateProgress = () => {
      const answered = getAnsweredCount();
      const percent = totalQuestions ? Math.round((answered / totalQuestions) * 100) : 0;

      if (progressText) progressText.textContent = `${answered}/${totalQuestions} answered`;
      if (progressBar) progressBar.style.width = `${percent}%`;
      if (submitBtn) submitBtn.disabled = answered !== totalQuestions;
    };

    const showIncompleteMessage = () => {
      if (typeof window.showToast === 'function') {
        window.showToast('Please answer all questions before viewing your result.', 'error');
      } else {
        window.alert('Please answer all questions before viewing your result.');
      }
    };

    screeningForm.addEventListener('change', updateProgress);

    screeningForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const answered = getAnsweredCount();
      if (answered !== totalQuestions) {
        showIncompleteMessage();
        return;
      }

      let score = 0;
      questionNames.forEach((name) => {
        const selected = screeningForm.querySelector(`input[name="${name}"]:checked`);
        score += Number(selected?.value || 0);
      });

      const band = getBandForScore(score);

      if (scoreValue) scoreValue.textContent = `${score}/24`;
      if (scoreBand) scoreBand.textContent = band.label;
      if (scoreSummary) scoreSummary.textContent = band.summary;
      if (nextStep) nextStep.textContent = band.next;

      if (severityBadge) {
        severityBadge.className =
          'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ' + band.severityClass;
        severityBadge.textContent = band.label;
      }

      if (bookBtn) {
        bookBtn.textContent = band.cta;
        bookBtn.href = 'contact.html';
      }

      if (whatsappBtn) {
        const message = encodeURIComponent(
          `Hi Joyful Hearing Clinic, I completed the 2-minute hearing screening quiz.\n` +
            `My score: ${score}/24\n` +
            `Result: ${band.label}\n` +
            `Recommendation: ${band.next}\n` +
            `I would like to book the next step consultation.`
        );
        whatsappBtn.href = `https://wa.me/918240516775?text=${message}`;
      }

      if (resultSection) {
        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        screeningForm.reset();
        updateProgress();
        if (resultSection) resultSection.classList.add('hidden');
      });
    }

    updateProgress();
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
