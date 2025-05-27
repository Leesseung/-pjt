<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="onLogIn">
      <input v-model="username" placeholder="아이디" />
      <input v-model="password" type="password" placeholder="비밀번호" />
      <button type="submit" class="btn-login">로그인</button>
    </form>
    <!-- 회원가입으로 이동하는 링크 -->
    <div class="signup-redirect">
      아직 계정이 없으신가요?
      <RouterLink to="/signup" class="btn-signup">회원가입</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const password = ref('')

const onLogIn = async () => {
  try {
    await userStore.logIn({ username: username.value, password: password.value })
    router.push({ name: 'HomeView' })
  } catch (err) {
    console.error('로그인 중 오류:', err)
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem 1.5rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.login-container h2 {
  text-align: center;
  color: #004080;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}
.login-container input {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}
.btn-login {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background-color: #0073e6;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-login:hover {
  background-color: #005bb5;
}

.signup-redirect {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #666;
}
.btn-signup {
  display: inline-block;
  margin-left: 0.5rem;
  padding: 0.4rem 1rem;
  background-color: #5c16ff;
  color: #fff;
  border-radius: 4px;
  font-size: 0.9rem;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-signup:hover {
  background-color: #3e0fcc;
}
</style>
