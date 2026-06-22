<template>
  <nav class="navbar">
    <a href="#" class="navbar-brand" @click.prevent="showMain">
      <i class="fa-solid fa-dice"></i> 뭐할게임?
    </a>
    <div class="navbar-links">
      <a href="#" :class="{ active: view === 'main' || view === 'recommend' }" @click.prevent="showRecommend">
        <i class="fa-solid fa-link"></i> 추천
      </a>
      <button type="button" @click="openToolModal('penalty')">
        <i class="fa-regular fa-square"></i> 벌칙/순서
      </button>
      <a href="/community/"><i class="fa-regular fa-comment"></i> 커뮤니티</a>
      <a href="/accounts/login/">로그인</a>
      <a href="/accounts/signup/">회원가입</a>
    </div>
  </nav>

  <main class="container">
    <section v-if="view === 'main'">
      <div style="margin-bottom: 3rem;">
        <i class="fa-solid fa-dice" style="font-size: 3rem; color: #a491bc;"></i>
        <h1>뭐할게임?</h1>
        <p class="subtitle">5명이서 할 건 없다고? 여기 있음</p>
      </div>

      <div class="hero-actions">
        <button class="btn btn-yellow" @click="showRecommend">
          <i class="fa-solid fa-dice-d20"></i> 게임 추천받기
        </button>
        <button class="btn btn-red" @click="openToolModal('penalty')">
          <i class="fa-solid fa-skull"></i> 벌칙 뽑기
        </button>
        <button class="btn btn-brown" @click="openToolModal('turn')">
          <i class="fa-solid fa-users"></i> 순서 정하기
        </button>
      </div>
    </section>

    <section v-else>
      <div style="margin-bottom: 2rem;">
        <h2 style="color: var(--primary-color);">오늘 뭐하지?</h2>
        <p class="subtitle">상황이나 조건으로 골라보기</p>
      </div>

      <div class="panels">
        <div class="card panel">
          <h3>상황 맞춤 AI 추천</h3>
          <div class="ai-row">
            <input
              v-model="situation"
              type="text"
              class="input-field"
              placeholder="예: 초보자 4명이서 1시간 안에 끝나는 파티 게임"
              style="margin-bottom: 0;"
              @keyup.enter="getAIRecommend"
            />
            <button class="btn btn-brown" style="margin: 0; width: 80px; padding: 0;" @click="getAIRecommend">
              추천
            </button>
          </div>
          <div v-if="aiLoading" style="text-align: center; margin-top: 10px;">
            <i class="fa-solid fa-spinner fa-spin"></i> AI가 고민 중...
          </div>
          <div style="margin-top: 20px;">
            <div v-for="item in aiRecommendations" :key="item.title" class="ai-item" @click="openAiRecommendModal(item.title)">
              <strong style="color: var(--primary-color); text-decoration: underline;">{{ item.title }}</strong><br />
              <span style="font-size: 0.9rem; color: var(--text-light);">{{ item.reason }}</span>
            </div>
            <p v-if="aiError" style="color: red;">오류: {{ aiError }}</p>
          </div>
        </div>

        <div class="card panel">
          <h3>조건 필터로 찾기</h3>
          <div class="filter-row">
            <input v-model="filters.players" type="number" placeholder="인원(명)" class="input-field" @change="fetchFilteredGames" @keyup.enter="fetchFilteredGames" />
            <input v-model="filters.time" type="number" placeholder="시간(분 이하)" class="input-field" @change="fetchFilteredGames" @keyup.enter="fetchFilteredGames" />
            <select v-model="filters.difficulty" class="input-field" @change="fetchFilteredGames">
              <option value="">난이도 전체</option>
              <option value="easy">쉬움</option>
              <option value="medium">보통</option>
              <option value="hard">어려움</option>
            </select>
          </div>
          <div v-if="filterLoading" style="text-align: center;">
            <i class="fa-solid fa-spinner fa-spin"></i> 검색 중...
          </div>
        </div>
      </div>

      <div class="games-grid">
        <div v-for="game in games" :key="game.game_id" class="card game-card" @click="openGameModal(game.game_id, game.title)">
          <h4>{{ game.title }}</h4>
          <p>순위: {{ game.rank }}</p>
          <p>출시: {{ game.released_year }}</p>
        </div>
      </div>

      <div style="margin-top: 2rem;">
        <button class="btn btn-outline" @click="showMain">메인으로 돌아가기</button>
      </div>
    </section>
  </main>

  <div v-if="toolModal" class="modal-overlay" @click.self="closeToolModal">
    <div class="modal-content">
      <button class="modal-close" type="button" @click="closeToolModal">&times;</button>
      <div class="tool-tabs">
        <button class="btn" :class="toolModal === 'penalty' ? 'btn-red' : 'btn-brown'" style="width: auto; padding: 0.5rem 1rem; font-size: 1rem;" @click="openToolModal('penalty')">
          벌칙 뽑기
        </button>
        <button class="btn" :class="toolModal === 'turn' ? 'btn-red' : 'btn-brown'" style="width: auto; padding: 0.5rem 1rem; font-size: 1rem;" @click="openToolModal('turn')">
          순서 정하기
        </button>
      </div>

      <template v-if="toolModal === 'penalty'">
        <h2 style="color: var(--primary-color);">오늘의 희생자는?</h2>
        <p style="color: var(--text-light);">불만 없기 약속</p>
        <div class="card tool-result">
          <i class="fa-regular fa-hand" style="font-size: 3rem; color: var(--text-light); margin-bottom: 10px;"></i>
          <p style="font-weight: bold; color: var(--text-light);">
            <span v-if="penaltyResult" style="color: var(--accent-color); font-size: 1.5rem;">{{ penaltyResult }}</span>
            <span v-else>아래 버튼을 눌러 뽑으세요</span>
          </p>
        </div>
        <button class="btn btn-red" @click="drawPenalty">뽑기!</button>
      </template>

      <template v-else>
        <h2 style="color: var(--primary-color);">누가 먼저 할래?</h2>
        <p style="color: var(--text-light);">공평하게 랜덤으로 결정</p>
        <input v-model.number="playerCount" type="number" class="input-field" placeholder="몇 명인가요?" min="2" max="10" style="text-align: center; width: 50%;" />
        <div class="card tool-result">
          <p style="font-weight: bold; color: var(--text-light);">
            <span v-if="turnResult" style="color: var(--primary-color); font-size: 1.2rem;">순서: {{ turnResult.join(' -> ') }}</span>
            <span v-else>인원을 입력하고 뽑아주세요</span>
          </p>
        </div>
        <button class="btn btn-brown" @click="decideTurn">뽑기!</button>
      </template>
    </div>
  </div>

  <div v-if="gameModal.open" class="modal-overlay" @click.self="closeGameDetail">
    <div class="modal-content wide">
      <button class="modal-close" type="button" @click="closeGameDetail">&times;</button>
      <h2 style="color: var(--primary-color); margin-bottom: 5px;">{{ gameModal.title }}</h2>
      <div v-if="gameModal.loading"><i class="fa-solid fa-spinner fa-spin"></i> 게임 정보를 불러오는 중...</div>
      <div v-else style="text-align: left;">
        <div class="detail-grid" style="margin-top: 20px;">
          <div style="flex: 1;">
            <div v-if="gameModal.details">
              <h4>기본 정보</h4>
              <p>인원: {{ gameModal.details.min_players }} ~ {{ gameModal.details.max_players }}명</p>
              <p>시간: {{ gameModal.details.playing_time }}분</p>
              <p>난이도: {{ Number(gameModal.details.weight).toFixed(1) }} / 5.0</p>
            </div>

            <h4 style="margin-top: 20px; color: var(--accent-color);">AI 룰 요약</h4>
            <div style="background: var(--box-bg); padding: 10px; border-radius: 8px; font-size: 0.9rem; white-space: pre-line;">
              <i v-if="gameModal.guideLoading" class="fa-solid fa-spinner fa-spin"></i>
              {{ gameModal.summary || (gameModal.guideLoading ? '요약 중...' : '요약을 불러오지 못했습니다.') }}
            </div>
          </div>
          <div style="flex: 1;">
            <h4>유튜브 영상 (룰 가이드)</h4>
            <div class="youtube-box">
              <i v-if="gameModal.guideLoading" class="fa-solid fa-spinner fa-spin"></i>
              <iframe
                v-else-if="gameModal.youtubeVideoId"
                width="100%"
                height="100%"
                :src="`https://www.youtube.com/embed/${gameModal.youtubeVideoId}`"
                frameborder="0"
                allowfullscreen
                style="border-radius: 8px;"
              ></iframe>
              <span v-else>영상 없음</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

