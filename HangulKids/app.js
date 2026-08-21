import { THEMES, CONSONANTS, VOWELS, WORD_QUIZZES, TRACING_LETTERS, STORYBOOK_PAGES, combineHangul } from './data.js';
import { sound } from './audio.js';

class HangulApp {
  constructor() {
    this.currentTheme = 'dino';
    this.currentMode = 'train';
    this.stars = parseInt(localStorage.getItem('hangul_stars') || '0', 10);
    
    // Train state
    this.selectedConsonant = CONSONANTS[0];
    this.selectedVowel = VOWELS[0];
    
    // Quiz state
    this.quizIndex = 0;
    this.currentQuizSyllableIndex = 0;
    this.currentQuiz = null;

    // Tracing state
    this.currentTracingChar = TRACING_LETTERS[0];
    this.isDrawing = false;
    this.canvas = null;
    this.ctx = null;
    this.lastX = 0;
    this.lastY = 0;
    this.drawnStrokeCount = 0;

    // Storybook state
    this.currentStoryPage = 0;

    // Confetti
    this.confettiParticles = [];

    this.initElements();
    this.bindEvents();
    this.initCanvas();
    this.applyTheme(this.currentTheme);
    this.renderTrainMode();
    this.renderQuizMode();
    this.renderTracingMode();
    this.renderStorybookMode();
    this.updateStarsUI();
    this.initConfetti();
    this.startSessionTimer();
  }

  initElements() {
    this.brandIcon = document.getElementById('brandIcon');
    this.charAvatar = document.getElementById('charAvatar');
    this.charBubble = document.getElementById('charBubble');
    this.starCountEl = document.getElementById('starCount');
    
    // Tabs & views
    this.tabButtons = document.querySelectorAll('.tab-btn');
    this.modeViews = {
      train: document.getElementById('viewTrain'),
      quiz: document.getElementById('viewQuiz'),
      tracing: document.getElementById('viewTracing'),
      storybook: document.getElementById('viewStorybook')
    };

    // Modals
    this.rewardModal = document.getElementById('rewardModal');
    this.modalEmoji = document.getElementById('modalEmoji');
    this.modalTitle = document.getElementById('modalTitle');
    this.modalDesc = document.getElementById('modalDesc');
    this.closeRewardBtn = document.getElementById('closeRewardModalBtn');
    
    this.timerModal = document.getElementById('timerModal');
    this.timerBtn = document.getElementById('timerBtn');
    this.closeTimerModalBtn = document.getElementById('closeTimerModalBtn');
    this.soundToggleBtn = document.getElementById('soundToggleBtn');
  }

