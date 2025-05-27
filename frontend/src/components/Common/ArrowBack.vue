<template>
  <div>
    <router-link class="arrow-back-container" to="/">
      <span class="arrow-back-icon material-symbols-outlined">
      </span>
      <span class="arrow-back-text">뒤로가기</span>
    </router-link>
  </div>
</template>

<style scoped>
.arrow-back-container {
  display: flex;
  align-items: center;
  text-decoration-line: none;
  color: #e0e0e0; 
  width: fit-content;
  gap: 5px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7); 
  transition: color 0.3s ease, font-weight 0.3s ease;
}

.arrow-back-container:hover {
  color: #000000; 
  font-weight: bold;
}

.arrow-back-text {
  font-size: 1.2rem;
}

.arrow-back-icon {
  font-size: 1.4rem;
  color: inherit; 
}
</style>
