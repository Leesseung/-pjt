<template>
  <div>
    <div class="input-group modern-search">
      <input
        type="text"
        class="form-control modern-input"
        placeholder="검색어를 입력하세요"
        v-model="userInput"
        @keyup.enter="getSearchData"
      />
      <button class="btn modern-btn" type="button" @click="getSearchData">
        검색
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const userInput = ref("");

const emit = defineEmits(['getVideos'])

const getSearchData = () => {
  emit('getVideos', userInput.value)
}
</script>

<style scoped>
.modern-search {
  max-width: 360px;
  margin: 30px auto;
  display: flex;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.modern-input {
  flex-grow: 1;
  border: none;
  padding: 14px 20px;
  font-size: 1rem;
  color: #333;
  outline: none;
  transition: background-color 0.3s ease;
}

.modern-input::placeholder {
  color: #bbb;
}

.modern-input:focus {
  background-color: #f9f9f9;
}

.modern-btn {
 background: linear-gradient(45deg, #a3afc9, #486196);




  border: none;
  padding: 0 25px;
  cursor: pointer;
  color: white;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.modern-btn:hover {
  background: linear-gradient(45deg, #111f5c, #8896e2); 
}

</style>
