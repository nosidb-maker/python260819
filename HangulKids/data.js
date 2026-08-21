// Hangul Data, Syllables, Themes, Word Quizzes, and Storybook Data

export const THEMES = {
  dino: {
    id: 'dino',
    name: '공룡 탐험대',
    icon: '🦖',
    bgGradient: 'linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%)',
    primaryColor: '#10b981',
    accentColor: '#f59e0b',
    character: '🦕 아기 티라노',
    greeting: '크앙! 나와 함께 신나는 한글 공룡 섬으로 떠나볼까?'
  },
  vehicle: {
    id: 'vehicle',
    name: '붕붕 탈것 마을',
    icon: '🚗',
    bgGradient: 'linear-gradient(135deg, #1d4ed8 0%, #3b82f6 50%, #60a5fa 100%)',
    primaryColor: '#3b82f6',
    accentColor: '#ef4444',
    character: '🚂 꼬마 기관차 칙칙이',
    greeting: '칙칙폭폭! 신호등이 초록불이야. 출발 준비 완료!'
  },
  animal: {
    id: 'animal',
    name: '귀여운 동물 숲',
    icon: '🦁',
    bgGradient: 'linear-gradient(135deg, #d97706 0%, #f59e0b 50%, #fbbf24 100%)',
    primaryColor: '#f59e0b',
    accentColor: '#10b981',
    character: '🦁 꼬마 사자 레오',
    greeting: '안녕! 동물 친구들이 한글 숲에 모두 모였어!'
  },
  space: {
    id: 'space',
    name: '신비한 우주 여행',
    icon: '🚀',
    bgGradient: 'linear-gradient(135deg, #4338ca 0%, #6366f1 50%, #818cf8 100%)',
    primaryColor: '#6366f1',
    accentColor: '#ec4899',
    character: '👨‍🚀 우주 비행사 토리',
    greeting: '반짝반짝 별빛 속으로 한글 우주선 발사 3, 2, 1!'
  }
};

// 기본 자음 및 음가 설명
export const CONSONANTS = [
  { char: 'ㄱ', name: '기역', sound: '그', sampleWord: '기차', emoji: '🚂' },
  { char: 'ㄴ', name: '니은', sound: '느', sampleWord: '나비', emoji: '🦋' },
  { char: 'ㄷ', name: '디귿', sound: '드', sampleWord: '다람쥐', emoji: '🐿️' },
  { char: 'ㄹ', name: '리을', sound: '르', sampleWord: '라디오', emoji: '📻' },
  { char: 'ㅁ', name: '미음', sound: '므', sampleWord: '모자', emoji: '🧢' },
  { char: 'ㅂ', name: '비읍', sound: '브', sampleWord: '바나나', emoji: '🍌' },
  { char: 'ㅅ', name: '시옷', sound: '스', sampleWord: '사자', emoji: '🦁' },
  { char: 'ㅇ', name: '이응', sound: '으', sampleWord: '오리', emoji: '🦆' },
  { char: 'ㅈ', name: '지읒', sound: '즈', sampleWord: '자동차', emoji: '🚗' },
  { char: 'ㅊ', name: '치읓', sound: '츠', sampleWord: '치타', emoji: '🐆' },
  { char: 'ㅋ', name: '키읔', sound: '크', sampleWord: '코끼리', emoji: '🐘' },
  { char: 'ㅌ', name: '티읕', sound: '트', sampleWord: '토끼', emoji: '🐰' },
  { char: 'ㅍ', name: '피읖', sound: '프', sampleWord: '포도', emoji: '🍇' },
  { char: 'ㅎ', name: '히읗', sound: '흐', sampleWord: '하마', emoji: '🦛' }
];

// 기본 모음 및 음가 설명
export const VOWELS = [
  { char: 'ㅏ', name: '아', sound: '아' },
  { char: 'ㅑ', name: '야', sound: '야' },
  { char: 'ㅓ', name: '어', sound: '어' },
  { char: 'ㅕ', name: '여', sound: '여' },
  { char: 'ㅗ', name: '오', sound: '오' },
  { char: 'ㅛ', name: '요', sound: '요' },
  { char: 'ㅜ', name: '우', sound: '우' },
  { char: 'ㅠ', name: '유', sound: '유' },
  { char: 'ㅡ', name: '으', sound: '으' },
  { char: 'ㅣ', name: '이', sound: '이' }
];

