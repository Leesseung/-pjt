<template>
  <div>
    <ul class="video-list-ul">
      <li
        class="video-list-li"
        v-for="video in videoList"
        :key="video.videoId"
      >
      <EachVideo :video="video" />
      </li>
    </ul>
  </div>
</template>

<script setup>
import EachVideo from "@/components/Common/EachVideo.vue";

const props = defineProps({
  videoList: Array
})

</script>
