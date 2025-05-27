<template>
  <div class="search-view">
    <ArrowBack />
    <h1>비디오 검색</h1>
    <hr />
    <SearchInput class="search-input" @get-videos="getVideos" />
    <div v-if="isLoading" class="loading-container">
      <LoadingIcon />
    </div>
    <div v-else>
      <div v-if="videoList.length === 0" class="no-results">
        검색 결과가 없습니다.
      </div>
      <SearchVideoList v-else :video-list="videoList" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import dayjs from "dayjs";
import ArrowBack from "@/components/Common/ArrowBack.vue";
import LoadingIcon from "@/components/Common/LoadingIcon.vue";
import SearchInput from "@/components/Search/SearchInput.vue";
import SearchVideoList from "@/components/Search/SearchVideoList.vue";

const URL     = "https://www.googleapis.com/youtube/v3";
const API_KEY = import.meta.env.VITE_API_KEY;

const videoList = ref([]);
const isLoading = ref(false);

function getVideos(query) {
  isLoading.value = true;
  axios
    .get(`${URL}/search`, {
      params: {
        key: API_KEY,
        part: "snippet",
        type: "video",
        q: query,
        maxResults: 10,
      },
    })
    .then((res) => {
      videoList.value = res.data.items.map((item) => ({
        videoId:     item.id.videoId,
        title:       item.snippet.title,
        description: item.snippet.description,
        publishTime: dayjs(item.snippet.publishTime).format("YYYY-MM-DD"),
        thumbnails:  item.snippet.thumbnails,
      }));
    })
    .catch(console.error)
    .finally(() => {
      isLoading.value = false;
    });
}
</script>

<style scoped>
.search-view {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: #333333;
}

h1 {
  font-size: 1.75rem;
  color: #004080;
  margin-bottom: 0.5rem;
}

hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin-bottom: 1.5rem;
}

.search-input {
  margin-bottom: 1.5rem;
}

.loading-container,
.no-results {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40vh;
  font-size: 1.2rem;
  color: #666666;
}
</style>
