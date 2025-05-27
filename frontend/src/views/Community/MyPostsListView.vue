<template>
  <div class="my-posts-page">
    <h2>내가 쓴 게시글</h2>
    <ul class="post-cards">
      <li v-for="post in posts" :key="post.id" class="card">
        <RouterLink
          :to="{ name: 'CommunityDetail', params: { id: post.id } }"
          class="card-link"
        >
          <div class="card-image">
            <img :src="post.image || defaultImage" alt="cover" />
          </div>
          <div class="card-content">
            <h3>{{ post.title }}</h3>
            <p class="meta">
              {{ post.author_username }} ·
              {{ new Date(post.created_at).toLocaleString() }}
            </p>
            <p class="comments">댓글 {{ post.comment_count }}</p>
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/lib/axios'
import defaultImage from '@/assets/default-post.png'

const posts = ref([])

onMounted(async () => {
  try {
    // MyPostListView 로 호출
    const { data } = await api.get('/community/posts/mine/')
    posts.value = data
  } catch (e) {
    console.error('내 게시글 로드 실패:', e)
  }
})
</script>

<style scoped>
.my-posts-page {
  max-width: 960px;
  margin: 2rem auto;
  padding: 0 1rem;
}
.post-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  list-style: none;
  padding: 0;
}
.card {
  width: calc(33.333% - 1rem);
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform .1s;
}
.card:hover {
  transform: translateY(-4px);
}
.card-link {
  color: inherit;
  text-decoration: none;
  display: block;
}
.card-image img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
.card-content {
  padding: 0.75rem;
}
.card-content h3 {
  margin: 0 0 .5rem;
  font-size: 1.1rem;
  color: #004080;
}
.meta {
  font-size: .85rem;
  color: #666;
  margin-bottom: .5rem;
}
.comments {
  font-size: .9rem;
  color: #333;
}
@media (max-width: 768px) {
  .card { width: calc(50% - 1rem); }
}
@media (max-width: 480px) {
  .card { width: 100%; }
}
</style>