  bindEvents() {
    // Theme switching
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.playPop();
        const themeKey = btn.dataset.theme;
        this.applyTheme(themeKey);
      });
    });

    // Mode tabs switching
    this.tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        sound.playPop();
        const mode = btn.dataset.mode;
        this.switchMode(mode);
      });
    });

    // Sound toggle
    this.soundToggleBtn.addEventListener('click', () => {
      sound.isMuted = !sound.isMuted;
      this.soundToggleBtn.textContent = sound.isMuted ? '🔇' : '🔊';
      if (!sound.isMuted) {
        sound.playPop();
      }
    });

    // Timer modal open/close
    this.timerBtn.addEventListener('click', () => {
      sound.playPop();
      this.timerModal.classList.add('active');
    });

    this.closeTimerModalBtn.addEventListener('click', () => {
      sound.playPop();
      this.timerModal.classList.remove('active');
    });

    // Reward modal close
    this.closeRewardBtn.addEventListener('click', () => {
      sound.playPop();
      this.rewardModal.classList.remove('active');
    });

    // Train Result Click
    const resultCard = document.getElementById('resultCombined');
    resultCard.addEventListener('click', () => {
      this.playCombinationSound();
    });

    // Quiz Controls
    document.getElementById('nextQuizBtn').addEventListener('click', () => {
      sound.playPop();
      const list = WORD_QUIZZES[this.currentTheme] || WORD_QUIZZES.animal;
      this.quizIndex = (this.quizIndex + 1) % list.length;
      this.renderQuizMode();
    });

    document.getElementById('quizHearBtn').addEventListener('click', () => {
      if (this.currentQuiz) {
        sound.speak(this.currentQuiz.soundText || this.currentQuiz.word);
      }
    });

    document.getElementById('quizEmoji').addEventListener('click', () => {
      if (this.currentQuiz) {
        sound.speak(this.currentQuiz.word);
      }
    });

    // Tracing Controls
    document.getElementById('clearCanvasBtn').addEventListener('click', () => {
      sound.playPop();
      this.clearCanvas();
    });

    document.getElementById('speakTraceCharBtn').addEventListener('click', () => {
      sound.speak(this.currentTracingChar.name + ', ' + this.currentTracingChar.char);
    });

    document.getElementById('tracingSuccessBtn').addEventListener('click', () => {
      this.completeTracing();
    });

    // Storybook Controls
    document.getElementById('prevStoryBtn').addEventListener('click', () => {
      sound.playPop();
      if (this.currentStoryPage > 0) {
        this.currentStoryPage--;
        this.renderStorybookMode();
      }
    });

    document.getElementById('nextStoryBtn').addEventListener('click', () => {
      sound.playPop();
      if (this.currentStoryPage < STORYBOOK_PAGES.length - 1) {
        this.currentStoryPage++;
        this.renderStorybookMode();
      }
    });

    document.getElementById('readStoryBtn').addEventListener('click', () => {
      const page = STORYBOOK_PAGES[this.currentStoryPage];
      sound.speak(page.text, 0.85, 1.1);
    });
  }

  // Theme Application
  applyTheme(themeKey) {
    const theme = THEMES[themeKey] || THEMES.dino;
    this.currentTheme = themeKey;

    document.documentElement.style.setProperty('--primary', theme.primaryColor);
    document.documentElement.style.setProperty('--accent', theme.accentColor);
    document.documentElement.style.setProperty('--bg-gradient', theme.bgGradient);

    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.theme === themeKey);
    });

    this.brandIcon.textContent = theme.icon;
    this.charAvatar.textContent = theme.character.split(' ')[0];
    this.charBubble.textContent = theme.greeting;

    // Reset quiz for theme
    this.quizIndex = 0;
    this.renderQuizMode();
  }

  // Switch Mode Tab
  switchMode(mode) {
    this.currentMode = mode;
    this.tabButtons.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    Object.keys(this.modeViews).forEach(key => {
      this.modeViews[key].classList.toggle('active', key === mode);
    });

    if (mode === 'train') {
      this.charBubble.textContent = '자음 카트에 모음 승객을 태워 새로운 소리를 만들어봐요!';
    } else if (mode === 'quiz') {
      this.charBubble.textContent = '풍선 속에 숨은 글자를 찾아 터뜨려 단어를 완성해볼까?';
    } else if (mode === 'tracing') {
      this.charBubble.textContent = '반짝이는 별을 따라 예쁜 글자를 그려보세요!';
    } else if (mode === 'storybook') {
      this.charBubble.textContent = '우리가 함께 만든 멋진 한글 모험 이야기를 읽어보자!';
    }
  }

  addStars(count = 1) {
    this.stars += count;
    localStorage.setItem('hangul_stars', this.stars.toString());
    this.updateStarsUI();
    this.triggerConfetti();
  }

  updateStarsUI() {
    this.starCountEl.textContent = this.stars;
    const badge = document.getElementById('starBadge');
    badge.classList.remove('popIn');
    void badge.offsetWidth;
    badge.classList.add('popIn');
  }

  showReward(emoji, title, desc) {
    this.modalEmoji.textContent = emoji;
    this.modalTitle.textContent = title;
    this.modalDesc.textContent = desc;
    this.rewardModal.classList.add('active');
    sound.playFanfare();
  }

  // =========================================================================
  // MODE 1: 자모음 합체 기차
  // =========================================================================
  renderTrainMode() {
    const consonantGrid = document.getElementById('consonantGrid');
    const vowelGrid = document.getElementById('vowelGrid');

    consonantGrid.innerHTML = '';
    vowelGrid.innerHTML = '';

    // Render Consonant buttons
    CONSONANTS.forEach(item => {
      const btn = document.createElement('button');
      btn.className = `char-btn ${this.selectedConsonant.char === item.char ? 'active' : ''}`;
      btn.innerHTML = `<span>${item.char}</span><span class="sub-sound">${item.sound}</span>`;
      btn.addEventListener('click', () => {
        sound.playPop();
        sound.speak(item.sound);
        this.selectedConsonant = item;
        this.updateTrainAssembly();
        this.renderTrainMode();
      });
      consonantGrid.appendChild(btn);
    });

    // Render Vowel buttons
    VOWELS.forEach(item => {
      const btn = document.createElement('button');
      btn.className = `char-btn ${this.selectedVowel.char === item.char ? 'active' : ''}`;
      btn.innerHTML = `<span>${item.char}</span><span class="sub-sound">${item.sound}</span>`;
      btn.addEventListener('click', () => {
        sound.playPop();
        sound.speak(item.sound);
        this.selectedVowel = item;
        this.updateTrainAssembly();
        this.renderTrainMode();
      });
      vowelGrid.appendChild(btn);
    });

    this.updateTrainAssembly(false);
  }

  updateTrainAssembly(shouldPlayVoice = true) {
    const slotC = document.getElementById('slotConsonantVal');
    const slotV = document.getElementById('slotVowelVal');
    const resultVal = document.getElementById('resultCombinedVal');

    slotC.textContent = this.selectedConsonant.char;
    slotV.textContent = this.selectedVowel.char;

    const combined = combineHangul(this.selectedConsonant.char, this.selectedVowel.char);
    resultVal.textContent = combined;

    if (shouldPlayVoice) {
      this.playCombinationSound();
    }
  }

  playCombinationSound() {
    const c = this.selectedConsonant;
    const v = this.selectedVowel;
    const combined = combineHangul(c.char, v.char);
    
    sound.playTrainWhistle();
    setTimeout(() => {
      sound.speak(`${c.sound}! ${v.sound}! 합쳐서 ${combined}!`);
      this.addStars(1);
    }, 400);
  }

  // =========================================================================
  // MODE 2: 풍선 팡팡 단어 퀴즈
  // =========================================================================
  renderQuizMode() {
    const list = WORD_QUIZZES[this.currentTheme] || WORD_QUIZZES.animal;
    if (this.quizIndex >= list.length) {
      this.quizIndex = 0;
    }
    this.currentQuiz = list[this.quizIndex];
    this.currentQuizSyllableIndex = 0;

    const emojiEl = document.getElementById('quizEmoji');
    const hintEl = document.getElementById('quizHint');
    const slotsContainer = document.getElementById('wordSlotsContainer');
    const arena = document.getElementById('balloonArena');

    emojiEl.textContent = this.currentQuiz.emoji;
    hintEl.textContent = this.currentQuiz.hint;

    // Render Slots
    slotsContainer.innerHTML = '';
    this.currentQuiz.syllables.forEach((syl, i) => {
      const slot = document.createElement('div');
      slot.className = `word-slot ${i === 0 ? 'active-target' : ''}`;
      slot.id = `quizSlot_${i}`;
      slot.textContent = '?';
      slotsContainer.appendChild(slot);
    });

    // Prepare Candidate Balloons (correct syllables + random distractors)
    const candidates = [...this.currentQuiz.syllables];
    const decoyPool = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하', '고', '노', '도', '로', '모', '보', '소', '오'];
    while (candidates.length < 6) {
      const rand = decoyPool[Math.floor(Math.random() * decoyPool.length)];
      if (!candidates.includes(rand)) {
        candidates.push(rand);
      }
    }
    // Shuffle
    candidates.sort(() => Math.random() - 0.5);

    // Render Balloons
    arena.innerHTML = '';
    candidates.forEach((char) => {
      const balloon = document.createElement('div');
      balloon.className = 'balloon';
      balloon.textContent = char;
      balloon.addEventListener('click', () => {
        this.handleBalloonClick(balloon, char);
      });
      arena.appendChild(balloon);
    });
  }

  handleBalloonClick(balloonEl, char) {
    if (balloonEl.classList.contains('popped')) return;

    const targetSyllable = this.currentQuiz.syllables[this.currentQuizSyllableIndex];

    if (char === targetSyllable) {
      // Correct!
      sound.playBalloonPop();
      sound.speak(char);
      balloonEl.classList.add('popped');
      balloonEl.style.transform = 'scale(1.4)';
      balloonEl.style.opacity = '0';
      setTimeout(() => balloonEl.remove(), 250);

      // Fill slot
      const currentSlot = document.getElementById(`quizSlot_${this.currentQuizSyllableIndex}`);
      if (currentSlot) {
        currentSlot.textContent = char;
        currentSlot.classList.add('filled');
      }

      this.currentQuizSyllableIndex++;

      // Check if word completed
      if (this.currentQuizSyllableIndex >= this.currentQuiz.syllables.length) {
        setTimeout(() => {
          sound.playCorrect();
          sound.speak(`정답이에요! ${this.currentQuiz.soundText || this.currentQuiz.word}!`);
          this.addStars(2);
          this.showReward('🎉 🏆', `멋져요! "${this.currentQuiz.word}" 완성!`, `별 2개를 모았어요! 단어를 아주 잘 맞췄어요.`);
        }, 500);
      }
    } else {
      // Wrong balloon
      sound.playBoing();
      sound.speak('다시 찾아볼까?');
      balloonEl.style.animation = 'wiggle 0.3s ease';
      setTimeout(() => {
        balloonEl.style.animation = '';
      }, 300);
    }
  }

  // =========================================================================
  // MODE 3: 별자리 따라쓰기
  // =========================================================================
  initCanvas() {
    this.canvas = document.getElementById('tracingCanvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    const startDraw = (e) => {
      this.isDrawing = true;
      const rect = this.canvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      this.lastX = clientX - rect.left;
      this.lastY = clientY - rect.top;
      sound.playSparkle();
    };

    const draw = (e) => {
      if (!this.isDrawing) return;
      e.preventDefault();
      const rect = this.canvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      const currentX = clientX - rect.left;
      const currentY = clientY - rect.top;

      this.ctx.beginPath();
      this.ctx.moveTo(this.lastX, this.lastY);
      this.ctx.lineTo(currentX, currentY);
      this.ctx.strokeStyle = '#38bdf8';
      this.ctx.lineWidth = 14;
      this.ctx.lineCap = 'round';
      this.ctx.lineJoin = 'round';
      this.ctx.shadowColor = '#818cf8';
      this.ctx.shadowBlur = 10;
      this.ctx.stroke();

      this.lastX = currentX;
      this.lastY = currentY;
      this.drawnStrokeCount++;
    };

    const stopDraw = () => {
      this.isDrawing = false;
    };

    this.canvas.addEventListener('mousedown', startDraw);
    this.canvas.addEventListener('mousemove', draw);
    window.addEventListener('mouseup', stopDraw);

    this.canvas.addEventListener('touchstart', startDraw, { passive: false });
    this.canvas.addEventListener('touchmove', draw, { passive: false });
    window.addEventListener('touchend', stopDraw);
  }

  clearCanvas() {
    if (this.ctx && this.canvas) {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.drawnStrokeCount = 0;
    }
  }

  renderTracingMode() {
    const listEl = document.getElementById('tracingPickerList');
    const guideLetter = document.getElementById('guideLetter');

    listEl.innerHTML = '';
    TRACING_LETTERS.forEach(item => {
      const card = document.createElement('div');
      card.className = `letter-pick-card ${this.currentTracingChar.char === item.char ? 'active' : ''}`;
      card.innerHTML = `
        <span class="pick-char">${item.char}</span>
        <span class="pick-name">${item.name} (${item.icon})</span>
      `;
      card.addEventListener('click', () => {
        sound.playPop();
        sound.speak(item.name);
        this.currentTracingChar = item;
        guideLetter.textContent = item.char;
        this.clearCanvas();
        this.renderTracingMode();
      });
      listEl.appendChild(card);
    });

    guideLetter.textContent = this.currentTracingChar.char;
  }

  completeTracing() {
    sound.playCorrect();
    sound.speak(`참 잘 썼어요! ${this.currentTracingChar.name}, ${this.currentTracingChar.char}!`);
    this.addStars(1);
    this.showReward('🌟 ✨', `글자 완성 도장 쾅!`, `"${this.currentTracingChar.char}" 글자를 멋지게 따라 썼어요!`);
  }

  // =========================================================================
  // MODE 4: 모험 동화책 (스토리 & 스티커)
  // =========================================================================
  renderStorybookMode() {
    const page = STORYBOOK_PAGES[this.currentStoryPage];
    const pageTag = document.getElementById('storyPageTag');
    const illustration = document.getElementById('storyIllustration');
    const storyText = document.getElementById('storyText');
    const stickerGrid = document.getElementById('stickerGrid');

    pageTag.textContent = `제 ${page.page}장 / 4장`;
    illustration.textContent = page.illustration;

    // Highlight key word in story
    const highlighted = page.text.replace(page.highlightWord, `<span class="highlight">${page.highlightWord}</span>`);
    storyText.innerHTML = highlighted;

    // Render Stickers
    stickerGrid.innerHTML = '';
    STORYBOOK_PAGES.forEach((p) => {
      const isUnlocked = this.stars >= p.requiredStars;
      const stickerEl = document.createElement('div');
      stickerEl.className = `sticker-item ${isUnlocked ? 'unlocked' : ''}`;
      stickerEl.innerHTML = `
        <span>${isUnlocked ? p.sticker : '🔒 별 ' + p.requiredStars + '개 필요'}</span>
      `;
      stickerEl.addEventListener('click', () => {
        if (isUnlocked) {
          sound.playPop();
          sound.speak(p.sticker);
        } else {
          sound.playBoing();
          sound.speak(`별이 ${p.requiredStars}개 필요해요!`);
        }
      });
      stickerGrid.appendChild(stickerEl);
    });
  }

  // Confetti Particle System
  initConfetti() {
    const canvas = document.getElementById('confettiCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resize);
    resize();

    const loop = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < this.confettiParticles.length; i++) {
        const p = this.confettiParticles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.15;
        p.rotation += p.vRot;
        p.opacity -= 0.008;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = Math.max(0, p.opacity);
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.restore();
      }
      this.confettiParticles = this.confettiParticles.filter(p => p.opacity > 0);
      requestAnimationFrame(loop);
    };
    loop();
  }

  triggerConfetti() {
    const colors = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#fde047'];
    for (let i = 0; i < 60; i++) {
      this.confettiParticles.push({
        x: window.innerWidth / 2,
        y: window.innerHeight / 2,
        vx: (Math.random() - 0.5) * 16,
        vy: (Math.random() - 0.8) * 16,
        size: Math.random() * 12 + 6,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * Math.PI * 2,
        vRot: (Math.random() - 0.5) * 0.2,
        opacity: 1
      });
    }
  }

  // 15-Minute session gentle timer
  startSessionTimer() {
    const SESSION_MINUTES = 15;
    setTimeout(() => {
      this.timerModal.classList.add('active');
      sound.speak('오늘 한글 탐험을 아주 잘 마쳤어요! 소중한 눈을 위해 잠깐 쉬어가요~');
    }, SESSION_MINUTES * 60 * 1000);
  }
}

// Start application when DOM is ready
window.addEventListener('DOMContentLoaded', () => {
  window.hangulApp = new HangulApp();
});
