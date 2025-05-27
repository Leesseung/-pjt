<template>
  <div class="bank-search">
    <h1>은행 검색</h1>

    <div class="controls">
      <label>
        광역시/도
        <select v-model="selectedSido" @change="onSidoChange">
          <option value="">선택하세요</option>
          <option
            v-for="s in regionData.mapInfo"
            :key="s.name"
            :value="s.name"
          >
            {{ s.name }}
          </option>
        </select>
      </label>

      <label>
        시/군/구
        <select v-model="selectedSigungu" :disabled="!sigunguList.length">
          <option value="">선택하세요</option>
          <option
            v-for="g in sigunguList"
            :key="g"
            :value="g"
          >
            {{ g }}
          </option>
        </select>
      </label>

      <label>
        은행
        <select v-model="selectedBank">
          <option value="">선택하세요</option>
          <option
            v-for="b in regionData.bankInfo"
            :key="b"
            :value="b"
          >
            {{ b }}
          </option>
        </select>
      </label>

      <button @click="searchBanks" :disabled="!canSearch">
        검색
      </button>
    </div>

    <div id="map" class="map-container"></div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import dataUrl  from '@/assets/data.json?url'

// .env 에 저장한 Kakao REST API Key
const REST_KEY = import.meta.env.VITE_KAKAO_REST_KEY

// 화면 상태
const regionData      = reactive({ mapInfo: [], bankInfo: [] })
const selectedSido    = ref('')
const selectedSigungu = ref('')
const selectedBank    = ref('')

// ‘구’ 목록과 검색 가능 여부
const sigunguList = computed(() => {
  const entry = regionData.mapInfo.find(r => r.name === selectedSido.value)
  return entry ? entry.countries : []
})
const canSearch = computed(() =>
  selectedSido.value && selectedSigungu.value && selectedBank.value
)

let map, markers = [], infowindows = []

// 시/도 변경 시 구 초기화
function onSidoChange() {
  selectedSigungu.value = ''
}

// 마운트 시: data.json → kakao.maps.load → 지도 초기화
onMounted(async () => {
  // 1) data.json 로드
  const res = await fetch(dataUrl)
  Object.assign(regionData, await res.json())

  // 2) SDK 가 index.html 에서 로드된 후, kakao.maps.load() 호출
  if (!window.kakao || !window.kakao.maps) {
    alert('카카오 JS SDK가 로드되지 않았습니다.\npublic/index.html을 확인하세요.')
    return
  }

  // 지도를 autoload=false 방식으로 초기화
  kakao.maps.load(() => {
    const container = document.getElementById('map')
    map = new kakao.maps.Map(container, {
      center: new kakao.maps.LatLng(37.5665, 126.9780),
      level: 5
    })
  })
})

// 검색 버튼 클릭 시: REST API 호출 → 마커 표시
async function searchBanks() {
  // 기존 마커·인포윈도우 제거
  markers.forEach(m => m.setMap(null))
  infowindows.forEach(iw => iw.close())
  markers = []; infowindows = []

  const keyword = `${selectedSigungu.value} ${selectedBank.value}`
  const resp = await fetch(
    `https://dapi.kakao.com/v2/local/search/keyword.json
     ?query=${encodeURIComponent(keyword)}&size=15`,
    { headers: { Authorization: `KakaoAK ${REST_KEY}` } }
  )
  const { documents } = await resp.json()

  if (!documents.length) {
    alert('검색 결과가 없습니다.')
    return
  }

  // kakao.maps.load 내부에서 지도 동작 보장
  kakao.maps.load(() => {
    // 지도 중심 이동
    const first = documents[0]
    map.setCenter(new kakao.maps.LatLng(first.y, first.x))

    // 마커·인포윈도우 생성
    documents.forEach(place => {
      const pos    = new kakao.maps.LatLng(place.y, place.x)
      const marker = new kakao.maps.Marker({ map, position: pos })
      const iw     = new kakao.maps.InfoWindow({
        content: `<div>${place.place_name}</div>`
      })

      kakao.maps.event.addListener(marker, 'click', () => {
        infowindows.forEach(w => w.close())
        iw.open(map, marker)
      })

      markers.push(marker)
      infowindows.push(iw)
    })
  })
}
</script>

<style scoped>
.bank-search {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 1rem;
}
.controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 1rem;
}
label {
  display: flex;
  flex-direction: column;
  font-weight: 500;
}
select, button {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  background: #0073e6;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}
button:disabled {
  background: #aaa;
  cursor: not-allowed;
}
button:not(:disabled):hover {
  background: #005bb5;
}
.map-container {
  width: 100%;
  height: 500px;
  border: 2px solid #004080;
  border-radius: 8px;
}
</style>
