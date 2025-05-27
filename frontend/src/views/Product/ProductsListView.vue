<!-- src/views/ProductsListView.vue -->
<template>
  <div class="products-list">
    <h2>예·적금 상품 비교</h2>

    <!-- 필터 영역 -->
    <div class="filters">
      <label>은행:</label>
      <select v-model="bankFilter">
        <option value="">전체 은행</option>
        <option v-for="bank in banks" :key="bank">{{ bank }}</option>
      </select>

      <label class="ml-4">상품 유형:</label>
      <select v-model="productType">
        <option value="deposit">예금</option>
        <option value="saving">적금</option>
      </select>
    </div>

    <!-- 상품 목록 테이블 -->
    <table class="rates-table">
      <thead>
        <tr>
          <th>은행명</th>
          <th>상품명</th>
          <th v-for="term in availableTerms" :key="term">{{ term }}개월</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="product in filteredProducts"
          :key="product.fin_prdt_cd"
          @click="showProductDetail(product)"
          class="clickable-row"
        >
          <td>{{ product.kor_co_nm }}</td>
          <td class="product-name">{{ product.fin_prdt_nm }}</td>
          <td
            v-for="term in availableTerms"
            :key="term"
            class="rate-cell"
          >
            <div
              v-if="getRateInfo(product, term).hasRate"
              class="rate-info"
            >
              <span class="base-rate">
                {{ getRateInfo(product, term).baseRate }}%
              </span>
              <span class="pref-rate">
                ({{ getRateInfo(product, term).prefRate }}%)
              </span>
            </div>
            <span v-else>-</span>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 상품 상세 모달 -->
    <ProductDetailModal
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="selectedProduct = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import ProductDetailModal from '@/components/ProductDetailModal/ProductDetailModal.vue'

const products = ref([])
const selectedProduct = ref(null)
const bankFilter = ref('')
const productType = ref('deposit')

// 사용 가능한 가입기간을 계산
const availableTerms = computed(() => {
  const terms = new Set()
  products.value.forEach(p =>
    p.options?.forEach(o => terms.add(o.save_trm))
  )
  return Array.from(terms).sort((a, b) => a - b)
})

// 은행 목록
const banks = computed(() =>
  [...new Set(products.value.map(p => p.kor_co_nm))].sort()
)

// 은행 필터링
const filteredProducts = computed(() => {
  let list = products.value
  if (bankFilter.value) {
    list = list.filter(p => p.kor_co_nm === bankFilter.value)
  }
  return list
})

// 특정 기간 금리 정보
function getRateInfo(product, term) {
  const opt = product.options?.find(o => o.save_trm === term)
  if (!opt) return { hasRate: false }
  return {
    hasRate: true,
    baseRate: opt.intr_rate.toFixed(2),
    prefRate: opt.intr_rate2.toFixed(2)
  }
}

// 모달 열기 (type 정보 추가)
function showProductDetail(product) {
  selectedProduct.value = {
    ...product,
    type: productType.value   // 'deposit' 또는 'saving'
  }
}

// 데이터 로드
async function loadProducts() {
  try {
    const endpoint =
      productType.value === 'deposit'
        ? 'deposit-products-with-options'
        : 'saving-products'
    const { data } = await axios.get(
      `http://127.0.0.1:8000/api/v1/products/${endpoint}/`
    )
    products.value = data
  } catch (e) {
    console.error('Failed to fetch products:', e)
  }
}

// 상품 유형 변경 시 재로딩
watch(productType, loadProducts)
onMounted(loadProducts)
</script>


<style scoped>
.products-list {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.filters {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.filters label {
  font-weight: 500;
  color: #666;
}

.filters select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.ml-4 {
  margin-left: 1rem;
}

.rates-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.rates-table th,
.rates-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.rates-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #2c3e50;
}

.product-name {
  padding: 0.75rem 1rem;
}

.product-name .name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.rate-cell {
  text-align: center;
  padding: 0.75rem 1rem;
}

.rate-info {
  font-size: 0.9em;
}

.base-rate {
  color: #2C5282;
  font-weight: 500;
  margin-left: 0.5rem;
}

.pref-rate {
  color: #E53E3E;
  margin-left: 0.25rem;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background-color: #f8fafc;
}
</style>