<template>
  <div class="comments">
    <h4>댓글</h4>
    <ul>
      <li v-for="c in comments" :key="c.id">
        <strong>{{ c.author.username }}:</strong> {{ c.content }}
      </li>
    </ul>
    <form v-if="user.isLogin" @submit.prevent="addComment">
      <input v-model="newComment" placeholder="댓글을 입력하세요" required />
      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'
import { useRoute } from 'vue-router'

const user = useUserStore()
const route = useRoute()

const comments = ref([])
const newComment = ref('')

async function loadComments() {
  const res = await axios.get(`/api/v1/community/posts/${route.params.id}/comments/`)
  comments.value = res.data
}

async function addComment() {
  try {
    await axios.post(
      `/api/v1/community/posts/${route.params.id}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Token ${user.token}` } }
    )
    newComment.value = ''
    loadComments()
  } catch (e) {
    console.error(e)
    alert('댓글 작성에 실패했습니다.')
  }
}

onMounted(loadComments)
</script>

<style scoped>
.comments ul { list-style: none; padding: 0; }
.comments li { padding: 0.5rem 0; border-bottom: 1px solid #eee; }
.comments form { margin-top: 1rem; }
.comments input { width: 80%; padding: 0.5rem; }
.comments button { padding: 0.5rem 1rem; }
</style>
