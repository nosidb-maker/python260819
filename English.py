import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


PAGE = r'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>파닉스 탐험대</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700&family=Jua&display=swap');
    :root { --ink:#233044; --muted:#66758c; --cream:#fff9ed; --coral:#ff6b5f; --blue:#3a8dde; --yellow:#ffd166; --mint:#67c5a6; --line:#e7dfd0; }
    * { box-sizing:border-box; }
    body { margin:0; color:var(--ink); background:var(--cream); font-family:'Baloo 2','Jua',sans-serif; }
    body:before { content:""; position:fixed; inset:0; z-index:-1; opacity:.45; background-image:radial-gradient(#f4c98b 1px,transparent 1px),radial-gradient(#aadcca 1px,transparent 1px); background-size:28px 28px,42px 42px; background-position:0 0,13px 15px; }
    .wrap { max-width:1120px; margin:auto; padding:28px 22px 60px; }
    header { display:flex; align-items:center; justify-content:space-between; gap:20px; margin-bottom:22px; }
    .brand { display:flex; align-items:center; gap:13px; }
    .logo { width:56px; height:56px; display:grid; place-items:center; color:white; background:var(--coral); border:3px solid var(--ink); border-radius:18px 18px 18px 5px; font-size:30px; box-shadow:4px 4px 0 var(--ink); }
    h1,h2,p { margin:0; } h1 { font-family:'Jua',sans-serif; font-size:clamp(28px,4vw,44px); line-height:1; } .tagline { color:var(--muted); margin-top:5px; font-size:16px; }
    .streak { padding:9px 14px; border:2px solid var(--ink); border-radius:14px; background:white; font-weight:700; white-space:nowrap; }
    .hero { display:grid; grid-template-columns:1.15fr .85fr; gap:20px; align-items:stretch; }
    .panel { background:rgba(255,255,255,.9); border:2px solid var(--ink); border-radius:24px; box-shadow:6px 6px 0 var(--ink); }
    .intro { padding:28px; position:relative; overflow:hidden; min-height:215px; background:#fff1c9; }
    .intro h2 { font-family:'Jua'; font-size:28px; margin-bottom:9px; max-width:460px; } .intro p { color:#566174; max-width:500px; line-height:1.5; }
    .flag { position:absolute; right:28px; bottom:20px; font-size:76px; transform:rotate(8deg); }
    .word-list { padding:20px; } .section-title { display:flex; justify-content:space-between; align-items:center; margin-bottom:13px; } .section-title h2 { font-family:'Jua'; font-size:22px; } .hint { color:var(--muted); font-size:14px; }
    .cards { display:grid; grid-template-columns:repeat(5,1fr); gap:10px; }
    .word-card { border:2px solid #cdd3da; background:white; border-radius:16px; padding:12px 5px 10px; cursor:pointer; color:var(--ink); font:inherit; transition:transform .16s, border-color .16s, background .16s; }
    .word-card:hover { transform:translateY(-3px); border-color:var(--coral); } .word-card.active { background:#e4f5ef; border-color:var(--mint); box-shadow:inset 0 -4px 0 var(--mint); }
    .emoji { display:block; font-size:28px; margin-bottom:2px; } .word { display:block; font-size:20px; font-weight:700; } .meaning { display:block; color:var(--muted); font-size:13px; }
    .lesson { display:grid; grid-template-columns:1.05fr .95fr; gap:20px; margin-top:22px; }
    .alphabet-panel { margin-top:22px; padding:22px; background:#fff; }
    .alphabet-grid { display:grid; grid-template-columns:repeat(13,1fr); gap:7px; }
    .letter-card { border:2px solid #d8dee5; border-radius:11px; padding:8px 2px 6px; background:#f8fbff; color:var(--ink); cursor:pointer; font:inherit; transition:transform .16s, border-color .16s, background .16s; }
    .letter-card:hover { transform:translateY(-3px); border-color:var(--blue); }
    .letter-card.active { background:#dff2ed; border-color:var(--mint); box-shadow:inset 0 -3px 0 var(--mint); }
    .letter-upper { display:block; font-size:25px; line-height:1; font-weight:700; color:var(--blue); }
    .letter-lower { display:block; color:var(--muted); font-weight:700; }
    .alphabet-detail { display:grid; grid-template-columns:150px 1fr auto; align-items:center; gap:18px; margin-top:18px; padding:17px 20px; border-radius:16px; background:#eef8f5; }
    .letter-big { display:flex; align-items:baseline; gap:8px; font-size:62px; line-height:1; font-weight:700; color:var(--coral); }
    .letter-big small { font-size:30px; color:var(--muted); }
    .letter-facts { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }
    .fact { padding-left:12px; border-left:3px solid var(--yellow); } .fact-label { display:block; color:var(--muted); font-size:13px; } .fact-value { display:block; font-weight:700; font-size:20px; } .letter-story { color:#566174; line-height:1.4; font-size:14px; }
    .letter-buttons { display:flex; flex-direction:column; gap:7px; } .letter-sound-btn { min-width:145px; border:2px solid var(--ink); border-radius:11px; padding:8px 10px; background:var(--yellow); color:var(--ink); cursor:pointer; font:700 14px 'Baloo 2'; }
    .word-stage { padding:27px; background:#e8f4ff; } .eyebrow { color:var(--blue); font-weight:700; letter-spacing:.04em; } .big-word { font-size:clamp(58px,9vw,98px); line-height:.95; font-weight:700; margin:8px 0 4px; color:var(--blue); } .ipa { font-size:27px; color:var(--coral); font-weight:700; }
    .sound-btn { margin-top:18px; border:2px solid var(--ink); background:var(--yellow); border-radius:14px; padding:12px 18px; color:var(--ink); cursor:pointer; font:700 17px 'Baloo 2'; box-shadow:3px 3px 0 var(--ink); } .sound-btn:active { transform:translate(2px,2px); box-shadow:1px 1px 0 var(--ink); }
    .sound-note { color:var(--muted); font-size:13px; margin-top:12px; }
    .details { padding:24px; } .details h2 { font-family:'Jua'; font-size:23px; margin-bottom:15px; } .chunk-row { display:flex; flex-wrap:wrap; align-items:center; gap:8px; margin-bottom:20px; } .chunk { padding:7px 12px; border-radius:10px; color:white; font-size:22px; font-weight:700; background:var(--coral); } .chunk:nth-child(3) { background:var(--blue); } .chunk:nth-child(5) { background:var(--mint); } .plus { color:var(--muted); font-size:22px; }
    .story { background:#fff6dd; border-left:6px solid var(--yellow); border-radius:5px 12px 12px 5px; padding:14px 16px; line-height:1.5; color:#4c5768; } .story strong { color:var(--ink); }
    .quiz { margin-top:22px; padding:22px 25px; display:flex; align-items:center; justify-content:space-between; gap:16px; background:#fce9e5; } .quiz h2 { font-family:'Jua'; font-size:22px; } .quiz p { color:var(--muted); } .options { display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end; } .option { border:2px solid var(--ink); border-radius:12px; background:white; padding:10px 15px; color:var(--ink); cursor:pointer; font:700 17px 'Baloo 2'; } .option:hover { background:var(--yellow); } .result { min-width:90px; font-weight:700; color:var(--coral); }
    @media (max-width:760px) { .wrap { padding:18px 14px 40px; } header { align-items:flex-start; } .streak { font-size:13px; padding:7px 9px; } .hero,.lesson { grid-template-columns:1fr; } .cards { grid-template-columns:repeat(3,1fr); } .alphabet-grid { grid-template-columns:repeat(7,1fr); } .alphabet-detail { grid-template-columns:1fr; gap:12px; } .letter-facts { grid-template-columns:repeat(3,1fr); } .letter-buttons { flex-direction:row; flex-wrap:wrap; } .intro { min-height:190px; } .flag { right:18px; bottom:10px; font-size:60px; } .quiz { align-items:flex-start; flex-direction:column; } .options { justify-content:flex-start; } }
    @media (max-width:400px) { .cards { grid-template-columns:repeat(2,1fr); } .alphabet-grid { grid-template-columns:repeat(5,1fr); } .letter-facts { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <main class="wrap">
    <header>
      <div class="brand"><div class="logo">A</div><div><h1>파닉스 탐험대</h1><p class="tagline">단어 속 소리 보물찾기</p></div></div>
      <div class="streak">⭐ 오늘의 별 <span id="stars">0</span>개</div>
    </header>
    <section class="hero">
      <div class="panel intro"><h2>글자 친구들이 만나면<br>어떤 소리가 날까?</h2><p>단어를 눌러 소리를 듣고, 알파벳이 왜 그렇게 읽히는지 탐험해 봐요!</p><div class="flag">🧭</div></div>
      <div class="panel word-list"><div class="section-title"><h2>오늘의 탐험 단어</h2><span class="hint">단어를 눌러 보세요</span></div><div class="cards" id="cards"></div></div>
    </section>
    <section class="panel alphabet-panel">
      <div class="section-title"><h2>🔤 알파벳 한 글자 탐험</h2><span class="hint">대문자와 소리를 함께 익혀요</span></div>
      <div class="alphabet-grid" id="alphabetGrid"></div>
      <div class="alphabet-detail" id="alphabetDetail"></div>
    </section>
    <section class="lesson">
      <div class="panel word-stage"><div class="eyebrow">NOW EXPLORING</div><div class="big-word" id="bigWord">cat</div><div class="ipa" id="ipa">/kæt/</div><button class="sound-btn" id="soundBtn">🔊 소리 듣기</button><p class="sound-note">브라우저의 영어 목소리로 천천히 읽어 줘요.</p></div>
      <div class="panel details"><h2>🔎 소리 조각 맞추기</h2><div class="chunk-row" id="chunks"></div><div class="story" id="story"></div></div>
    </section>
    <section class="panel quiz"><div><h2>🎯 탐험 퀴즈</h2><p id="question">cat의 첫 소리는 무엇일까요?</p></div><div class="options" id="options"></div><div class="result" id="result"></div></section>
  </main>
  <script>
    const lessons = [
      { word:'cat', meaning:'고양이', emoji:'🐱', ipa:'/kæt/', chunks:[['c','/k/'],['a','/æ/'],['t','/t/']], story:'고양이 <strong>cat</strong>이 “캣!” 하고 살금살금 걸어요. <strong>c</strong>는 여기서 컵의 첫 소리처럼 /k/, <strong>a</strong>는 입을 크게 벌리는 /æ/예요.', answer:'/k/' },
      { word:'cake', meaning:'케이크', emoji:'🍰', ipa:'/keɪk/', chunks:[['c','/k/'],['a_e','/eɪ/'],['k','/k/']], story:'케이크 <strong>cake</strong>는 마법의 e가 숨어 있어요. a와 e가 손을 잡으면 a가 자기 이름처럼 “에이!” /eɪ/ 하고 길게 말해요.', answer:'/k/' },
      { word:'ship', meaning:'배', emoji:'🚢', ipa:'/ʃɪp/', chunks:[['sh','/ʃ/'],['i','/ɪ/'],['p','/p/']], story:'배 <strong>ship</strong>가 바다를 지나며 “쉬이익!” 소리를 내요. <strong>s</strong>와 <strong>h</strong>가 붙은 <strong>sh</strong>는 “쉬” /ʃ/라는 한 팀 소리예요.', answer:'/ʃ/' },
      { word:'fish', meaning:'물고기', emoji:'🐟', ipa:'/fɪʃ/', chunks:[['f','/f/'],['i','/ɪ/'],['sh','/ʃ/']], story:'물고기 <strong>fish</strong>가 물속에서 “퓌시!” 헤엄쳐요. 끝의 <strong>sh</strong>는 입술을 살짝 내밀고 바람을 보내는 /ʃ/예요.', answer:'/f/' },
      { word:'moon', meaning:'달', emoji:'🌙', ipa:'/muːn/', chunks:[['m','/m/'],['oo','/uː/'],['n','/n/']], story:'달 <strong>moon</strong>은 밤하늘에서 “우우” 노래해요. <strong>oo</strong>가 만나면 길고 둥근 /uː/ 소리가 자주 나요.', answer:'/m/' },
      { word:'rain', meaning:'비', emoji:'🌧️', ipa:'/reɪn/', chunks:[['r','/r/'],['ai','/eɪ/'],['n','/n/']], story:'비 <strong>rain</strong>가 “레인!” 하고 내려요. <strong>ai</strong>는 기차처럼 함께 달리며 /eɪ/ 소리를 만들어요.', answer:'/r/' },
      { word:'bike', meaning:'자전거', emoji:'🚲', ipa:'/baɪk/', chunks:[['b','/b/'],['i_e','/aɪ/'],['k','/k/']], story:'자전거 <strong>bike</strong>를 타면 “바이크!” 신나요. 끝의 e는 조용히 서 있지만 i를 자기 이름 /aɪ/으로 바꿔 줘요.', answer:'/b/' },
      { word:'tree', meaning:'나무', emoji:'🌳', ipa:'/triː/', chunks:[['tr','/tr/'],['ee','/iː/']], story:'나무 <strong>tree</strong>가 “트리!” 자라나요. <strong>ee</strong>는 환하게 웃으며 길쭉한 /iː/ 소리를 내는 쌍둥이예요.', answer:'/tr/' },
      { word:'book', meaning:'책', emoji:'📚', ipa:'/bʊk/', chunks:[['b','/b/'],['oo','/ʊ/'],['k','/k/']], story:'책 <strong>book</strong>을 펼치면 “북!” 이야기가 시작돼요. 같은 <strong>oo</strong>라도 moon의 /uː/보다 짧고 가벼운 /ʊ/가 될 때가 있어요.', answer:'/b/' },
      { word:'sun', meaning:'해', emoji:'☀️', ipa:'/sʌn/', chunks:[['s','/s/'],['u','/ʌ/'],['n','/n/']], story:'해 <strong>sun</strong>이 “썬!” 하고 반짝여요. <strong>u</strong>는 여기서 우가 아니라 짧고 힘찬 /ʌ/ 소리가 나요.', answer:'/s/' }
    ];
    const alphabet = [
      ['A','a','/eɪ/','/æ/','apple','사과','aah'], ['B','b','/biː/','/b/','bus','버스','buh'], ['C','c','/siː/','/k/','cat','고양이','kuh'], ['D','d','/diː/','/d/','dog','개','duh'], ['E','e','/iː/','/ɛ/','egg','달걀','eh'], ['F','f','/ɛf/','/f/','fish','물고기','fff'], ['G','g','/dʒiː/','/g/','goat','염소','guh'], ['H','h','/eɪtʃ/','/h/','hat','모자','huh'], ['I','i','/aɪ/','/ɪ/','igloo','이글루','ih'], ['J','j','/dʒeɪ/','/dʒ/','jam','잼','juh'], ['K','k','/keɪ/','/k/','kite','연','kuh'], ['L','l','/ɛl/','/l/','lion','사자','lll'], ['M','m','/ɛm/','/m/','moon','달','mmm'], ['N','n','/ɛn/','/n/','nest','둥지','nnn'], ['O','o','/oʊ/','/ɒ/','octopus','문어','aw'], ['P','p','/piː/','/p/','pig','돼지','puh'], ['Q','q','/kjuː/','/kw/','queen','여왕','kwuh'], ['R','r','/ɑːr/','/r/','rain','비','ruh'], ['S','s','/ɛs/','/s/','sun','해','sss'], ['T','t','/tiː/','/t/','tree','나무','tuh'], ['U','u','/juː/','/ʌ/','umbrella','우산','uh'], ['V','v','/viː/','/v/','van','승합차','vuh'], ['W','w','/ˈdʌbəl.juː/','/w/','web','거미줄','wuh'], ['X','x','/ɛks/','/ks/','fox','여우','ksss'], ['Y','y','/waɪ/','/j/','yo-yo','요요','yuh'], ['Z','z','/ziː/','/z/','zoo','동물원','zzz']
    ];
    let selected = lessons[0]; let stars = 0;
    const cards = document.querySelector('#cards');
    lessons.forEach((item, index) => { const button=document.createElement('button'); button.className='word-card' + (index===0?' active':''); button.innerHTML=`<span class="emoji">${item.emoji}</span><span class="word">${item.word}</span><span class="meaning">${item.meaning}</span>`; button.onclick=()=>selectLesson(item, button); cards.appendChild(button); });
    const alphabetGrid = document.querySelector('#alphabetGrid');
    alphabet.forEach((item, index) => { const button=document.createElement('button'); button.className='letter-card' + (index===0?' active':''); button.innerHTML=`<span class="letter-upper">${item[0]}</span><span class="letter-lower">${item[1]}</span>`; button.onclick=()=>selectLetter(item, button); alphabetGrid.appendChild(button); });
    function findBrightFemaleVoice() { const voices=speechSynthesis.getVoices(); const preferred=/Jenny|Aria|Samantha|Ava|Zira|Google US English|Karen|Victoria/i; return voices.find(voice=>preferred.test(voice.name) && /^en(-US|-GB)?/i.test(voice.lang)) || voices.find(voice=>/^en(-US|-GB)?/i.test(voice.lang)); }
    function speak(text, isPhonics=false) { if('speechSynthesis' in window) { speechSynthesis.cancel(); const voice=new SpeechSynthesisUtterance(text); voice.lang='en-US'; voice.rate=isPhonics?.7:.78; voice.pitch=isPhonics?1.28:1.18; const selectedVoice=findBrightFemaleVoice(); if(selectedVoice) voice.voice=selectedVoice; speechSynthesis.speak(voice); } else alert('이 브라우저에서는 소리를 지원하지 않아요.'); }
    function selectLetter(item, button) { document.querySelectorAll('.letter-card').forEach(card=>card.classList.remove('active')); button.classList.add('active'); document.querySelector('#alphabetDetail').innerHTML=`<div class="letter-big">${item[0]}<small>${item[1]}</small></div><div class="letter-facts"><div class="fact"><span class="fact-label">글자 이름</span><span class="fact-value">${item[2]}</span></div><div class="fact"><span class="fact-label">대표 파닉스 소리</span><span class="fact-value">${item[3]}</span></div><div class="fact"><span class="fact-label">예시 단어</span><span class="fact-value">${item[4]} <small>(${item[5]})</small></span></div><p class="letter-story">${item[0]}는 이름을 부르면 <strong>${item[2]}</strong>, 단어 속에서는 주로 <strong>${item[3]}</strong> 소리로 변신해요. ${item[4]}의 첫소리를 따라 말해 보세요!</p></div><div class="letter-buttons"><button class="letter-sound-btn" onclick="speak('${item[0]}')">🔊 이름 듣기</button><button class="letter-sound-btn" onclick="speak('${item[6]}', true)">👂 ${item[3]} 소리 듣기</button></div>`; }
    function selectLesson(item, button) { selected=item; document.querySelectorAll('.word-card').forEach(card=>card.classList.remove('active')); button.classList.add('active'); document.querySelector('#bigWord').textContent=item.word; document.querySelector('#ipa').textContent=item.ipa; document.querySelector('#story').innerHTML=item.story; document.querySelector('#result').textContent=''; document.querySelector('#question').textContent=`${item.word}의 첫 소리는 무엇일까요?`; document.querySelector('#chunks').innerHTML=item.chunks.map((chunk,index)=>`${index?' <span class="plus">+</span> ':''}<span class="chunk">${chunk[0]}<small>${chunk[1]}</small></span>`).join(''); document.querySelectorAll('.chunk small').forEach(s=>s.style.display='block'); setOptions(); }
    function setOptions() { const pool=['/k/','/ʃ/','/m/','/s/','/b/','/f/','/r/','/tr/']; const choices=[selected.answer,...pool.filter(value=>value!==selected.answer).sort(()=>Math.random()-.5).slice(0,2)].sort(()=>Math.random()-.5); document.querySelector('#options').innerHTML=choices.map(value=>`<button class="option" onclick="checkAnswer(this.textContent)">${value}</button>`).join(''); }
    function checkAnswer(answer) { const result=document.querySelector('#result'); if(answer===selected.answer) { result.textContent='정답! ⭐'; stars++; document.querySelector('#stars').textContent=stars; } else result.textContent='다시 소리 내어 볼까요?'; }
    document.querySelector('#soundBtn').onclick=()=>speak(selected.word);
    selectLesson(selected, document.querySelector('.word-card'));
    selectLetter(alphabet[0], document.querySelector('.letter-card'));
  </script>
</body>
</html>'''


class PageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), PageHandler)
    address = f"http://127.0.0.1:{server.server_port}"
    print(f"파닉스 탐험대를 열었습니다: {address}")
    threading.Timer(0.4, lambda: webbrowser.open(address)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n파닉스 탐험대를 닫았습니다.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()