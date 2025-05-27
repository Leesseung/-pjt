<!-- frontend/src/components/community/CommentSection.vue -->
<template>
  <div>
    <h4>댓글</h4>
    <!-- 댓글 작성 폼 -->
    <CommentForm :postId="postId" @refresh="loadComments" />

    <!-- 댓글 리스트: 빈 배열이어도 <li> 가 없을 뿐 섹션은 보임 -->
    <ul>
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @refresh="loadComments"
      />
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/lib/axios'
import CommentForm from './CommentForm.vue'
import CommentItem from './CommentItem.vue'

const props    = defineProps({ postId: Number })
const comments = ref([])

// 댓글을 서버에서 가져오는 함수
async function loadComments() {
  try {
    const { data } = await api.get(`/community/posts/${props.postId}/comments/`)
    comments.value = data
  } catch (err) {
    console.error('댓글 로드 실패:', err)
  }
}

// 마운트 시 단 한 번만 불러오기
onMounted(loadComments)
</script>

<style scoped>
ul { list-style: none; padding: 0; }
li + li { margin-top: 0.5rem; }
</style>