// 한글 음절 조합 계산 함수 (자음 + 모음)
export function combineHangul(consonant, vowel) {
  const CHO = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
  const JUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'];
  
  const choIndex = CHO.indexOf(consonant);
  const jungIndex = JUNG.indexOf(vowel);
  
  if (choIndex === -1 || jungIndex === -1) {
    return consonant + vowel;
  }
  
  const code = 0xAC00 + (choIndex * 21 * 28) + (jungIndex * 28);
  return String.fromCharCode(code);
}

// 테마별 단어 퀴즈 데이터 (6세 아동 친화적 단어)
export const WORD_QUIZZES = {
  animal: [
    { word: '사자', syllables: ['사', '자'], emoji: '🦁', hint: '용감한 동물의 왕!', soundText: '어흥! 사자' },
    { word: '토끼', syllables: ['토', '끼'], emoji: '🐰', hint: '깡충깡충 귀가 길어요', soundText: '깡충깡충 토끼' },
    { word: '오리', syllables: ['오', '리'], emoji: '🦆', hint: '뒤뚱뒤뚱 꽥꽥 헤엄쳐요', soundText: '꽥꽥 오리' },
    { word: '호랑이', syllables: ['호', '랑', '이'], emoji: '🐯', hint: '멋진 줄무늬가 있는 친구!', soundText: '어흥! 호랑이' },
    { word: '원숭이', syllables: ['원', '숭', '이'], emoji: '🐒', hint: '나무를 잘 타고 바나나를 좋아해요', soundText: '우끼끼 원숭이' },
    { word: '나비', syllables: ['나', '비'], emoji: '🦋', hint: '꽃밭을 팔랑팔랑 날아다녀요', soundText: '팔랑팔랑 나비' },
    { word: '코끼리', syllables: ['코', '끼', '리'], emoji: '🐘', hint: '긴 코로 물을 뿜어요', soundText: '뿌우 코끼리' },
    { word: '하마', syllables: ['하', '마'], emoji: '🦛', hint: '입이 아주 크고 물을 좋아해요', soundText: '크왕 하마' }
  ],
  vehicle: [
    { word: '기차', syllables: ['기', '차'], emoji: '🚂', hint: '칙칙폭폭 철길을 달려요', soundText: '칙칙폭폭 기차' },
    { word: '버스', syllables: ['버', '스'], emoji: '🚌', hint: '친구들과 함께 타는 큰 차예요', soundText: '빵빵 버스' },
    { word: '비행기', syllables: ['비', '행', '기'], emoji: '✈️', hint: '하늘 높이 날아가는 탈것!', soundText: '슝 비행기' },
    { word: '소방차', syllables: ['소', '방', '차'], emoji: '🚒', hint: '불을 끄러 출동해요 삐오삐오!', soundText: '삐오삐오 소방차' },
    { word: '경찰차', syllables: ['경', '찰', '차'], emoji: '🚓', hint: '마을을 안전하게 지켜줘요', soundText: '삐뽀삐뽀 경찰차' },
    { word: '배', syllables: ['배'], emoji: '🚢', hint: '넓은 바다 위를 둥둥 떠가요', soundText: '뿌앙 배' },
    { word: '자전거', syllables: ['자', '전', '거'], emoji: '🚲', hint: '따르릉 페달을 밟아요', soundText: '따르릉 자전거' }
  ],
  dino: [
    { word: '티라노', syllables: ['티', '라', '노'], emoji: '🦖', hint: '날카로운 이빨의 최강 공룡!', soundText: '크아앙 티라노' },
    { word: '트리케라', syllables: ['트', '리', '케', '라'], emoji: '🦕', hint: '얼굴에 멋진 뿔이 세 개 있어요', soundText: '트리케라톱스' },
    { word: '익룡', syllables: ['익', '룡'], emoji: '🦅', hint: '하늘을 나는 멋진 날개!', soundText: '푸드덕 익룡' },
    { word: '공룡알', syllables: ['공', '룡', '알'], emoji: '🥚', hint: '아기 공룡이 태어날 준비 중!', soundText: '토닥토닥 공룡알' },
    { word: '화석', syllables: ['화', '석'], emoji: '🦴', hint: '땅속에 숨겨진 공룡의 흔적', soundText: '반짝 화석' }
  ],
  space: [
    { word: '우주선', syllables: ['우', '주', '선'], emoji: '🚀', hint: '불꽃을 뿜으며 우주로 날아가요', soundText: '슝 우주선' },
    { word: '외계인', syllables: ['외', '계', '인'], emoji: '👽', hint: '우주에서 온 귀여운 친구', soundText: '삐리삐리 외계인' },
    { word: '달', syllables: ['달'], emoji: '🌙', hint: '밤하늘에 둥근 빛을 비춰줘요', soundText: '밝은 달' },
    { word: '별', syllables: ['별'], emoji: '⭐', hint: '반짝반짝 예쁘게 빛나요', soundText: '반짝반짝 별' },
    { word: '행성', syllables: ['행', '성'], emoji: '🪐', hint: '고리가 있는 신비한 우주 별', soundText: '신비한 행성' }
  ]
};

