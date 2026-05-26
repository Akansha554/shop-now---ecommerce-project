<template>
  <div>
    <nav class="navbar">
      <div class="nav-inner">
        <router-link to="/" class="nav-brand">🛍️ ShopNow</router-link>
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <router-link to="/cart" class="cart-link">
             Cart
            <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
          </router-link>
          <router-link to="/orders">Orders</router-link>
          <router-link to="/wishlist"> Wishlist</router-link>
          <template v-if="isLoggedIn">
            <span class="nav-user"> {{ user.full_name || user.mobile }}</span>
            <button class="btn-logout" @click="handleLogout">Logout</button>
          </template>
          <router-link v-else to="/login" class="btn-login">Login</router-link>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { mapGetters as mapCartGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters('auth', ['isLoggedIn', 'currentUser']),
    ...mapGetters('cart', ['cartCount']),
    user() { return this.currentUser || {} }
  },
  methods: {
    handleLogout() {
      this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.navbar {
  background: #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-brand { font-size: 20px; font-weight: 800; color: #6c5ce7; }
.nav-links { display: flex; align-items: center; gap: 20px; font-size: 15px; }
.nav-links a { color: #2d3436; font-weight: 500; }
.nav-links a.router-link-active { color: #6c5ce7; }
.cart-link { position: relative; }
.cart-badge {
  position: absolute;
  top: -8px; right: -10px;
  background: #d63031;
  color: white;
  font-size: 10px;
  font-weight: 700;
  width: 18px; height: 18px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.nav-user { color: #636e72; font-size: 14px; }
.btn-logout {
  background: #dfe6e9;
  color: #2d3436;
  padding: 6px 14px;
  font-size: 13px;
}
.btn-login {
  background: #6c5ce7;
  color: white !important;
  padding: 7px 16px;
  border-radius: 8px;
  font-weight: 600;
}
</style>