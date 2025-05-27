<template>
  <div class="create-container">
    <h3 class="create-title">새 글 작성</h3>
    <form @submit.prevent="submit" class="create-form">
      <input
        v-model="title"
        placeholder="제목"
        required
        class="create-input"
      />
      <textarea
        v-model="content"
        placeholder="내용"
        required
        class="create-textarea"
      ></textarea>
      <input
        type="file"
        @change="onFileChange"
        class="create-file"
      />
      <button type="submit" class="create-btn">등록</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/lib/axios'

const title   = ref('')
const content = ref('')
const file    = ref(null)
const router  = useRouter()

function onFileChange(e) {
  file.value = e.target.files[0]
}

async function submit() {
  const form = new FormData()
  form.append('title', title.value)
  form.append('content', content.value)
  if (file.value) form.append('image', file.value)

  await api.post('/community/posts/', form)
  router.push({ name: 'CommunityList' })
}
</script>

<style scoped>
.create-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.create-title {
  font-size: 1.5rem;
  color: #004080;
  margin-bottom: 1rem;
  text-align: center;
}
.create-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.create-input,
.create-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  color: #333;
}
.create-input:focus,
.create-textarea:focus {
  outline: none;
  border-color: #004080;
  box-shadow: 0 0 0 2px rgba(0, 64, 128, 0.2);
}
.create-textarea {
  min-height: 150px;
  resize: vertical;
}
.create-file {
  font-size: 0.9rem;
}
.create-btn {
  align-self: flex-end;
  padding: 0.5rem 1.5rem;
  background-color: #004080;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.create-btn:hover {
  background-color: #003060;
}
</style>