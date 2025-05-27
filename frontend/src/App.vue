<template>
  <nav class="navbar">
    <div class="container d-flex align-items-center justify-content-between">
      <!-- Brand + Greeting -->
      <div class="brand-section d-flex align-items-center">
        <RouterLink to="/" class="navbar-brand logo">
          <span class="logo-primary">Fin</span><span class="logo-secondary">Trust</span>
        </RouterLink>
        <span v-if="userStore.isLogin" class="greeting">
          {{ userStore.username }}님, 안녕하세요
        </span>
      </div>

      <!-- Navigation -->
      <ul class="nav nav-pills">
        <li class="nav-item">
          <RouterLink
            to="/bank-search"
            class="nav-link"
            :class="{ active: $route.name === 'ProductsList' }"
            v-if="userStore.isLogin"
          >근처 은행 검색</RouterLink>
        </li>
        <li class="nav-item dropdown" v-if="userStore.isLogin">
          <a
            class="nav-link dropdown-toggle"
            data-bs-toggle="dropdown"
            role="button"
            aria-expanded="false"
          >비디오</a>
          <ul class="dropdown-menu">
            <li><RouterLink to="/search" class="dropdown-item">검색</RouterLink></li>
            <li><RouterLink to="/later" class="dropdown-item">나중에 볼 영상</RouterLink></li>
            <li><RouterLink to="/channels" class="dropdown-item">저장된 채널</RouterLink></li>
          </ul>
        </li>
        <li class="nav-item dropdown" v-if="userStore.isLogin">
          <a
            class="nav-link dropdown-toggle"
            data-bs-toggle="dropdown"
            role="button"
            aria-expanded="false"
          >커뮤니티</a>
          <ul class="dropdown-menu">
            <li><RouterLink to="/community/create" class="dropdown-item">게시글 작성</RouterLink></li>
            <li><RouterLink to="/community" class="dropdown-item">게시글 목록</RouterLink></li>
            <li><RouterLink to="/community/mine" class="dropdown-item">내 게시글</RouterLink></li>
          </ul>
        </li>
        <li class="nav-item dropdown" v-if="userStore.isLogin">
          <a
            class="nav-link dropdown-toggle"
            data-bs-toggle="dropdown"
            role="button"
            aria-expanded="false"
          >예·적금</a>
          <ul class="dropdown-menu">
            <li><RouterLink to="/products" class="dropdown-item">금리비교</RouterLink></li>
            <li><RouterLink to="/my-products" class="dropdown-item">내가 가입한 상품</RouterLink></li>
            <li><RouterLink to="/charts" class="dropdown-item">시세 차트</RouterLink></li>
          </ul>
        </li>
      </ul>

      <!-- Auth Buttons -->
      <div class="auth-buttons d-flex align-items-center">
        <Chatbot />
        <RouterLink
          v-if="userStore.isLogin"
          to="/profile"
          class="btn btn-outline-secondary me-2"
        >내 프로필</RouterLink>
        <button
          v-if="userStore.isLogin"
          class="btn btn-outline-primary"
          @click="handleLogout"
        >로그아웃</button>
        <template v-else>
          <RouterLink to="/signup" class="btn btn-outline-primary me-2">회원가입</RouterLink>
          <RouterLink to="/login" class="btn btn-primary">로그인</RouterLink>
        </template>
      </div>
    </div>
  </nav>
  <RouterView />
</template>

<script setup>
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import Chatbot from '@/components/Chatbot.vue'

const userStore = useUserStore()
const router = useRouter()

function handleLogout() {
  userStore.logOut()
  router.push('/')
}
</script>

<style scoped>
/* 테마 변수 */
:root {
  --color-primary: #01c878;
  --color-primary-dark: #019e65;
  --color-bg: #ffffff;
  --color-text: #212529;
  --color-border: #e9ecef;
  --transition-speed: 0.3s;
}

.navbar {
  background-color: var(--color-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0.75rem 1.5rem;
  font-family: 'Inter', sans-serif;
}

/* 브랜드 로고 */
.brand-section .logo {
  font-size: 1.75rem;
  font-weight: 700;
  transition: transform var(--transition-speed);
}
.brand-section .logo:hover {
  transform: scale(1.05);
}
.logo-primary { color: var(--color-primary-dark); }
.logo-secondary { color: var(--color-primary); }
.greeting {
  margin-left: 1rem;
  color: var(--color-text);
  font-weight: 500;
  opacity: 0.8;
}

/* 네비게이션 */
.nav-pills .nav-link {
  color: var(--color-primary-dark);
  font-weight: 500;
  transition: background-color var(--transition-speed),
              color var(--transition-speed);
}
.nav-pills .nav-link:hover {
  background-color: rgba(1, 200, 120, 0.1);
}
.nav-pills .nav-link.active {
  background-color: var(--color-primary);
  color: #fff;
}
.dropdown-menu {
  min-width: 12rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.2s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 인증 버튼 */
.auth-buttons .btn {
  font-size: 0.9rem;
  border-radius: 6px;
  transition: background-color var(--transition-speed),
              transform var(--transition-speed);
}
.btn-primary {
  background-color: var(--color-primary);
  border-color: var(--color-primary-dark);
  color: #fff;
}
.btn-primary:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
}
.btn-outline-primary {
  color: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
}
.btn-outline-primary:hover {
  background-color: var(--color-primary);
  color: #fff;
}
.btn-outline-secondary {
  color: var(--color-text);
  border-color: var(--color-border);
}
.btn-outline-secondary:hover {
  background-color: var(--color-border);
}
</style>