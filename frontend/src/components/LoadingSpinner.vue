<template>
  <div class="spinner-wrap">
    <div class="spinner"></div>
    <p v-if="message" class="spinner-msg">{{ message }}</p>
  </div>
</template>

<script>
export default {
  props: {
    message: { type: String, default: 'Loading...' }
  }
}
</script>

<style scoped>
.spinner-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e0e0e0;
  border-top-color: #6c5ce7;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.spinner-msg {
  margin-top: 14px;
  font-size: 14px;
  color: #636e72;
}
</style>