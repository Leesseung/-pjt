<template>
  <div class="detail-view">
    <LoadingIcon v-if="isLoading" />
    <div v-else>
      <ArrowBack />
      <h1>{{ video.title }}</h1>
      <div class="upload-date">업로드 날짜: {{ video.publishedAt }}</div>
      <div class="video-wrapper">
        <iframe
          :src="videoSrc"
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media;
                 gyroscope; picture-in-picture; web-share"
          allowfullscreen
        ></iframe>
      </div>
      <p class="description">{{ video.description }}</p>

      <div class="button-group">
        <button
          v-if="isLaterVideo"
          type="button"
          class="btn-outline-danger"
          @click="unregisterLaterVideo"
        >
          저장 취소
        </button>
        <button
          v-else
          type="button"
          class="btn-primary"
          @click="registerLaterVideo"
        >
          동영상 저장
        </button>

        <button
          :class="['btn', 'btn-channel', isChannelSaved ? 'saved' : '']"
          @click="saveChannel"
        >
          {{ isChannelSaved ? '⭐ 채널 저장됨' : '☆ 채널 저장' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import dayjs from "dayjs";
import { useRoute, useRouter } from "vue-router";
import ArrowBack from "@/components/Common/ArrowBack.vue";
import LoadingIcon from "@/components/Common/LoadingIcon.vue";
import { ref } from "vue";

const route = useRoute();
const router = useRouter();

const detailURL = "https://www.googleapis.com/youtube/v3/videos";
const API_KEY = import.meta.env.VITE_API_KEY;

const isLoading = ref(true);
const video = ref({});
const videoSrc = ref("");
const isLaterVideo = ref(false);
const isChannelSaved = ref(false);

const checkVideoInStorage = () => {
  const raw = localStorage.getItem("laterVideoList");
  if (!raw) return false;
  return JSON.parse(raw).arr.includes(video.value.videoId);
};

const unregisterLaterVideo = () => {
  const raw = localStorage.getItem("laterVideoList");
  if (!raw) return;
  const list = JSON.parse(raw);
  list.arr = list.arr.filter(id => id !== video.value.videoId);
  localStorage.setItem("laterVideoList", JSON.stringify(list));
  isLaterVideo.value = false;
};

const checkChannelInStorage = () => {
  const raw = localStorage.getItem("savedChannels");
  if (!raw) return false;
  return JSON.parse(raw).channels.some(c => c.channelId === video.value.channelId);
};

const saveChannel = () => {
  const channelData = {
    channelId: video.value.channelId,
    channelTitle: video.value.channelTitle,
  };
  const raw = localStorage.getItem("savedChannels");
  const list = raw ? JSON.parse(raw) : { channels: [] };
  if (!list.channels.find(c => c.channelId === channelData.channelId)) {
    list.channels.push(channelData);
    localStorage.setItem("savedChannels", JSON.stringify(list));
    isChannelSaved.value = true;
  }
};

const registerLaterVideo = () => {
  const raw = localStorage.getItem("laterVideoList");
  const list = raw ? JSON.parse(raw) : { arr: [] };
  if (!list.arr.includes(video.value.videoId)) {
    list.arr.push(video.value.videoId);
    localStorage.setItem("laterVideoList", JSON.stringify(list));
    isLaterVideo.value = true;
  }
};

axios.get(detailURL, {
    params: { key: API_KEY, part: "snippet", id: route.params.videoId }
  })
  .then(res => {
    const item = res.data.items[0].snippet;
    video.value = {
      videoId: route.params.videoId,
      title:   item.title,
      description: item.description,
      publishedAt: dayjs(item.publishedAt).format("YYYY-MM-DD"),
      channelId:   item.channelId,
      channelTitle: item.channelTitle,
    };
    videoSrc.value = `https://www.youtube.com/embed/${route.params.videoId}`;
    isLaterVideo.value    = checkVideoInStorage();
    isChannelSaved.value  = checkChannelInStorage();
  })
  .catch(console.error)
  .finally(() => { isLoading.value = false; });
</script>

<style scoped>
.detail-view {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  color: #333;
}

h1 {
  font-size: 1.8rem;
  color: #004080;
  margin-bottom: 0.5rem;
}

.upload-date {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.video-wrapper {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  margin-bottom: 1.5rem;
}
.video-wrapper iframe {
  position: absolute;
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 8px;
}

.description {
  line-height: 1.5;
  margin-bottom: 2rem;
  color: #555;
}

.button-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
  border: none;
}

.btn-primary {
  background: #0073e6;
  color: white;
}
.btn-primary:hover {
  background: #005bb5;
}

.btn-outline-danger {
  background: #ffffff;
  color: #e55353;
  border: 1px solid #e55353;
}
.btn-outline-danger:hover {
  background: #e55353;
  color: white;
}

.btn-channel {
  background: #ffc107;
  color: #333;
}
.btn-channel.saved {
  background: #28a745;
  color: white;
}
.btn-channel:hover {
  opacity: 0.85;
}
</style>
