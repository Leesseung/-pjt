<template>
  <div class="later-view">
    <h1>나중에 볼 동영상</h1>
    <hr />

    <LoadingIcon v-if="isLoading" />
    <div v-else>
      <div v-if="isLaterVideo">
        <LaterVideoList :laterVideoList="laterVideoList" />
      </div>
      <div v-else class="no-videos">등록된 비디오가 없습니다.</div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import dayjs from "dayjs";
import { ref, onMounted } from "vue";
import LaterVideoList from "@/components/Later/LaterVideoList.vue";
import ArrowBack from "@/components/Common/ArrowBack.vue";
import LoadingIcon from "@/components/Common/LoadingIcon.vue";

const URL     = "https://www.googleapis.com/youtube/v3/videos";
const API_KEY = import.meta.env.VITE_API_KEY;

const laterVideoList = ref([]);
const isLaterVideo   = ref(false);
const isLoading      = ref(false);

function setLaterVideoList(videoIds) {
  videoIds.forEach((videoId) => {
    axios
      .get(URL, {
        params: { key: API_KEY, part: "snippet", id: videoId },
      })
      .then((res) => {
        const item = res.data.items[0].snippet;
        laterVideoList.value.push({
          videoId:    videoId,
          title:      item.title,
          description:item.description,
          publishTime: dayjs(item.publishedAt).format("YYYY-MM-DD"),
          thumbnails: item.thumbnails,
          channelId:  item.channelId,
        });
      })
      .catch(console.error);
  });
}

onMounted(() => {
  isLoading.value = true;
  const raw = localStorage.getItem("laterVideoList");
  if (raw) {
    const parsed = JSON.parse(raw);
    if (parsed.arr?.length) {
      setLaterVideoList(parsed.arr);
      isLaterVideo.value = true;
    }
  }
  isLoading.value = false;
});
</script>

<style scoped>
.later-view {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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

.no-videos {
  text-align: center;
  color: #666;
  font-size: 1rem;
  padding: 2rem 0;
}

.video-card {
  background: #f7f9fc;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}
</style>