const view = ref('main')
const games = ref([])
const filters = reactive({ players: '', time: '', difficulty: '' })
const filterLoading = ref(false)
const situation = ref('')
const aiLoading = ref(false)
const aiError = ref('')
const aiRecommendations = ref([])
const toolModal = ref('')
const penaltyResult = ref('')
const playerCount = ref(null)
const turnResult = ref([])
const gameModal = reactive({
  open: false,
  loading: false,
  guideLoading: false,
  title: '',
  details: null,
  summary: '',
  youtubeVideoId: ''
})

const penalties = ['핸디캡 받기', '설거지 하기', '음료수 사기', '뒷정리 하기', '한 턴 쉬기', '무사 통과!']

onMounted(() => {
  fetchFilteredGames()
})

function showMain() {
  view.value = 'main'
}

function showRecommend() {
  view.value = 'recommend'
  if (!games.value.length) fetchFilteredGames()
}

async function fetchFilteredGames() {
  filterLoading.value = true
  const params = new URLSearchParams()
  if (filters.players) params.append('players', filters.players)
  if (filters.time) params.append('time', filters.time)
  if (filters.difficulty) params.append('difficulty', filters.difficulty)

  try {
    const response = await fetch(`/boardgames/filter/?${params.toString()}`)
    const data = await response.json()
    games.value = data.games || []
  } finally {
    filterLoading.value = false
  }
}

