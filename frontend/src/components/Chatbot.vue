<!-- src/components/Chatbot.vue -->
<template>
  <!-- 1) 로그인 상태일 때만 뜨는 채팅 아이콘 -->
  <div v-if="isLogin" class="chat-icon" @click="open = !open">
    <img src="@/assets/chat-icon.png" alt="Chatbot" />
  </div>

  <!-- 2) 채팅창 -->
  <div v-if="open" class="chatbot">
    <div class="header">
      <h4>금융 추천 챗봇</h4>
      <button class="close-btn" @click="open = false">&times;</button>
    </div>

    <div class="messages">
      <div
        v-for="(m, i) in messages"
        :key="i"
        :class="['message', m.from]"
      >
        <pre v-if="m.from === 'bot'">{{ m.text }}</pre>
        <p v-else>{{ m.text }}</p>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="금융 상품 추천을 물어보세요…"
      />
      <button @click="send">전송</button>
    </div>
  </div>

  <!-- 3) 풀스크린 모달 (teleport to body) -->
  <teleport to="body">
    <ProductDetailModal
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="selectedProduct = null"
    />
  </teleport>

  <LoadingOverlay :visible="loading" />
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import ProductDetailModal from '@/components/ProductDetailModal/ProductDetailModal.vue'

const store = useUserStore()
const isLogin = computed(() => store.isLogin)
const loading = ref(false)

const open = ref(false)
const messages = ref([])
const input = ref('')
const selectedProduct = ref(null)

async function send() {
  const txt = input.value.trim()
  if (!txt) return

  messages.value.push({ from: 'user', text: txt })
  input.value = ''
  loading.value = true

  try {
    const { data } = await api.post('/chat/recommend/', { message: txt })

    // 챗봇 답변 메시지 추가 (bot 응답 텍스트가 있다면)
    if (data.text) {
      messages.value.push({ from: 'bot', text: data.text })
    }

    // 상품 객체가 있으면 모달로 띄우기
    if (data.product && data.product.fin_prdt_cd) {
      const prod = data.product
      // 추천 API에서 옵션 리스트를 내려주면 data.options에, 아니면 prod.options 사용
      const options = data.options || prod.options || []

      // fin_prdt_cd 첫 글자 숫자 → 예금, 문자(WR 등) → 적금
      const type = /^[0-9]/.test(prod.fin_prdt_cd) ? 'deposit' : 'saving'

      selectedProduct.value = {
        ...prod,
        type,
        options
      }
    }
  } catch (e) {
    console.error(e)
    messages.value.push({
      from: 'bot',
      text: '추천 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 채팅 아이콘 */
.chat-icon {
  position: fixed;
  right: 1.5rem;
  bottom: 1.5rem;
  width: 56px;
  height: 56px;
  cursor: pointer;
  z-index: 1001;
}
.chat-icon img {
  width: 100%;
  height: 100%;
}

/* 채팅창 */
.chatbot {
  position: fixed;
  right: 1.5rem;
  bottom: 1.5rem;
  width: 360px;
  max-height: 480px;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  overflow: hidden;
  font-family: 'Noto Sans KR', sans-serif;
  z-index: 1000;
}
.chatbot .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #5c16ff;
  color: #fff;
}
.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.2rem;
  cursor: pointer;
}
.messages {
  flex: 1;
  padding: 0.75rem 1rem;
  overflow-y: auto;
  background: #fafafa;
}
.message { margin-bottom: .75rem; }
.message.user { text-align: right; color: #004080; }
.message.bot  { text-align: left;  color: #333; }
.input-area {
  display: flex;
  border-top: 1px solid #ddd;
}
.input-area input {
  flex: 1;
  padding: .75rem;
  border: none;
  outline: none;
}
.input-area button {
  padding: 0 1.2rem;
  border: none;
  background: #5c16ff;
  color: #fff;
  cursor: pointer;
  transition: background .2s;
}
.input-area button:hover {
  background: #3e0fcc;
}
</style>
