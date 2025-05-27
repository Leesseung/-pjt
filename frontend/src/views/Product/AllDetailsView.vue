<template>
  <div class="all-details">
    <h1>금융상품 전체 보기</h1>
    <hr />

    <div v-if="loading" class="no-items">
      데이터 로딩 중...
    </div>

    <div v-else>
      <div v-if="products.length === 0" class="no-items">
        불러올 상품이 없습니다.
      </div>

      <div v-else class="detail-list">
        <div
          v-for="prod in products"
          :key="prod.id"
          class="detail-card"
        >
          <!-- 상품 타입 -->
          <h2 class="product-type">
            {{ prod.name.includes('예금') ? '정기예금' : '정기적금' }}
          </h2>

          <div class="detail-item">
            <strong>공시 제출월:</strong> {{ prod.dcls_month }}
          </div>
          <div class="detail-item">
            <strong>금융회사명:</strong> {{ prod.bank_name }}
          </div>
          <div class="detail-item">
            <strong>상품명:</strong> {{ prod.name }}
          </div>
          <div class="detail-item">
            <strong>가입 제한:</strong> {{ prod.join_deny === 'Y' ? '제한' : '가능' }}
          </div>
          <div class="detail-item">
            <strong>기간:</strong> {{ prod.save_trm }}개월
          </div>
          <div class="detail-item">
            <strong>기준 이율:</strong> {{ prod.intr_rate }}%
          </div>
          <div class="detail-item">
            <strong>우대 이율:</strong> {{ prod.supr_rate }}%
          </div>
          <div class="detail-item">
            <strong>우대 조건:</strong>
            <ul>
              <li v-for="(c, i) in splitSpcl(prod.spcl_cnd)" :key="i">
                {{ c }}
              </li>
            </ul>
          </div>
          <div class="detail-item">
            <strong>기타 안내:</strong> {{ prod.etc_note }}
          </div>

          <RouterLink
            :to="{ name: 'ProductsDetail', params: { id: prod.id } }"
            class="btn btn-primary btn-sm"
          >
            상세 보기
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProductStore } from '@/stores/productStore'

const productStore = useProductStore()
const products     = ref([])
const loading      = ref(true)

onMounted(async () => {
  // 전체 상품 불러오기
  await productStore.fetchProducts()
  products.value = productStore.products
  loading.value  = false
})

// 우대조건 문자열(';')을 배열로
function splitSpcl(raw = '') {
  return raw.split(';').filter(Boolean)
}
</script>

<style scoped>
.all-details {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
h1 {
  color: #004080;
  margin-bottom: 0.5rem;
}
hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin-bottom: 1.5rem;
}
.no-items {
  text-align: center;
  color: #666;
  padding: 2rem 0;
}
.detail-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-height: 70vh;
  overflow-y: auto;
}
.detail-card {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background: #f7f9fc;
}
.product-type {
  font-size: 1.25rem;
  font-weight: bold;
  color: #004080;
  margin-bottom: 0.75rem;
}
.detail-item {
  margin-bottom: 0.5rem;
  line-height: 1.4;
}
.detail-item strong {
  display: inline-block;
  width: 100px;
}
.btn-primary {
  background-color: #0073e6;
  border-color: #0073e6;
}
.btn-primary:hover {
  background-color: #005bb5;
  border-color: #005bb5;
}
</style>
