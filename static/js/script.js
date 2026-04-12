// Helper alert
function showAlert(msg) {
  alert(msg);
}

document.addEventListener('DOMContentLoaded', () => {
  // Live button alert
  const liveBtn = document.getElementById('watchLiveNowBtn');
  if (liveBtn) {
    liveBtn.addEventListener('click', () => {
      showAlert('🌐 LIVE STREAM: Join the worship now! Tune in via our YouTube channel.');
    });
  }

  // Modal logic
  const socialModal = document.getElementById('socialModal');
  const prayerModal = document.getElementById('prayerModal');
  const closeBtns = document.querySelectorAll('.close-modal');

  function openModal(modal) {
    if (modal) modal.style.display = 'flex';
  }
  function closeModal(modal) {
    if (modal) modal.style.display = 'none';
  }

  const joinCard = document.getElementById('joinCard');
  const liveCard = document.getElementById('liveCard');
  const prayerCard = document.getElementById('prayerCard');

  if (joinCard) joinCard.addEventListener('click', () => openModal(socialModal));
  if (liveCard) liveCard.addEventListener('click', () => window.open('https://www.youtube.com/@henryonyirioha_ppn', '_blank'));
  if (prayerCard) prayerCard.addEventListener('click', () => openModal(prayerModal));

  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      closeModal(socialModal);
      closeModal(prayerModal);
    });
  });
  window.addEventListener('click', (e) => {
    if (e.target === socialModal) closeModal(socialModal);
    if (e.target === prayerModal) closeModal(prayerModal);
  });

  // Hero slideshow (6 seconds)
  let slideIndex = 0;
  const slides = document.querySelectorAll('.slide');
  if (slides.length > 0) {
    function showSlides() {
      slides.forEach(slide => slide.classList.remove('active'));
      slideIndex++;
      if (slideIndex > slides.length) slideIndex = 1;
      if (slides[slideIndex - 1]) slides[slideIndex - 1].classList.add('active');
      setTimeout(showSlides, 6000);
    }
    showSlides();
  }

  // Gallery slideshow (6 seconds)
  let galleryIndex = 0;
  const gallerySlides = document.querySelectorAll('.gallery-slide');
  function showGallerySlides() {
    if (!gallerySlides.length) return;
    gallerySlides.forEach(slide => slide.classList.remove('active'));
    galleryIndex++;
    if (galleryIndex > gallerySlides.length) galleryIndex = 1;
    if (gallerySlides[galleryIndex - 1]) gallerySlides[galleryIndex - 1].classList.add('active');
    setTimeout(showGallerySlides, 6000);
  }
  if (gallerySlides.length > 0) showGallerySlides();

  // Mobile menu toggle
  const toggleBtn = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => navLinks.classList.toggle('show'));
    document.querySelectorAll('.nav-links a').forEach(link => {
      link.addEventListener('click', () => navLinks.classList.remove('show'));
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === "#" || targetId === "") return;
      const targetElem = document.querySelector(targetId);
      if (targetElem) {
        e.preventDefault();
        targetElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ========== TESTIMONY IMAGE CAROUSEL ==========
  const track = document.getElementById('testiCarouselTrack');
  const prevBtn = document.getElementById('testiPrevBtn');
  const nextBtn = document.getElementById('testiNextBtn');
  const dotsContainer = document.getElementById('testiDots');

  if (track && prevBtn && nextBtn && dotsContainer) {
    const images = Array.from(track.children);
    const imageCount = images.length;
    let currentIndex = 0;

    // Create dots
    images.forEach((_, idx) => {
      const dot = document.createElement('span');
      dot.classList.add('dot');
      if (idx === 0) dot.classList.add('active');
      dot.addEventListener('click', () => goToImage(idx));
      dotsContainer.appendChild(dot);
    });
    const dots = document.querySelectorAll('.dot');

    function updateCarousel() {
      const width = images[0].getBoundingClientRect().width;
      track.style.transform = `translateX(-${currentIndex * width}px)`;
      dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === currentIndex);
      });
    }

    function goToImage(index) {
      if (index < 0) index = 0;
      if (index >= imageCount) index = imageCount - 1;
      currentIndex = index;
      updateCarousel();
    }

    prevBtn.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + imageCount) % imageCount;
      updateCarousel();
    });
    nextBtn.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % imageCount;
      updateCarousel();
    });

    // Touch swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    track.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    });
    track.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      if (touchEndX < touchStartX - 50) {
        currentIndex = (currentIndex + 1) % imageCount;
        updateCarousel();
      } else if (touchEndX > touchStartX + 50) {
        currentIndex = (currentIndex - 1 + imageCount) % imageCount;
        updateCarousel();
      }
    });

    window.addEventListener('resize', updateCarousel);
    updateCarousel();
  }
});

// Manchester countdown
function startManchesterCountdown() {
  const countdownEl = document.getElementById('manchesterCountdown');
  if (!countdownEl) return;
  // Set your actual event date here (YYYY, MM-1, DD, HH, MM, SS)
  const eventDate = new Date(2026, 4, 15, 18, 0, 0); // May 15, 2026 18:00
  const timer = setInterval(() => {
    const now = new Date();
    const distance = eventDate - now;
    if (distance < 0) {
      clearInterval(timer);
      countdownEl.innerHTML = "🔥 EVENT STARTED! 🔥";
    } else {
      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (86400000)) / (3600000));
      const mins = Math.floor((distance % 3600000) / 60000);
      const secs = Math.floor((distance % 60000) / 1000);
      countdownEl.innerHTML = `${days}d ${hours}h ${mins}m ${secs}s`;
    }
  }, 1000);
}
startManchesterCountdown();

document.querySelectorAll('.glass-card-light').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const rotateX = ((y / rect.height) - 0.5) * -10;
    const rotateY = ((x / rect.width) - 0.5) * 10;

    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'translateY(0)';
  });
});