async function getAIRecommend() {
  if (!situation.value) {
    alert('상황을 입력해주세요.')
    return
  }

  aiLoading.value = true
  aiError.value = ''
  aiRecommendations.value = []

  try {
    const response = await fetch('/boardgames/recommend/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ situation: situation.value })
    })
    const data = await response.json()
    if (data.error) {
      aiError.value = data.error
      return
    }
    aiRecommendations.value = data.recommendations || []
  } catch (error) {
    aiError.value = error.message
  } finally {
    aiLoading.value = false
  }
}

function openToolModal(type) {
  toolModal.value = type
}

function closeToolModal() {
  toolModal.value = ''
}

function drawPenalty() {
  penaltyResult.value = penalties[Math.floor(Math.random() * penalties.length)]
}

function decideTurn() {
  if (!playerCount.value || playerCount.value < 2) {
    alert('2명 이상 입력해주세요!')
    return
  }

  const arr = Array.from({ length: playerCount.value }, (_, i) => i + 1)
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  turnResult.value = arr
}

async function openGameModal(gameId, title) {
  resetGameModal(title)
  gameModal.loading = true

  try {
    const response = await fetch(`/boardgames/api/${gameId}/details/`)
    if (!response.ok) throw new Error('Details not found')
    gameModal.details = await response.json()
    gameModal.loading = false
    fetchGameSmartGuide(gameId)
  } catch {
    gameModal.loading = false
    gameModal.summary = '상세 정보가 데이터베이스에 없습니다.'
  }
}

async function fetchGameSmartGuide(gameId) {
  gameModal.guideLoading = true
  try {
    const response = await fetch(`/boardgames/${gameId}/recommend/`)
    const data = await response.json()
    gameModal.summary = data.summary || ''
    gameModal.youtubeVideoId = data.youtube_videoId || ''
  } finally {
    gameModal.guideLoading = false
  }
}

async function openAiRecommendModal(title) {
  resetGameModal(`${title} (AI 추천)`)
  gameModal.loading = true
  gameModal.guideLoading = true

  try {
    const response = await fetch(`/boardgames/api/details_by_title/?title=${encodeURIComponent(title)}`)
    const data = await response.json()
    gameModal.summary = data.ai_summary || ''
    gameModal.youtubeVideoId = data.youtube_videoId || ''
  } finally {
    gameModal.loading = false
    gameModal.guideLoading = false
  }
}

function closeGameDetail() {
  gameModal.open = false
}

function resetGameModal(title) {
  gameModal.open = true
  gameModal.title = title
  gameModal.details = null
  gameModal.summary = ''
  gameModal.youtubeVideoId = ''
}
</script>
