<template>
  <div class="home-page">
    <!-- 1. 히어로 섹션 -->
    <section
      v-if="!isLogin"
      class="hero"
      :style="{ backgroundImage: `url(${heroImage})` }"
    >
      <div class="hero-content">
        <h1>FinTrust</h1>
        <p>당신의 똑똑한 금융 파트너</p>
        <RouterLink to="/login" class="btn-primary">지금 시작하기</RouterLink>
      </div>
    </section>

    <!-- 2. 대시보드 히어로 (로그인 후) -->
    <section v-else class="hero dashboard">
      <div class="hero-content">
        <h1>환영합니다, {{ userName }}님!</h1>
        <p>FinTrust의 다양한 기능을 만나보세요</p>
        <div class="dash-buttons">
          <RouterLink to="/bank-search" class="btn-outline">은행 검색</RouterLink>
          <RouterLink to="/community" class="btn-outline">커뮤니티</RouterLink>
          <RouterLink to="/products" class="btn-outline">금리 비교</RouterLink>
          <RouterLink to="/profile" class="btn-outline">내 정보</RouterLink>
        </div>
      </div>
    </section>

    <!-- 3. 통합 기능 섹션 -->
    <section class="features">
      <h2>주요 기능</h2>
      <div class="feature-grid">
        <div class="feature-box" v-for="feature in features" :key="feature.title">
          <img :src="feature.img" :alt="feature.title" />
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </div>
      </div>
    </section>

    <!-- 4. 왜 FinTrust인가요? -->
    <section class="benefits">
      <h2>왜 FinTrust인가요?</h2>
      <ul class="benefit-list">
        <li v-for="item in benefits" :key="item.title">
          <strong>{{ item.title }}</strong>
          <p>{{ item.desc }}</p>
        </li>
      </ul>
    </section>

    <!-- 5. 콜투액션 -->
    <section class="cta">
      <RouterLink v-if="!isLogin" to="/signup" class="btn-primary">회원가입 하기</RouterLink>
      <RouterLink v-else to="/community" class="btn-primary">커뮤니티 둘러보기</RouterLink>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import heroImage from '@/assets/hero.jpg'
import feature1 from '@/assets/feature1.png'
import feature2 from '@/assets/feature2.png'
import feature3 from '@/assets/feature3.png'
import feature4 from '@/assets/feature4.png'
import feature5 from '@/assets/feature5.png'

const store = useUserStore()
const isLogin = computed(() => store.isLogin)
const userName = ref('')

const features = [
  { img: feature1, title: 'AI 상품 추천', desc: '나만의 금융 패턴을 분석해 딱 맞는 상품을 추천합니다.' },
  { img: feature2, title: '커뮤니티', desc: '질문과 꿀팁을 나누며 함께 성장하세요.' },
  { img: feature3, title: '차트 확인', desc: '가입한 상품을 그래프로 한눈에 비교·분석.' },
  { img: feature4, title: '은행 검색', desc: '내 위치 근처 은행의 금리와 혜택을 확인.' },
  { img: feature5, title: '현물 시세', desc: '금·은 등 현물 가격을 실시간 그래프로.' }
]

const benefits = [
  { title: '데이터 보안', desc: '은행 수준의 암호화로 개인정보를 안전하게 보호합니다.' },
  { title: '맞춤형 경험', desc: '내 금융 이력을 기반으로 개인화된 추천을 제공합니다.' },
  { title: '멀티 디바이스 지원', desc: '웹·모바일 어디서든 일관된 경험을 누리세요.' },
  { title: '24/7 고객지원', desc: '언제든 문의하시면 빠르게 도움을 드립니다.' }
]

onMounted(async () => {
  if (isLogin.value) {
    try {
      const { data } = await api.get('/accounts/profile/')
      userName.value = data.username
    } catch {
      userName.value = store.username || 'User'
    }
  }
})
</script>

<style>
/* 전역 테마 변수 */
:root {
  --color-primary: #01c878;
  --color-primary-dark: #019e65;
  --color-secondary: #5c16ff;
  --color-bg-light: #f5f7fa;
  --color-bg: #ffffff;
  --color-text: #333333;
  --transition-speed: 0.3s;
}
</style>

<style scoped>
.home-page {
  font-family: 'Noto Sans KR', sans-serif;
  color: var(--color-text);
}

/* 히어로 공통 */
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  background-size: cover;
  position: relative;
  transition: background var(--transition-speed);
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  animation: fadeOverlay 1s ease;
}

@keyframes fadeOverlay {
  from { background: rgba(0, 0, 0, 0); }
  to   { background: rgba(0, 0, 0, 0.4); }
}

.hero-content {
  position: relative;
  text-align: center;
  color: #fff;
  padding: 2rem;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: fadeInUp 0.6s ease-out;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 대시보드 히어로 */
.hero.dashboard {
  background: var(--color-bg-light);
}

.dashboard .hero-content h1 {
  color: var(--color-secondary);
}

.dash-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.btn-outline {
  padding: 0.6rem 1.2rem;
  border: 2px solid var(--color-secondary);
  color: var(--color-secondary);
  border-radius: 6px;
  font-weight: 500;
  text-decoration: none;
  transition: background var(--transition-speed), color var(--transition-speed);
}

.btn-outline:hover {
  background: var(--color-secondary);
  color: #fff;
}

/* 버튼 공통 */
.btn-primary {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: var(--color-secondary);
  color: #fff;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: background var(--transition-speed), transform 0.1s;
}

.btn-primary:hover {
  background: #3e0fcc;
  transform: translateY(-2px);
}

/* 기능 그리드 */
.features {
  padding: 3rem 1rem;
  text-align: center;
}

.features h2 {
  font-size: 2rem;
  color: var(--color-secondary);
  margin-bottom: 1.5rem;
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
}

.feature-box {
  background: #f9f9ff;
  padding: 1.5rem;
  border-radius: 10px;
  transition: transform 0.2s;
}

.feature-box:hover {
  transform: translateY(-4px);
}

.feature-box img {
  width: 48px;
  margin-bottom: 0.75rem;
}

.feature-box h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

/* 왜 FinTrust */
.benefits {
  padding: 3rem 1rem;
  background: var(--color-bg-light);
}

.benefits h2 {
  font-size: 1.75rem;
  margin-bottom: 1.25rem;
  color: var(--color-text);
  text-align: center;
}

.benefit-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
  gap: 1.25rem;
  list-style: none;
  padding: 0;
}

.benefit-list li {
  background: var(--color-bg);
  padding: 1.25rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}

.benefit-list li:hover {
  transform: translateY(-3px);
}

.benefit-list strong {
  display: block;
  font-size: 1.1rem;
  color: var(--color-secondary);
  margin-bottom: 0.5rem;
}

/* 콜투액션 */
.cta {
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
  background: var(--color-bg);
}

/* 반응형 */
@media (max-width: 768px) {
  .hero {
    padding: 2rem 1rem;
  }
  .hero-content h1 {
    font-size: 2.25rem;
  }
}
</style>
