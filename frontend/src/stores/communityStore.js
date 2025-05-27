import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './userStore'

export const useCommunityStore = defineStore('community', () => {
  const posts    = ref([])
  const post     = ref(null)
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/posts'
  const userStore = useUserStore()

  async function fetchPosts() {
    const res = await axios.get(BASE_URL)
    posts.value = res.data
  }
  async function fetchPost(id) {
    const res = await axios.get(`${BASE_URL}/${id}/`)
    post.value = res.data
  }
  async function createPost(data) {
    const res = await axios.post(BASE_URL + '/', data, { headers: { Authorization: `Token ${userStore.token}` } })
    return res.data
  }
  async function updatePost(id, data) {
    await axios.put(`${BASE_URL}/${id}/`, data, { headers: { Authorization: `Token ${userStore.token}` } })
  }
  async function deletePost(id) {
    await axios.delete(`${BASE_URL}/${id}/`, { headers: { Authorization: `Token ${userStore.token}` } })
  }

  return { posts, post, fetchPosts, fetchPost, createPost, updatePost, deletePost }
})