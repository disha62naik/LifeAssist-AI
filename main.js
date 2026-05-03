// LifeAssist AI — main.js

document.addEventListener('DOMContentLoaded', () => {

  // ── Auto-hide alerts after 4 seconds ──
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // ── Active nav link highlight (fallback) ──
  const navLinks = document.querySelectorAll('.nav-links a');
  navLinks.forEach(link => {
    if (link.href === window.location.href) {
      link.classList.add('active');
    }
  });

  // ── Range slider live value display ──
  const ranges = document.querySelectorAll('input[type="range"]');
  ranges.forEach(range => {
    const targetId = range.id + '-val';
    const display = document.getElementById(targetId);
    if (display) {
      // Set initial value
      display.textContent = range.value;
      // Update on change
      range.addEventListener('input', () => {
        display.textContent = range.value;
      });
    }
  });

  // ── Confirm before deleting a task ──
  const deleteForms = document.querySelectorAll('form');
  deleteForms.forEach(form => {
    const hiddenAction = form.querySelector('input[name="action"]');
    if (hiddenAction && hiddenAction.value === 'delete') {
      form.addEventListener('submit', (e) => {
        const confirmed = confirm('Delete this task?');
        if (!confirmed) e.preventDefault();
      });
    }
  });

  // ── Animate productivity score circle on load ──
  const scoreFill = document.querySelector('.score-fill');
  if (scoreFill) {
    const offset = scoreFill.style.strokeDashoffset;
    scoreFill.style.strokeDashoffset = '314';
    setTimeout(() => {
      scoreFill.style.strokeDashoffset = offset;
    }, 100);
  }

  // ── Animate progress bar on tasks page ──
  const progressFill = document.querySelector('.progress-fill');
  if (progressFill) {
    const targetWidth = progressFill.style.width;
    progressFill.style.width = '0%';
    setTimeout(() => {
      progressFill.style.transition = 'width 0.8s ease';
      progressFill.style.width = targetWidth;
    }, 200);
  }

  // ── Animate ranked bars on decision page ──
  const rankBars = document.querySelectorAll('.rank-bar');
  rankBars.forEach(bar => {
    const targetWidth = bar.style.width;
    bar.style.width = '0%';
    setTimeout(() => {
      bar.style.transition = 'width 0.7s ease';
      bar.style.width = targetWidth;
    }, 300);
  });

});