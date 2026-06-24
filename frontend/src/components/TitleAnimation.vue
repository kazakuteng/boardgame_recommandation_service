<template>
  <div class="title-exploration">
    <svg class="map-path-svg" viewBox="0 0 350 120" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <mask id="path-mask">
          <rect class="mask-rect" x="0" y="0" width="350" height="120" fill="white" />
        </mask>
      </defs>
      <!-- 은은한 브라운 톤의 탐험 궤적 (보물지도 점선) -->
      <path
        d="M 10 40 Q 40 90 70 40 T 130 40 T 190 40 T 250 40 T 310 40"
        fill="none"
        stroke="var(--primary-color)"
        stroke-width="3"
        stroke-dasharray="6 6"
        stroke-linecap="round"
        mask="url(#path-mask)"
      />
    </svg>
    
    <!-- 경로를 따라 이동하는 주사위 말 -->
    <div class="pawn">
      <i class="fa-solid fa-dice"></i>
    </div>
    
    <!-- 순차적으로 나타나는 타이틀 글자 -->
    <h1 class="animated-title">
      <span class="char char-1">뭐</span>
      <span class="char char-2">할</span>
      <span class="char char-3">게</span>
      <span class="char char-4">임</span>
      <span class="char char-5">?</span>
    </h1>
  </div>
</template>

<script setup>
// 순수 CSS 및 SVG 애니메이션이므로 추가 스크립트 불필요
</script>

<style scoped>
.title-exploration {
  position: relative;
  width: 350px;
  height: 120px;
  margin: 0 auto 1.5rem auto; /* 기존 h1 간격 유지 */
}

/* SVG 맵 캔버스 - 15초 주기로 무한 반복 */
.map-path-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0;
  animation: mapFade 15s infinite;
}

@keyframes mapFade {
  0% { opacity: 0.6; }
  16.66% { opacity: 0.6; }  /* 2.5s: 그리기 완료 */
  23.33% { opacity: 0.6; }  /* 3.5s: 대기 */
  30% { opacity: 0; }       /* 4.5s: 페이드아웃 */
  100% { opacity: 0; }      /* 15s까지 숨김 유지 */
}

/* 선이 손으로 그려지듯 펼쳐지는 마스크 애니메이션 */
.mask-rect {
  transform-origin: left;
  animation: mapDraw 15s infinite;
}

@keyframes mapDraw {
  0% { transform: scaleX(0); }
  16.66% { transform: scaleX(1); }
  100% { transform: scaleX(1); } /* 다음 루프까지 상태 유지 */
}

/* 주사위(말) 설정 및 이동 애니메이션 */
.pawn {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 2.5rem;
  color: #a491bc;
  offset-path: path("M 10 40 Q 40 90 70 40 T 130 40 T 190 40 T 250 40 T 310 40");
  offset-rotate: 0deg;
  animation: pawnMove 15s infinite;
  z-index: 2;
}

.pawn i {
  position: absolute;
  top: -1.25rem;
  left: -1.25rem;
  text-shadow: 2px 2px 0 #fff, -2px -2px 0 #fff;
}

@keyframes pawnMove {
  0% { offset-distance: 0%; opacity: 0; transform: scale(0.5); }
  1% { opacity: 1; transform: scale(1); }
  16.66% { offset-distance: 100%; opacity: 1; transform: scale(1); } /* 2.5s: 도착 */
  23.33% { offset-distance: 100%; opacity: 1; transform: scale(1); } /* 3.5s: 대기 */
  30% { offset-distance: 100%; opacity: 0; transform: scale(1); } /* 4.5s: 페이드아웃 */
  100% { offset-distance: 100%; opacity: 0; transform: scale(1); } /* 15s까지 숨김 유지 */
}

/* 타이틀 텍스트 설정 (최초 1회만 실행되어 영구 유지) */
.animated-title {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

.char {
  position: absolute;
  top: 50px;
  transform: translateX(-50%) scale(1);
  opacity: 0;
  font-size: 3.5rem;
  font-weight: 900;
  color: var(--primary-color);
  z-index: 1;
}

/* 주사위가 지나갈 때 번쩍거리는 효과를 위한 다중 애니메이션 */
.char-1 { 
  left: 70px;  
  animation: 
    popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.5s forwards,
    charFlash 15s infinite 0.5s; 
}
.char-2 { 
  left: 130px; 
  animation: 
    popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) 1.0s forwards,
    charFlash 15s infinite 1.0s; 
}
.char-3 { 
  left: 190px; 
  animation: 
    popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) 1.5s forwards,
    charFlash 15s infinite 1.5s; 
}
.char-4 { 
  left: 250px; 
  animation: 
    popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) 2.0s forwards,
    charFlash 15s infinite 2.0s; 
}
.char-5 { 
  left: 310px; 
  animation: 
    popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) 2.5s forwards,
    charFlash 15s infinite 2.5s; 
}

/* 최초 등장 팝업 */
@keyframes popIn {
  0% { opacity: 0; transform: translateX(-50%) scale(0.5); }
  70% { opacity: 1; transform: translateX(-50%) scale(1.1); }
  100% { opacity: 1; transform: translateX(-50%) scale(1); }
}

/* 주사위가 지나갈 때 네온 번쩍임 */
@keyframes charFlash {
  0% { text-shadow: none; color: var(--primary-color); }
  1% { text-shadow: 0 0 15px #a491bc, 0 0 30px #eadecc; color: #a491bc; }
  3% { text-shadow: none; color: var(--primary-color); }
  100% { text-shadow: none; color: var(--primary-color); }
}
</style>
