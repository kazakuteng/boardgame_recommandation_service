<template>
  <div class="doodle-container">
    <!-- Top Left: Meeple -->
    <svg class="doodle doodle-1" viewBox="0 0 100 100" width="100" height="100">
      <path d="M50 15 C60 15, 65 25, 50 35 C35 25, 40 15, 50 15 Z M50 35 C70 35, 80 45, 85 65 L95 90 L60 90 L50 75 L40 90 L5 90 L15 65 C20 45, 30 35, 50 35 Z" stroke="var(--primary-color)" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>

    <!-- Bottom Left: Star -->
    <svg class="doodle doodle-2" viewBox="0 0 100 100" width="80" height="80">
      <polygon points="50,10 61,35 88,35 66,51 74,77 50,61 26,77 34,51 12,35 39,35" stroke="var(--primary-color)" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>

    <!-- Top Right: Dice -->
    <svg class="doodle doodle-3" viewBox="0 0 100 100" width="90" height="90">
      <rect x="15" y="15" width="70" height="70" rx="10" stroke="var(--primary-color)" stroke-width="4" fill="none" stroke-linejoin="round"/>
      <circle cx="35" cy="35" r="4" stroke="var(--primary-color)" stroke-width="3" fill="none"/>
      <circle cx="65" cy="65" r="4" stroke="var(--primary-color)" stroke-width="3" fill="none"/>
      <circle cx="50" cy="50" r="4" stroke="var(--primary-color)" stroke-width="3" fill="none"/>
    </svg>

    <!-- Middle Right: Card -->
    <svg class="doodle doodle-4" viewBox="0 0 100 100" width="70" height="90">
      <rect x="15" y="10" width="70" height="80" rx="5" stroke="var(--primary-color)" stroke-width="4" fill="none" stroke-linejoin="round"/>
      <rect x="25" y="20" width="50" height="60" rx="3" stroke="var(--primary-color)" stroke-width="3" fill="none" stroke-linejoin="round"/>
    </svg>

    <!-- Bottom Right: Arrow -->
    <svg class="doodle doodle-5" viewBox="0 0 100 100" width="80" height="80">
      <path d="M20 50 Q40 20 80 40" stroke="var(--primary-color)" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M60 30 L80 40 L70 60" stroke="var(--primary-color)" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>

    <!-- Middle Left: Check -->
    <svg class="doodle doodle-6" viewBox="0 0 100 100" width="80" height="80">
      <path d="M20 50 L40 70 L80 20" stroke="var(--primary-color)" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>
    
    <!-- Top Center-ish: Bubble -->
    <svg class="doodle doodle-7" viewBox="0 0 100 100" width="80" height="80">
      <path d="M10 30 C10 10, 90 10, 90 30 C90 50, 60 60, 60 80 L50 60 C10 60, 10 50, 10 30 Z" stroke="var(--primary-color)" stroke-width="3" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>
  </div>
</template>

<script setup>
// 이 컴포넌트는 순수 CSS 애니메이션으로 동작하며 무거운 JS 렌더링 로직이 없습니다.
// 모바일/데스크탑 모두에서 가볍게 백그라운드로 돌아갑니다.
</script>

<style scoped>
.doodle-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none; /* 클릭 방해 금지 */
  z-index: -10; /* 모든 컨텐츠 뒤로 */
  overflow: hidden;
  opacity: 0.08; /* 은은한 투명도 8% */
}

/* 
  각 아이콘별로 animation 딜레이를 주어 번갈아가면서 나타남 
  총 주기: 20s
*/
.doodle {
  position: absolute;
  opacity: 0;
  animation: sketch 20s infinite ease-in-out;
}

.doodle path, .doodle polygon, .doodle rect, .doodle circle {
  stroke-dasharray: 400; /* 선 긋기용 */
  stroke-dashoffset: 400;
  animation: draw 20s infinite ease-in-out;
}

/* 배치 및 딜레이 설정 */
.doodle-1 { top: 15%; left: 8%; animation-delay: 0s; transform: rotate(-10deg); }
.doodle-1 * { animation-delay: 0s; }

.doodle-2 { bottom: 15%; left: 10%; animation-delay: 3s; transform: rotate(15deg); }
.doodle-2 * { animation-delay: 3s; }

.doodle-3 { top: 20%; right: 10%; animation-delay: 6s; transform: rotate(5deg); }
.doodle-3 * { animation-delay: 6s; }

.doodle-4 { top: 55%; right: 7%; animation-delay: 9s; transform: rotate(-5deg); }
.doodle-4 * { animation-delay: 9s; }

.doodle-5 { bottom: 12%; right: 18%; animation-delay: 12s; transform: rotate(-25deg); }
.doodle-5 * { animation-delay: 12s; }

.doodle-6 { top: 45%; left: 5%; animation-delay: 15s; transform: rotate(20deg); }
.doodle-6 * { animation-delay: 15s; }

.doodle-7 { top: 5%; left: 45%; animation-delay: 18s; transform: rotate(-5deg); }
.doodle-7 * { animation-delay: 18s; }


@keyframes sketch {
  0% { opacity: 0; }
  10% { opacity: 1; }
  40% { opacity: 1; } /* 충분히 머무름 */
  50% { opacity: 0; }
  100% { opacity: 0; } /* 나머지 시간 동안 안보임 */
}

@keyframes draw {
  0% { stroke-dashoffset: 400; }
  15% { stroke-dashoffset: 0; } /* 3초만에 그려짐 */
  100% { stroke-dashoffset: 0; }
}

@media (max-width: 768px) {
  /* 모바일 환경에서는 구석으로 밀어넣어 중앙 침범을 막음 */
  .doodle-1 { left: -5%; }
  .doodle-2 { left: -5%; }
  .doodle-3 { right: -5%; }
  .doodle-4 { right: -5%; }
}
</style>
