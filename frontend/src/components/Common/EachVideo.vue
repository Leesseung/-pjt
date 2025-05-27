<template>
  <div>
    <div
      class="video-card card text-bg-light border-secondary"
      @click="moveToDetail"
    >
      <div class="thumbnail-container" @mouseenter="isHovered = true" @mouseleave="isHovered = false">
        <img
          v-if="!isHovered"
          class="card-img-top"
          :src="thumbnailSrc"
          alt="video"
        />
        <iframe
          v-else
          class="card-img-top"
          :src="previewVideoUrl"
          title="YouTube video preview"
          frameborder="0"
          allow="autoplay; encrypted-media"
          allowfullscreen
        ></iframe>
      </div>

      <div class="card-body">
        <p class="card-title">{{ video.title }}</p>
        <p class="card-subtitle">{{ video.publishTime }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  video: Object
})

const video = props.video
const router = useRouter()

const isHovered = ref(false)

const thumbnailSrc = video.thumbnails.medium.url || video.thumbnails.default.url

const previewVideoUrl = `https://www.youtube.com/embed/${video.videoId}?autoplay=1&mute=1&controls=0&loop=1&playlist=${video.videoId}`

const moveToDetail = () => {
  router.push(`/videos/${video.videoId}`);
}
</script>

<style scoped>
.video-card {
  width: 300px;
  height: auto;
  cursor: pointer;
}

.thumbnail-container {
  width: 100%;
  height: 170px;
  overflow: hidden;
  position: relative;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-bottom: 1px solid #ccc;
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #666;
}
</style>
