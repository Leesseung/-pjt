<script setup>
import EachVideo from "@/components/Common/EachVideo.vue";

const props = defineProps(['laterVideoList'])

</script>

<template>
  <div>
    <ul class="video-list-ul">
      <li
        class="video-list-li"
        v-for="video in props.laterVideoList"
        :key="video.videoId"
      >
        <EachVideo :video="video" />
      </li>
    </ul>
  </div>
</template>

