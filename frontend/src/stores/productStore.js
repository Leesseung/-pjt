import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './userStore'

export const useProductStore = defineStore('product', () => {
  const products = ref([])
  const detail   = ref(null)
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/products'

  // 전체 상품 목록 조회
  async function fetchProducts() {
    const res = await axios.get(`${BASE_URL}/`)
    products.value = res.data
  }

  // 단일 상품 상세 조회
  async function fetchProduct(id) {
    const res = await axios.get(`${BASE_URL}/${id}/`)
    detail.value = res.data
  }

  // 가입하기: userStore.subscribe에 위임
  async function subscribe(id) {
    const userStore = useUserStore()
    if (!userStore.isLogin) {
      alert('로그인 후 이용해주세요.')
      return
    }
    try {
      // userStore.subscribe가 API 호출 및 localStorage 갱신을 담당합니다
      await userStore.subscribe(id)
      alert('가입이 완료되었습니다.')
    } catch (err) {
      console.error(err)
      alert(err.response?.data?.detail || '가입 중 오류가 발생했습니다.')
    }
  }

  return {
    products,
    detail,
    fetchProducts,
    fetchProduct,
    subscribe
  }
})