// 글자 따라쓰기 가이드 데이터
export const TRACING_LETTERS = [
  { char: 'ㄱ', name: '기역', strokes: ['가로로 긋고 아래로 꺾어요'], icon: '🚂' },
  { char: 'ㄴ', name: '니은', strokes: ['아래로 긋고 오른쪽으로 가요'], icon: '🦋' },
  { char: 'ㄷ', name: '디귿', strokes: ['가로, 아래, 오른쪽으로!'], icon: '🐿️' },
  { char: 'ㄹ', name: '리을', strokes: ['지그재그 마법의 길'], icon: '📻' },
  { char: 'ㅁ', name: '미음', strokes: ['네모네모 상자 모양'], icon: '🧢' },
  { char: 'ㅂ', name: '비읍', strokes: ['두 기둥 세우고 가로로 닫아요'], icon: '🍌' },
  { char: 'ㅅ', name: '시옷', strokes: ['지붕처럼 양쪽으로 내려요'], icon: '🦁' },
  { char: 'ㅇ', name: '이응', strokes: ['동글동글 둥근 해 모양'], icon: '🦆' },
  { char: 'ㅈ', name: '지읒', strokes: ['모자를 쓴 시옷 모양'], icon: '🚗' },
  { char: 'ㅊ', name: '치읓', strokes: ['안테나가 달린 지읒'], icon: '🐆' },
  { char: 'ㅋ', name: '키읔', strokes: ['기역 가운데 날개 하나'], icon: '🐘' },
  { char: 'ㅌ', name: '티읕', strokes: ['디귿 가운데 줄 하나'], icon: '🐰' },
  { char: 'ㅍ', name: '피읖', strokes: ['위아래 가로선과 두 기둥'], icon: '🍇' },
  { char: 'ㅎ', name: '히읗', strokes: ['모자 쓰고 방긋 웃는 이응'], icon: '🦛' },
  { char: '가', name: '가', strokes: ['기역과 아가 만났어요!'], icon: '🍎' },
  { char: '나', name: '나', strokes: ['니은과 아가 만났어요!'], icon: '🦋' },
  { char: '다', name: '다', strokes: ['디귿과 아가 만났어요!'], icon: '🐿️' },
  { char: '라', name: '라', strokes: ['리을과 아가 만났어요!'], icon: '🦁' }
];

// 동화책 스토리 데이터 (단계별 해금)
export const STORYBOOK_PAGES = [
  {
    page: 1,
    title: '제 1장: 한글 섬으로의 초대',
    text: '어느 맑은 날, 호기심 많은 꼬마 탐험가에게 반짝이는 비밀 지도가 날아왔어요. "한글 섬에서 신나는 모험을 시작해볼까?"',
    highlightWord: '지도',
    illustration: '🗺️ 🌟 👦',
    requiredStars: 0,
    sticker: '🌟 황금 나침반',
    unlocked: true
  },
  {
    page: 2,
    title: '제 2장: 칙칙폭폭 소리 기차',
    text: '기역 카트에 아 승객이 타자 "가!" 소리를 내며 무지개 철길을 힘차게 달렸어요!',
    highlightWord: '기차',
    illustration: '🚂 💨 🌈',
    requiredStars: 3,
    sticker: '🚂 무지개 기차',
    unlocked: false
  },
  {
    page: 3,
    title: '제 3장: 숲속 동물 친구들과 퀴즈',
    text: '사자와 토끼가 "우리 이름을 맞춰줘서 고마워!" 하고 맛있는 과일 열매를 선물했어요.',
    highlightWord: '사자',
    illustration: '🦁 🐰 🍎',
    requiredStars: 6,
    sticker: '🦁 용감한 사자',
    unlocked: false
  },
  {
    page: 4,
    title: '제 4장: 반짝반짝 한글 마스터',
    text: '하늘에 수놓인 별자리를 모두 잇자, 눈부신 왕관이 내려와 탐험가의 머리 위에 얹어졌답니다!',
    highlightWord: '별',
    illustration: '⭐ 👑 🌌',
    requiredStars: 9,
    sticker: '👑 한글 마스터 왕관',
    unlocked: false
  }
];
