<!-- src/views/UserProfileView.vue -->
<template>
  <div class="wrapper">
    <div v-if="profile" class="profile-card">
      <!-- 1) 아바타 -->
      <img
        :src="profile.profile_image || defaultAvatar"
        alt="avatar"
        class="avatar"
      />

      <!-- 2) 기본 정보 -->
      <h2 class="username">{{ profile.username }}</h2>
      <p class="field"><strong>이메일:</strong> {{ profile.email }}</p>
      <p class="field">
        <strong>가입일:</strong>
        {{ formattedDate(profile.date_joined) }}
      </p>
      <p class="field"><strong>한 줄 소개:</strong> {{ profile.bio || '-' }}</p>
      <p class="field"><strong>나이:</strong> {{ profile.age || '-' }}</p>
      <p class="field">
        <strong>보유 금액:</strong> {{ profile.current_balance || '-' }}
      </p>
      <p class="field"><strong>연봉:</strong> {{ profile.salary || '-' }}</p>
      <p class="field">
        <strong>회원번호:</strong> {{ profile.membership_number }}
      </p>
      <p class="field"><strong>User ID:</strong> {{ profile.id }}</p>

      <!-- 3) 팔로워/팔로잉 -->
      <div class="stats">
        <span>팔로워 {{ profile.followers_count }}</span>
        <span>팔로잉 {{ profile.following_count }}</span>
      </div>

      <!-- 4) 팔로우 토글 -->
      <div class="actions">
        <button
          v-if="isLogin && !isOwner"
          :class="['btn', isFollowing ? 'btn-unfollow' : 'btn-follow']"
          @click="toggleFollow"
        >
          {{ isFollowing ? '언팔로우' : '팔로우' }}
        </button>
      </div>

      <!-- 5) 작성한 게시글 리스트 -->
      <div v-if="posts.length" class="user-posts">
        <h3>작성한 게시글</h3>
        <ul class="post-list">
          <li
            v-for="post in posts"
            :key="post.id"
            class="post-item"
          >
            <RouterLink
              :to="{ name: 'CommunityDetail', params: { id: post.id } }"
              class="post-link"
            >
              <h3>{{ post.title }}</h3>
              <img
                v-if="post.image"
                :src="post.image"
                alt="cover"
                class="thumb"
              />
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="loading">
      로딩 중…
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import defaultAvatar from '@/assets/default-avatar.png'

const route       = useRoute()
const store       = useUserStore()
const profile     = ref(null)
const posts       = ref([])
const isFollowing = ref(false)

const isLogin = computed(() => store.isLogin)
const isOwner = computed(() => store.username === route.params.username)

// ISO 문자열을 보기 좋은 날짜로
function formattedDate(iso) {
  return new Date(iso).toLocaleString()
}

async function loadProfile() {
  // 1) 프로필 + 팔로우 여부
  const { data: userData } = await api.get(
    `/accounts/users/${route.params.username}/`
  )
  // 2) 게시글
  const { data: postData } = await api.get(
    `/community/users/${route.params.username}/posts/`
  )
  // 3) 팔로워/팔로잉 리스트 얻어서 카운트 계산
  const [{ data: fwList }, { data: fgList }] = await Promise.all([
    api.get(`/accounts/users/${route.params.username}/followers/`),
    api.get(`/accounts/users/${route.params.username}/following/`),
  ])

  profile.value = {
    ...userData,
    followers_count: Array.isArray(fwList) ? fwList.length : 0,
    following_count: Array.isArray(fgList) ? fgList.length : 0,
  }
  isFollowing.value = !!userData.is_following
  posts.value      = postData
}

async function toggleFollow() {
  try {
    await api.post(
      `/accounts/users/${route.params.username}/follow-toggle/`
    )
    // 로컬 상태 즉시 업데이트
    isFollowing.value = !isFollowing.value
    profile.value.followers_count += isFollowing.value ? 1 : -1
  } catch (err) {
    console.error('팔로우 토글 실패', err)
  }
}

onMounted(loadProfile)
</script>

<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  padding: 2rem;
  background: #f0f2f5;
}
.profile-card {
  width: 600px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  padding: 2rem;
  text-align: center;
}
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #004080;
  object-fit: cover;
  margin-bottom: 1rem;
  transition: transform 0.2s;
}
.avatar:hover {
  transform: scale(1.05);
}
.username {
  font-size: 2rem;
  color: #004080;
  margin-bottom: 1rem;
}
.field {
  margin: 0.4rem 0;
  color: #555;
  text-align: left;
}
.stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 1.5rem 0;
}
.stats span {
  background: #f5f7fa;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-weight: 500;
  color: #333;
}
.actions {
  margin-bottom: 2rem;
}
.btn {
  padding: 0.6rem 1.4rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-follow {
  background: #004080;
  color: #fff;
}
.btn-follow:hover {
  background: #002952;
}
.btn-unfollow {
  background: #dc2626;
  color: #fff;
}
.btn-unfollow:hover {
  background: #b91c1c;
}
.user-posts {
  margin-top: 2rem;
  text-align: left;
}
.user-posts h3 {
  margin-bottom: 1rem;
  color: #004080;
  font-size: 1.4rem;
  border-bottom: 2px solid #004080;
  padding-bottom: 0.5rem;
}
.post-list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 1rem;
}
.post-item {
  background: #fafafa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  transition: box-shadow 0.1s, transform 0.1s;
}
.post-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}
.post-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}
.post-link h3 {
  margin: 0;
  flex: 1;
  font-size: 1.1rem;
  color: #004080;
}
.thumb {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-left: 1rem;
}
.loading {
  color: #666;
  font-size: 1.1rem;
}
</style>
