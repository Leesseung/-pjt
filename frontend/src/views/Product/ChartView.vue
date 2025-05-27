<template>
  <div class="chart-view">
    <h2>금융 시세 차트</h2>
    
    <div class="chart-tabs">
      <button 
        :class="['tab-btn', { active: selectedCommodity === 'gold' }]"
        @click="selectedCommodity = 'gold'"
      >
        금(Gold)
      </button>
      <button 
        :class="['tab-btn', { active: selectedCommodity === 'silver' }]"
        @click="selectedCommodity = 'silver'"
      >
        은(Silver)
      </button>
    </div>

    <CommodityChart 
      :commodity="selectedCommodity"
      :key="selectedCommodity"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CommodityChart from '@/components/Chart/CommodityChart.vue'

const selectedCommodity = ref('gold')
</script>

<style scoped>
.chart-view {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h2 {
  color: #004080;
  margin-bottom: 2rem;
  text-align: center;
}

.chart-tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.tab-btn {
  padding: 0.75rem 2rem;
  border: 2px solid #004080;
  border-radius: 6px;
  background: #ffffff;
  color: #004080;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #f0f7ff;
}

.tab-btn.active {
  background: #004080;
  color: #ffffff;
}
</style>