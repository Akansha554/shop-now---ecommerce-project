<template>
  <teleport to="body">
    <div class="toast-container">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast-${toast.type}`]">
          <span class="toast-icon">
            {{ toast.type === 'success' ? '' : toast.type === 'error' ? '' : 'ℹ' }}
          </span>
          {{ toast.message }}
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script>
export default {
  data() { return { toasts: [] } },
  methods: {
    show(message, type = 'success', duration = 3000) {
      const id = Date.now()
      this.toasts.push({ id, message, type })
      setTimeout(() => {
        this.toasts = this.toasts.filter(t => t.id !== id)
      }, duration)
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  min-width: 260px;
}
.toast-success { background: #00b894; }
.toast-error   { background: #d63031; }
.toast-info    { background: #6c5ce7; }
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(40px); }
.toast-leave-to   { opacity: 0; transform: translateX(40px); }
.toast-icon { font-size: 16px; }
</style>