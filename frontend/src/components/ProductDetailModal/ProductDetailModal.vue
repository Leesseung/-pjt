<!-- src/components/ProductDetailModal/ProductDetailModal.vue -->
<template>
  <div
    v-if="product"
    class="modal-overlay"
    @click.self="$emit('close')"
  >
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ product.fin_prdt_nm }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div class="modal-body">
        <!-- 은행명 -->
        <div class="bank-info">
          <h3>{{ product.kor_co_nm }}</h3>
        </div>

        <!-- 금리 테이블 -->
        <div class="rates-table">
          <table>
            <thead>
              <tr>
                <th>가입기간</th>
                <th>기본금리</th>
                <th>우대금리</th>
                <th>금리유형</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="opt in sortedOptions"
                :key="opt.save_trm"
              >
                <td>{{ opt.save_trm }}개월</td>
                <td>{{ opt.intr_rate.toFixed(2) }}%</td>
                <td>{{ opt.intr_rate2.toFixed(2) }}%</td>
                <td>{{ opt.intr_rate_type_nm }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 가입 기간 선택 -->
        <div
          v-if="userStore.isLogin && !isSubscribed"
          class="date-selection"
        >
          <h4>가입 기간 선택</h4>
          <div class="date-inputs">
            <div class="form-group">
              <label>시작일</label>
              <input
                type="date"
                v-model="startDate"
                :min="today"
                @change="updateEndDate"
              />
            </div>
            <div class="form-group">
              <label>가입 기간</label>
              <select
                v-model="selectedTerm"
                @change="updateEndDate"
              >
                <option
                  v-for="opt in sortedOptions"
                  :key="opt.save_trm"
                  :value="opt.save_trm"
                >
                  {{ opt.save_trm }}개월
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>만기일</label>
              <input
                type="date"
                v-model="endDate"
                disabled
              />
            </div>
          </div>
        </div>

        <!-- 상세 정보 -->
        <div class="product-details">
          <div class="detail-section">
            <h4>가입방법</h4>
            <p>{{ product.join_way }}</p>
          </div>
          <div class="detail-section">
            <h4>가입대상</h4>
            <p>{{ product.join_member }}</p>
          </div>
          <div class="detail-section">
            <h4>우대조건</h4>
            <p>{{ product.spcl_cnd }}</p>
          </div>
          <div class="detail-section">
            <h4>기타 유의사항</h4>
            <p>{{ product.etc_note }}</p>
          </div>
        </div>

        <!-- 가입/해지 버튼 -->
        <div class="action-area">
          <button
            v-if="userStore.isLogin && !isSubscribed"
            class="subscribe-btn"
            :disabled="!isValidSubscription"
            @click="onSubscribe"
          >
            가입하기
          </button>
          <button
            v-else-if="userStore.isLogin && isSubscribed"
            class="unsubscribe-btn"
            @click="onUnsubscribe"
          >
            가입 취소
          </button>
          <RouterLink
            v-else
            to="/login"
            class="subscribe-btn"
          >
            로그인 후 가입
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import dayjs from 'dayjs'

const props = defineProps({
  product: { type: Object, required: true }
})

const router = useRouter()
const userStore = useUserStore()

// 날짜
const today = dayjs().format('YYYY-MM-DD')
const startDate = ref(today)
const endDate = ref('')
const selectedTerm = ref(null)

// 옵션 정렬
const sortedOptions = computed(() =>
  [...(props.product.options || [])].sort(
    (a, b) => a.save_trm - b.save_trm
  )
)

// 예·적금 구분
const productType = computed(
  () => props.product.type || 'deposit'
)

// 이미 구독 여부
const isSubscribed = computed(() =>
  userStore.subscriptions?.some(
    s => s.fin_prdt_cd === props.product.fin_prdt_cd
  )
)

// 가입 유효성
const isValidSubscription = computed(
  () =>
    startDate.value &&
    endDate.value &&
    selectedTerm.value
)

function updateEndDate() {
  if (startDate.value && selectedTerm.value) {
    endDate.value = dayjs(startDate.value)
      .add(selectedTerm.value, 'month')
      .format('YYYY-MM-DD')
  }
}

async function onSubscribe() {
  try {
    const endpoint =
      productType.value === 'saving'
        ? 'saving-products'
        : 'deposit-products'

    // ↓ 여기서 '/api/v1' 을 빼고 relative 경로만 사용합니다
    await api.post(
      `products/${endpoint}/subscribe/${props.product.fin_prdt_cd}/`,
      {
        term_months: selectedTerm.value,
        start_date: startDate.value,
        end_date: endDate.value
      }
    )
    router.push({ name: 'MyProductsView' })
  } catch (err) {
    console.error(err)
    alert('가입이 완료되었습니다.')
  }
}

async function onUnsubscribe() {
  try {
    const endpoint =
      productType.value === 'saving'
        ? 'saving-products'
        : 'deposit-products'

    await api.delete(
      `products/${endpoint}/subscribe/${props.product.fin_prdt_cd}/`
    )
    router.push({ name: 'MyProductsView' })
  } catch (err) {
    console.error(err)
    alert('가입이 완료되었습니다.')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  font-size: 1.5rem;
  color: #1a365d;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0.5rem;
}

.bank-info {
  margin-bottom: 1.5rem;
}

.bank-info h3 {
  color: #2563eb;
  font-size: 1.25rem;
}

.rates-table {
  margin: 1.5rem 0;
  overflow-x: auto;
}

.rates-table table {
  width: 100%;
  border-collapse: collapse;
}

.rates-table th,
.rates-table td {
  padding: 0.75rem 1rem;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.rates-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #1e293b;
}

.rates-table td {
  color: #334155;
}

.date-selection {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.date-selection h4 {
  color: #1e293b;
  margin-bottom: 1rem;
}

.date-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  color: #4b5563;
}

.form-group input,
.form-group select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

.product-details {
  margin-top: 2rem;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  color: #1e293b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.detail-section p {
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.action-area {
  margin-top: 1.5rem;
  text-align: center;
}

.subscribe-btn,
.unsubscribe-btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  display: inline-block;
}

.subscribe-btn {
  background-color: #0073e6;
  color: #fff;
}

.subscribe-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.subscribe-btn:not(:disabled):hover {
  background-color: #005bb5;
}

.unsubscribe-btn {
  background-color: #dc2626;
  color: #fff;
}

.unsubscribe-btn:hover {
  background-color: #b91c1c;
}
</style>