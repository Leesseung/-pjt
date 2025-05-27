<template>
  <div class="edit-container">
    <h3 class="edit-title">글 수정</h3>
    <form @submit.prevent="submit" class="edit-form">
      <input
        v-model="title"
        required
        placeholder="제목"
        class="edit-input"
      />
      <textarea
        v-model="content"
        required
        placeholder="내용"
        class="edit-textarea"
      ></textarea>
      <input
        type="file"
        @change="onFileChange"
        class="edit-file"
      />
      <button type="submit" class="edit-btn">저장</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/lib/axios'

const route   = useRoute()
const router  = useRouter()
const title   = ref('')
const content = ref('')
const file    = ref(null)

onMounted(async () => {
  const { data } = await api.get(`/community/posts/${route.params.id}/`)
  title.value   = data.title
  content.value = data.content
})

function onFileChange(e) {
  file.value = e.target.files[0]
}

async function submit() {
  const form = new FormData()
  form.append('title', title.value)
  form.append('content', content.value)
  if (file.value) form.append('image', file.value)

  await api.patch(`/community/posts/${route.params.id}/`, form)
  router.push({ name: 'CommunityDetail', params: { id: route.params.id } })
}
</script>

<style scoped>
.edit-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.edit-title {
  font-size: 1.5rem;
  color: #004080;
  margin-bottom: 1rem;
  text-align: center;
}
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.edit-input,
.edit-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  color: #333;
}
.edit-input:focus,
.edit-textarea:focus {
  outline: none;
  border-color: #004080;
  box-shadow: 0 0 0 2px rgba(0, 64, 128, 0.2);
}
.edit-textarea {
  min-height: 150px;
  resize: vertical;
}
.edit-file {
  font-size: 0.9rem;
}
.edit-btn {
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
.edit-btn:hover {
  background-color: #003060;
}
</style>
