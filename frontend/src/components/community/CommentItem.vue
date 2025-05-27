<template>
  <li class="comment-item">
    <p class="comment-header">
      <span class="comment-author">{{ comment.author_username }}</span>
      <span class="comment-date">{{ new Date(comment.created_at).toLocaleString() }}</span>
      <span v-if="comment.author === userStore.userId" class="comment-actions">
        <button class="btn btn-small btn-edit" @click="isEdit = true">수정</button>
        <button class="btn btn-small btn-delete" @click="remove()">삭제</button>
      </span>
    </p>

    <!-- 수정 폼 -->
    <div v-if="isEdit" class="comment-edit-form">
      <textarea v-model="editContent" class="edit-textarea" />
      <button class="btn btn-small btn-save" @click="update()">저장</button>
      <button class="btn btn-small btn-cancel" @click="cancel()">취소</button>
    </div>

    <!-- 댓글 내용 -->
    <div v-else class="comment-content">
      {{ comment.content }}
    </div>

    <!-- 답글 쓰기: 최상위 댓글에만 -->
    <button
      v-if="!comment.parent"
      class="btn btn-small btn-reply"
      @click="replying = !replying"
    >
      {{ replying ? '답글 취소' : '답글 쓰기' }}
    </button>

    <!-- 대댓글 입력 폼 -->
    <CommentForm
      v-if="replying"
      :postId="comment.post"
      :parentId="comment.id"
      @refresh="$emit('refresh')"
    />

    <!-- 답글 보기 토글 -->
    <div v-if="comment.replies.length" class="replies-section">
      <button class="btn btn-small btn-toggle" @click="showReplies = !showReplies">
        {{ showReplies ? '답글 숨기기' : `답글 보기 (${comment.replies.length})` }}
      </button>
      <ul v-if="showReplies" class="replies-list">
        <CommentItem
          v-for="child in comment.replies"
          :key="child.id"
          :comment="child"
          @refresh="$emit('refresh')"
        />
      </ul>
    </div>
  </li>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import api from '@/lib/axios'
import CommentForm from './CommentForm.vue'

const props = defineProps({ comment: Object })
const emit = defineEmits(['refresh'])
const userStore = useUserStore()

const isEdit      = ref(false)
const replying    = ref(false)
const showReplies = ref(false)
const editContent = ref(props.comment.content)

async function remove() {
  await api.delete(`/community/comments/${props.comment.id}/`)
  emit('refresh')
}
async function update() {
  await api.patch(`/community/comments/${props.comment.id}/`, { content: editContent.value })
  isEdit.value = false
  emit('refresh')
}
function cancel() {
  isEdit.value = false
  editContent.value = props.comment.content
}
</script>

<style scoped>
.comment-item {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #555;
}
.comment-author {
  font-weight: 500;
  color: #004080;
}
.comment-date {
  margin-left: 0.5rem;
  color: #888;
}
.comment-actions .btn {
  margin-left: 0.5rem;
}

.btn {
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  border: none;
  font-size: 0.8rem;
  cursor: pointer;
}
.btn-small { font-size: 0.75rem; }
.btn-edit { background-color: #fff; color: #004080; border: 1px solid #004080; }
.btn-delete { background-color: #e60000; color: #fff; }
.btn-save { background-color: #004080; color: #fff; }
.btn-cancel { background-color: #ccc; color: #333; }
.btn-reply { background: none; color: #004080; }
.btn-toggle { background: none; color: #004080; margin-top: 0.5rem; }

.comment-edit-form {
  margin-bottom: 0.5rem;
}
.edit-textarea {
  width: 100%;
  min-height: 60px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.comment-content {
  margin-bottom: 0.5rem;
  line-height: 1.4;
  color: #333;
}

.replies-section {
  margin-top: 0.5rem;
}
.replies-list {
  list-style: none;
  padding-left: 1rem;
}
</style>
