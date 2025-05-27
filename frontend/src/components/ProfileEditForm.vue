<!-- src/components/ProfileEditForm.vue -->
<template>
  <div class="profile-edit">
    <h3>내 정보 수정</h3>
    <form @submit.prevent="submit">
      <div class="form-group">
        <label>프로필 이미지</label>
        <input type="file" @change="onFileChange" />
      </div>
      <div class="form-group">
        <label>한 줄 소개</label>
        <input v-model="form.bio" />
      </div>
      <div class="form-group">
        <label>나이</label>
        <input type="number" v-model="form.age" />
      </div>
      <div class="form-group">
        <label>현재 금액</label>
        <input type="number" v-model="form.current_balance" step="0.01" />
      </div>
      <div class="form-group">
        <label>연봉</label>
        <input type="number" v-model="form.salary" step="0.01" />
      </div>
      <div class="form-group readonly">
        <label>회원번호</label>
        <input :value="form.membership_number" readonly />
      </div>
      <div class="form-group readonly">
        <label>User ID</label>
        <input :value="form.id" readonly />
      </div>
      <button type="submit">저장</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import api from '@/lib/axios'

const emit = defineEmits(['saved', 'error'])

const form = ref({
  profile_image: null,
  bio: '',
  age: null,
  current_balance: null,
  salary: null,
  membership_number: '',
  id: null,
})

let file = null

onMounted(async () => {
  try {
    const { data } = await api.get('/accounts/profile/')
    form.value = { ...form.value, ...data }
  } catch (e) {
    emit('error', e)
  }
})

function onFileChange(e) {
  file = e.target.files[0]
}

async function submit() {
  const fd = new FormData()
  if (file) fd.append('profile_image', file)
  fd.append('bio', form.value.bio)
  fd.append('age', form.value.age)
  fd.append('current_balance', form.value.current_balance)
  fd.append('salary', form.value.salary)

  try {
    await api.patch('/accounts/profile/', fd)
    emit('saved')
  } catch (e) {
    emit('error', e)
  }
}
</script>

<style scoped>
.profile-edit {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1rem;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
}
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-group.readonly input {
  background: #f5f5f5;
  cursor: not-allowed;
}
button {
  padding: 0.5rem 1.2rem;
  background: #004080;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background: #003060;
}
</style>
