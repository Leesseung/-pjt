<!-- FollowerList.vue -->
<template>
  <div class="list-container">
    <h3>팔로워 목록</h3>
    <ul>
      <li v-for="u in followers" :key="u.id">
        <RouterLink :to="{ name: 'UserProfile', params: { username: u.username } }">
          <img :src="u.profile_image || defaultAvatar" class="avatar" />
          <span>{{ u.username }}</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import defaultAvatar from '@/assets/default-avatar.png'

const followers = ref([])
const store = useUserStore()

onMounted(async () => {
  // 로그인한 자신의 팔로워 조회
  const username = store.username
  const res = await api.get(`/accounts/users/${username}/followers/`)
  followers.value = res.data
})
</script>


<style scoped>
.list-container { padding: 1rem; }
.list-container h3 { margin-bottom: .5rem; color: #004080; }
.list-container ul { list-style: none; padding: 0; }
.list-container li {
  display: flex;
  align-items: center;
  margin-bottom: .75rem;
}
.avatar {
  width:32px; height:32px; border-radius:50%; object-fit:cover;
  margin-right:.5rem;
}
</style>
