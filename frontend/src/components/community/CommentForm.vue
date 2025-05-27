<template>
  <form @submit.prevent="submit" class="comment-form">
    <textarea
      v-model="content"
      placeholder="댓글을 입력하세요"
      required
      class="comment-textarea"
    />
    <button type="submit" class="comment-btn">
      {{ parentId ? '답글 등록' : '댓글 등록' }}
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/lib/axios'

const props = defineProps({
  postId:   { type: Number, required: true },
  parentId: { type: Number, default: null }
})
const emit = defineEmits(['refresh'])
const content = ref('')

async function submit() {
  const payload = { content: content.value }
  if (props.parentId !== null) payload.parent = props.parentId
  await api.post(
    `/community/posts/${props.postId}/comments/`,
    payload
  )
  content.value = ''
  emit('refresh')
}
</script>

<style scoped>
.comment-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.comment-textarea {
  width: 100%;
  min-height: 80px;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.95rem;
  resize: vertical;
}

.comment-textarea:focus {
  outline: none;
  border-color: #004080;
  box-shadow: 0 0 0 2px rgba(0, 64, 128, 0.2);
}

.comment-btn {
  align-self: flex-end;
  padding: 0.5rem 1rem;
  background-color: #004080;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
}

.comment-btn:hover {
  background-color: #003060;
}
</style>