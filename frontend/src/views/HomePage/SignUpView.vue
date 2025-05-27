<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="onSignUp">
      <input v-model="username" placeholder="아이디" />
      <input v-model="email" placeholder="이메일" />
      <input v-model="password1" type="password" placeholder="비밀번호" />
      <input v-model="password2" type="password" placeholder="비밀번호 확인" />
      <button type="submit">가입</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')

const onSignUp = async () => {
  try {
    await userStore.signUp({ username: username.value, email: email.value, password1: password1.value, password2: password2.value })
    const confirmed = window.confirm('회원가입이 성공했습니다. 로그인 하시겠습니까?')
    if (confirmed) {
      router.push({ name: 'LogInView' })
    }
  } catch (err) {
    console.error('회원가입 중 오류:', err)
  }
}
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.signup-container h2 {
  text-align: center;
  color: #004080;
  margin-bottom: 1rem;
}
.signup-container input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.signup-container button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background-color: #0073e6;
  color: #ffffff;
  font-size: 1rem;
  cursor: pointer;
}
.signup-container button:hover {
  background-color: #005bb5;
}
</style>