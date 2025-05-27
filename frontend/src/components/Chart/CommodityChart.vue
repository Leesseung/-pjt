<template>
  <div class="chart-container">
    <div v-if="commodity === 'gold'" class="data-info">
      * Data available for the last 3 years only
    </div>
    <div class="chart-controls">
      <div class="date-range">
        <label>
          Start Date:
          <input 
            type="date" 
            v-model="startDate" 
            @change="updateChart"
          >
        </label>
        <label>
          End Date:
          <input 
            type="date" 
            v-model="endDate" 
            @change="updateChart"
          >
        </label>
      </div>
    </div>
    <div v-if="noDataMessage" class="no-data-message">
      {{ noDataMessage }}
    </div>
    <Line
      v-else-if="chartData.datasets.length > 0"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import api from '@/lib/axios'

const props = defineProps({
  commodity: {
    type: String,
    required: true,
    validator: value => ['gold', 'silver'].includes(value)
  },
  years: {
    type: Number,
    default: 1
  }
})

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const startDate = ref('')
const endDate = ref('')
const priceData = ref([])
const noDataMessage = ref('')

const chartData = computed(() => {
  let filteredData = priceData.value

  if (startDate.value && endDate.value) {
    filteredData = priceData.value.filter(item => 
      item.date >= startDate.value && item.date <= endDate.value
    )
    
    if (filteredData.length === 0) {
      noDataMessage.value = 'The selected data does not exist'
      return { labels: [], datasets: [] }
    }
  }

  noDataMessage.value = ''
  return {
    labels: filteredData.map(item => item.date),
    datasets: [
      {
        label: `${props.commodity.charAt(0).toUpperCase() + props.commodity.slice(1)} Price (USD)`,
        borderColor: props.commodity === 'gold' ? '#FFD700' : '#C0C0C0',
        data: filteredData.map(item => item.price),
        tension: 0.1
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      onClick: () => {}
    },
    title: {
      display: true,
      text: `${props.commodity.charAt(0).toUpperCase() + props.commodity.slice(1)} Price Trend (USD)`
    }
  },
  scales: {
    y: {
      beginAtZero: false,
      title: {
        display: true,
        text: 'Price (USD)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Date'
      }
    }
  }
}

const fetchData = async () => {
  try {
    const years = props.commodity === 'gold' ? 3 : 1
    const response = await api.get(`commodities/${props.commodity}`, {
      params: { years }
    })
    priceData.value = response.data

    if (priceData.value.length > 0) {
      const dates = priceData.value.map(item => item.date).sort()
      startDate.value = dates[0]
      endDate.value = dates[dates.length - 1]
    }
  } catch (error) {
    console.error('Error fetching data:', error)
    noDataMessage.value = 'Error loading data'
  }
}

const updateChart = () => {
  if (!startDate.value || !endDate.value) return
  if (startDate.value > endDate.value) {
    const temp = startDate.value
    startDate.value = endDate.value
    endDate.value = temp
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.chart-container {
  height: 400px;
  padding: 20px;
  position: relative;
  margin-bottom: 40px;
}

.chart-controls {
  margin-bottom: 20px;
}

.date-range {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 20px;
}

.date-range label {
  display: flex;
  gap: 10px;
  align-items: center;
}

input[type="date"] {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.no-data-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #666;
  font-size: 1.2em;
}

.data-info {
  position: absolute;
  top: 10px;
  right: 30px;
  color: #666;
  font-size: 0.9em;
  font-style: italic;
}
</style>