<template>
  <div class="detail-container" v-if="post.id">
    <div class="detail-header">
      <RouterLink to="/community" class="back-link">← 목록으로</RouterLink>
      <div v-if="post.author === Number(userStore.userId)" class="actions">
        <RouterLink
          :to="{ name: 'CommunityEdit', params: { id: post.id } }"
          class="btn btn-edit"
        >수정</RouterLink>
        <button @click="remove" class="btn btn-delete">삭제</button>
      </div>
    </div>

    <div class="post-card">
      <!-- 작성자 정보 -->
      <div class="author-info">
        <RouterLink
          :to="{ name: 'UserProfile', params: { username: post.author_username } }"
          class="author-link"
        >
          <img
            :src="post.author_profile_image || defaultAvatar"
            class="author-avatar"
            alt="작성자 프로필"
          />
          <span class="author-name">{{ post.author_username }}</span>
        </RouterLink>
        <span class="post-date">{{ new Date(post.created_at).toLocaleString() }}</span>
      </div>

      <h2 class="post-title">{{ post.title }}</h2>

      <img
        v-if="post.image"
        :src="post.image"
        alt="Post image"
        class="post-image"
      />

      <div class="post-content" v-html="post.content"></div>
    </div>

    <CommentSection :postId="post.id" />
  </div>

  <div v-else class="loading">
    <p>로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import CommentSection from '@/components/Community/CommentSection.vue'
import defaultAvatar from '@/assets/default-avatar.png'

const route     = useRoute()
const router    = useRouter()
const userStore = useUserStore()
const post      = ref({})

onMounted(async () => {
  try {
    const { data } = await api.get(`/community/posts/${route.params.id}/`)
    post.value = data
  } catch (err) {
    console.error('게시글 로드 실패:', err)
  }
})

async function remove() {
  try {
    await api.delete(`/community/posts/${post.value.id}/`)
    router.push({ name: 'CommunityList' })
  } catch (err) {
    console.error('게시글 삭제 실패:', err)
  }
}
</script>

<style scoped>
.detail-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.back-link {
  color: #004080;
  text-decoration: none;
  font-weight: 500;
}
.back-link:hover {
  text-decoration: underline;
}

.actions .btn {
  margin-left: 0.5rem;
  padding: 0.4rem 0.8rem;
  border: 1px solid #004080;
  border-radius: 4px;
  font-size: 0.9rem;
}
.btn-edit {
  background-color: #ffffff;
  color: #004080;
}
.btn-delete {
  background-color: #e60000;
  color: #ffffff;
  border-color: #e60000;
}
.btn-edit:hover {
  background-color: #f0f8ff;
}
.btn-delete:hover {
  background-color: #cc0000;
}

/* 작성자 정보 */
.author-info {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.author-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
  margin-right: auto;
}
.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 0.5rem;
}
.author-name {
  font-weight: 600;
  color: #004080;
}
.author-name:hover {
  text-decoration: underline;
}
.post-date {
  font-size: 0.85rem;
  color: #666666;
}

/* 게시글 카드 */
.post-card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
}
.post-title {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #004080;
}
.post-image {
  width: 100%;
  height: auto;
  border-radius: 4px;
  margin-bottom: 1rem;
  object-fit: cover;
}
.post-content {
  line-height: 1.6;
  color: #333333;
}

.loading {
  text-align: center;
  color: #666666;
  padding: 2rem;
}
</style>
