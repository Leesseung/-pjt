<!-- src/views/ProfileView.vue -->
<template>
  <div class="profile-page">
    <aside class="sidebar">
      <nav>
        <ul>
          <li :class="{ active: activeTab === 'info' }">
            <router-link to="#" @click.prevent="activeTab = 'info'">내 프로필</router-link>
          </li>
          <li>
            <button class="edit-toggle" @click="editing = !editing">
              {{ editing ? '수정 취소' : '회원 정보 수정' }}
            </button>
          </li>
        </ul>
      </nav>
    </aside>

    <main class="content">
      <!-- 정보보기 모드 -->
      <template v-if="!editing">
        <!-- 통계 박스 -->
        <section class="profile-stats">
          <div class="stat-box" @click="activeTab = 'followers'">
            <h3>팔로워</h3>
            <p>{{ user.followers_count }}</p>
          </div>
          <div class="stat-box" @click="activeTab = 'following'">
            <h3>팔로잉</h3>
            <p>{{ user.following_count }}</p>
          </div>
          <div class="stat-box">
            <h3>가입일</h3>
            <p>{{ new Date(user.date_joined).toLocaleDateString() }}</p>
          </div>
        </section>

        <!-- 프로필 상세 -->
        <section v-if="activeTab === 'info'">
          <div class="profile-header">
            <div class="avatar-wrapper">
              <img :src="user.profile_image || defaultImage" alt="avatar" />
            </div>
            <div class="user-info">
              <h2>{{ user.username }}</h2>
              <p>{{ user.email }}</p>
            </div>
          </div>

          <section class="profile-details">
            <dl>
              <dt>한 줄 소개</dt><dd>{{ user.bio || '-' }}</dd>
              <dt>나이</dt><dd>{{ user.age || '-' }}세</dd>
              <dt>연봉</dt><dd>{{ user.salary ? user.salary.toLocaleString() + '원' : '-' }}</dd>
              <dt>회원번호</dt><dd>{{ user.id }}</dd>
            </dl>
          </section>
        </section>

        <!-- 팔로워 리스트 -->
        <section v-if="activeTab === 'followers'">
          <FollowerList />
        </section>

        <!-- 팔로잉 리스트 -->
        <section v-if="activeTab === 'following'">
          <FollowingList />
        </section>
      </template>

      <!-- 편집 모드 -->
      <div v-else>
        <ProfileEditForm @saved="onSaved" @error="onError" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import defaultImage from '@/assets/default-avatar.png'
import ProfileEditForm from '@/components/ProfileEditForm.vue'
import FollowerList from '@/components/FollowerList.vue'
import FollowingList from '@/components/FollowingList.vue'

const user = ref({})
const store = useUserStore()
const editing = ref(false)
const activeTab = ref('info')

onMounted(async () => {
  try {
    const { data } = await api.get('/accounts/profile/')
    user.value = data
  } catch (e) {
    console.error(e)
  }
})

function onSaved() {
  editing.value = false
  api.get('/accounts/profile/').then(r => (user.value = r.data))
}

function onError(err) {
  console.error('프로필 수정 에러', err)
  alert('프로필 수정 중 오류가 발생했습니다.')
}
</script>

<style scoped>
/* 네이버 그린 테마 */
:root {
  --naver-green: #2DB400;
  --bg-light: #F9F9F9;
  --text-dark: #222;
  --sidebar-bg: #ffffff;
  --radius: 8px;
  --spacing: 1rem;
  --font-base: 'Noto Sans KR', sans-serif;
}

.profile-page {
  display: flex;
  min-height: 100vh;
  font-family: var(--font-base);
  background: var(--bg-light);
}

.sidebar {
  width: 200px;
  background: var(--sidebar-bg);
  border-right: 1px solid #ebebeb;
  padding: var(--spacing);
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: var(--spacing);
}

.sidebar a {
  color: #555;
  text-decoration: none;
  font-weight: 500;
  display: block;
  padding: 0.5rem;
  border-radius: var(--radius);
  transition: background 0.2s;
}

.sidebar li.active a,
.sidebar a:hover {
  background: var(--naver-green);
  color: #fff;
}

.edit-toggle {
  background: none;
  border: none;
  color: var(--naver-green);
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem;
}
.edit-toggle:hover {
  text-decoration: underline;
}

.content {
  flex: 1;
  padding: 2rem;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar-wrapper {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 1rem;
}

.avatar-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info h2 {
  font-size: 1.5rem;
  margin: 0 0 0.25rem;
  color: var(--text-dark);
}

.user-info p {
  margin: 0;
  color: #666;
}

.profile-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: #fff;
  border-radius: var(--radius);
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  flex: 1;
  text-align: center;
  padding: 1rem;
  cursor: pointer;
}

.stat-box h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  color: var(--naver-green);
}

.stat-box p {
  margin: 0;
  font-size: 1.25rem;
  font-weight: bold;
}

.profile-details dl {
  display: grid;
  grid-template-columns: 100px 1fr;
  row-gap: 0.75rem;
  column-gap: 1rem;
  margin-bottom: 2rem;
}

.profile-details dt {
  font-weight: 500;
  color: #555;
}

.profile-details dd {
  margin: 0;
  color: var(--text-dark);
}

@media (max-width: 768px) {
  .profile-page {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #ebebeb;
    display: flex;
    justify-content: center;
  }
  .sidebar ul {
    display: flex;
    gap: 1rem;
  }
  .content {
    padding: 1rem;
  }
  .profile-stats {
    flex-direction: column;
  }
}
</style>
