<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ subscription.product_name }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="bank-info">
          <h3>{{ subscription.bank_name }}</h3>
        </div>

        <div class="subscription-details">
          <div class="detail-row">
            <span class="label">가입기간:</span>
            <span class="value">{{ subscription.term_months }}개월</span>
          </div>
          <div class="detail-row">
            <span class="label">시작일:</span>
            <span class="value">{{ formatDate(subscription.start_date) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">만기일:</span>
            <span class="value">{{ formatDate(subscription.end_date) }}</span>
          </div>
          <div class="detail-row highlight">
            <span class="label">남은 기간:</span>
            <span class="value">{{ subscription.remaining_days }}일</span>
          </div>
        </div>

        <div class="actions">
          <button class="btn-cancel" @click="cancelSubscription">
            가입 취소
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import dayjs from 'dayjs'
import api from '@/lib/axios'

const props = defineProps({
  subscription: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'cancelled'])

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD')
}

async function cancelSubscription() {
  try {
    // Get the product type from the subscription
    const isDeposit = props.subscription.product_name.includes('예금')
    const endpoint = isDeposit ? 'deposit-products' : 'saving-products'
    
    // Make the DELETE request with the correct product code
    await api.delete(`/api/v1/products/${endpoint}/subscribe/${props.subscription.product.fin_prdt_cd}/`)
    
    alert('가입이 취소되었습니다.')
    emit('cancelled')
    emit('close')
  } catch (err) {
    console.error('Subscription cancellation failed:', err)
    alert('가입 취소 중 오류가 발생했습니다.')
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
  max-width: 600px;
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

.subscription-details {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-row.highlight {
  background: #e8f4ff;
  margin: 0 -1.5rem;
  padding: 0.75rem 1.5rem;
  color: #1e40af;
  font-weight: 500;
}

.label {
  color: #64748b;
  font-weight: 500;
}

.value {
  color: #1e293b;
  font-weight: 500;
}

.actions {
  text-align: center;
}

.btn-cancel {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-cancel:hover {
  background: #b91c1c;
}
</style>