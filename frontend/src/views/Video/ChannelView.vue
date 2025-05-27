<template>
  <div class="channel-container">
    <h2>⭐ 저장된 채널</h2>
    <hr />

    <ArrowBack />

    <ul class="channel-list">
      <li
        v-for="channel in channels"
        :key="channel.channelId"
        class="channel-item"
      >
        <span class="channel-title">{{ channel.channelTitle || '유튜브 바로가기' }}</span>

        <div class="actions">
          <a
            :href="`https://www.youtube.com/channel/${channel.channelId}`"
            target="_blank"
            class="btn-link"
          >
            이동
          </a>
          <button
            @click="removeChannel(channel.channelId)"
            class="btn-outline"
          >
            저장 취소
          </button>
        </div>
      </li>
    </ul>

    <div v-if="channels.length === 0" class="no-channels">
      저장된 채널이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ArrowBack from "@/components/Common/ArrowBack.vue";

const channels = ref([]);

onMounted(() => {
  loadChannels();
});

function loadChannels() {
  const raw = localStorage.getItem("savedChannels");
  if (raw) {
    const parsed = JSON.parse(raw);
    channels.value = parsed.channels || [];
  }
}

function removeChannel(channelId) {
  channels.value = channels.value.filter(c => c.channelId !== channelId);
  localStorage.setItem(
    "savedChannels",
    JSON.stringify({ channels: channels.value })
  );
}
</script>

<style scoped>
.channel-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.75rem;
  color: #004080;
  margin-bottom: 1rem;
}

hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin-bottom: 1.5rem;
}

.channel-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.channel-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f7f9fc;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  transition: background-color 0.2s ease;
}

.channel-item:hover {
  background-color: #e8f0fe;
}

.channel-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333333;
}

.actions {
  display: flex;
  gap: 0.75rem;
}

.btn-link,
.btn-outline {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* 파란색 테두리 버튼 */
.btn-outline {
  border: 1px solid #0073e6;
  background-color: #ffffff;
  color: #0073e6;
}

.btn-outline:hover {
  background-color: #0073e6;
  color: #ffffff;
}

/* 이동 링크를 버튼처럼 */
.btn-link {
  border: 1px solid #004080;
  background-color: #ffffff;
  color: #004080;
}

.btn-link:hover {
  background-color: #004080;
  color: #ffffff;
}

.no-channels {
  margin-top: 2rem;
  text-align: center;
  color: #888888;
  font-style: italic;
}
</style>
