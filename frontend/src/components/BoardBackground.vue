<template>
  <div class="board-background">
    <!-- 기본 격자 무늬 배경 -->
    <svg class="board-grid-svg" width="100%" height="100%">
      <defs>
        <pattern id="board-grid" width="80" height="80" patternUnits="userSpaceOnUse">
          <rect width="80" height="80" fill="none" stroke="var(--primary-color)" stroke-width="2" />
        </pattern>
      </defs>
      <!-- 격자 채우기 -->
      <rect width="100%" height="100%" fill="url(#board-grid)" opacity="0.12" />
      
      <!-- 점수 칸(Score Track) 역할을 하는 큰 점선 테두리 -->
      <rect width="100%" height="100%" fill="none" stroke="var(--primary-color)" stroke-width="40" stroke-dasharray="40 40" opacity="0.08" />
    </svg>




  </div>
</template>

<script setup>
// 거대한 보드게임 판 背景 Component
</script>

<style scoped>
.board-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -9999;
  pointer-events: none;
  overflow: hidden;
}

/* 그리드 및 스코어 트랙 */
.board-grid-svg {
  position: absolute;
  top: 0;
  left: 0;
}




</style>
