<!-- src/components/LoadingOverlay.vue -->
<template>
  <teleport to="body">
    <div v-if="visible" class="overlay">
      <div class="spinner"></div>
      <div class="loading-text">로딩 중...</div>
    </div>
  </teleport>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  visible: {
    type: Boolean,
    required: true
  }
});
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.spinner {
  position: relative;
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
}

/* 바깥 링 */
.spinner::before,
.spinner::after {
  content: "";
  box-sizing: border-box;
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 6px solid transparent;
}

.spinner::before {
  border-top-color: #5c16ff;
  animation: spin 1s linear infinite;
}

.spinner::after {
  border-bottom-color: #ff4081;
  animation: spin 1.5s linear infinite reverse;
}

.loading-text {
  color: #fff;
  font-size: 1.1rem;
  letter-spacing: 0.05em;
  animation: fade 1.5s ease-in-out infinite;
  text-shadow: 0 0 8px rgba(0,0,0,0.5);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>
