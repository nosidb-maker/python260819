const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav');

menuToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
});

document.querySelectorAll('.main-nav a').forEach((link) => {
  link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

document.querySelectorAll('.filter').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelector('.filter.active').classList.remove('active');
    button.classList.add('active');
    const filter = button.dataset.filter;
    document.querySelectorAll('.project-card').forEach((card) => {
      card.hidden = filter !== 'all' && card.dataset.category !== filter;
    });
  });
});

const emailButton = document.querySelector('.email-button');
const feedback = document.querySelector('.copy-feedback');
emailButton.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(emailButton.dataset.email);
    feedback.textContent = '이메일 주소가 클립보드에 복사되었습니다.';
  } catch {
    feedback.textContent = 'gidong@naver.com';
  }
  window.setTimeout(() => { feedback.textContent = ''; }, 2500);
});

document.querySelector('#year').textContent = new Date().getFullYear();
