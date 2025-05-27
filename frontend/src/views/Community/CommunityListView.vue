<template>
  <div class="community-list">
    <div class="header">
      <h2>게시판</h2>
      <RouterLink to="/community/create" class="write-btn">새 글 쓰기</RouterLink>
    </div>

    <div class="card-grid">
      <div v-for="post in posts" :key="post.id" class="card">
        <RouterLink :to="`/community/${post.id}`" class="card-link">
          <img
            :src="post.image || defaultImage"
            alt="Post image"
            class="card-img"
          />
          <div class="card-body">
            <h3 class="card-title">{{ post.title }}</h3>
            <p class="card-meta">
              <span>{{ post.author_username }}</span>
              <span>{{ new Date(post.created_at).toLocaleDateString() }}</span>
              <span>댓글 {{ post.comment_count }}</span>
            </p>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/lib/axios'
// 기본 이미지: src/assets/default-post.png 파일을 추가하세요
import defaultImage from '@/assets/default-post.png'

const posts = ref([])

onMounted(async () => {
  const { data } = await api.get('/community/posts/')
  posts.value = data
})
</script>

<style scoped>
.community-list {
  padding: 1rem;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.write-btn {
  padding: 0.5rem 1rem;
  background-color: #004080;
  color: #fff;
  border-radius: 0.25rem;
  text-decoration: none;
  font-weight: 500;
}
.write-btn:hover {
  background-color: #003060;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}
.card {
  background: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s;
}
.card:hover {
  transform: translateY(-5px);
}
.card-link {
  color: inherit;
  text-decoration: none;
  display: block;
}
.card-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
.card-body {
  padding: 1rem;
}
.card-title {
  font-size: 1.25rem;
  margin: 0 0 0.5rem;
  color: #004080;
}
.card-meta {
  font-size: 0.875rem;
  color: #666;
  display: flex;
  justify-content: space-between;
}
</style>
