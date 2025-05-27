// frontend/src/stores/userStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/lib/axios";

export const useUserStore = defineStore("user", () => {
  const token    = ref(localStorage.getItem("token") || "");
  const userId   = ref(localStorage.getItem("userId") || null);
  const username = ref(localStorage.getItem("username") || "");

const isLogin  = computed(() => !!token.value)

  function _saveToken(t) {
    token.value = t;
    localStorage.setItem("token", t);
    console.log('[userStore] saved token:', t);  // ← 로그인 직후 찍히는지 확인
  }
  function _saveUserId(id) {
    userId.value = id;
    localStorage.setItem("userId", id);
  }
  function _saveUsername(u) {
    username.value = u;
    localStorage.setItem("username", u);
  }

  function _clearAll() {
    token.value = "";
    userId.value = null;
    username.value = "";
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    localStorage.removeItem("username");
  }

  async function logIn({ username: u, password }) {
    // DRF 기본 토큰 발급
    const res = await api.post("/api-token-auth/", { username: u, password });
    _saveToken(res.data.token);

    // 내 정보 조회
    const me = await api.get("/accounts/user/");
    _saveUserId(me.data.pk ?? me.data.id);
    _saveUsername(me.data.username);
  }

  async function signUp(payload) {
    await api.post("/accounts/registration/", payload);
  }

  function logOut() {
    _clearAll();
  }

  return {
    token,
    userId,
    username,
    isLogin,
    logIn,
    signUp,
    logOut,
  };
}, {
  persist: {
    key: "user",
    paths: ["token", "userId", "username"],
  },
});
