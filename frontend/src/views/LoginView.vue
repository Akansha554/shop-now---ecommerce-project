<template>
  <div class="page-wrapper">
    <div class="login-card">
      <h2 class="section-title">Login to ShopNow</h2>

      <div v-if="!otpSent">
        <label>Mobile Number</label>
        <input v-model="mobile" type="tel" placeholder="Enter 10-digit mobile number" />
        <button class="btn-primary" style="margin-top:16px;width:100%" @click="handleSendOtp" :disabled="loading">
          {{ loading ? 'Sending...' : 'Send OTP' }}
        </button>
      </div>

      <div v-else>
        <p style="margin-bottom:16px;color:#636e72">OTP sent to {{ mobile }}</p>
        <label>Enter OTP</label>
        <input v-model="otp" type="text" placeholder="6-digit OTP" maxlength="6" />
        <label style="margin-top:12px;display:block">Full Name (optional)</label>
        <input v-model="fullName" type="text" placeholder="Your name" />
        <button class="btn-primary" style="margin-top:16px;width:100%" @click="handleVerifyOtp" :disabled="loading">
          {{ loading ? 'Verifying...' : 'Verify & Login' }}
        </button>
        <button class="btn-outline" style="margin-top:10px;width:100%" @click="otpSent = false">
          Change Number
        </button>

        <div v-if="devOtp" style="margin-top:16px;padding:12px;background:#f0f0f0;border-radius:8px;font-size:13px">
          🔧 Dev mode OTP: <strong>{{ devOtp }}</strong>
        </div>
      </div>

      <p v-if="error" style="color:#d63031;margin-top:12px">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  data() {
    return { mobile: '', otp: '', fullName: '', otpSent: false, devOtp: null }
  },
  computed: {
    ...mapState('auth', ['loading', 'error'])
  },
  methods: {
    ...mapActions('auth', ['sendOtp', 'verifyOtp']),
    async handleSendOtp() {
      if (!this.mobile) return
      const res = await this.sendOtp(this.mobile)
      if (res) {
        this.otpSent = true
        this.devOtp = res.otp  // shown only in development
      }
    },
    async handleVerifyOtp() {
      try {
        await this.verifyOtp({ mobile: this.mobile, otp: this.otp, full_name: this.fullName })
        await this.$store.dispatch('cart/fetchCart')
        this.$router.push('/')
      } catch {}
    }
  }
}
</script>

<style scoped>
.login-card {
  max-width: 420px;
  margin: 60px auto;
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; margin-top: 12px; color: #636e72; }
</style>