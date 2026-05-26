<template>
  <div class="page-wrapper">
    <h2 class="section-title"> Your Cart</h2>

    <div v-if="!cartItems.length" class="empty-state">
      Your cart is empty. <router-link to="/" style="color:#6c5ce7">Shop now →</router-link>
    </div>

    <div v-else class="cart-layout">
      <div class="cart-items">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.product.image_url" :alt="item.product.title" class="cart-img" />
          <div class="cart-item-info">
            <h3>{{ item.product.title }}</h3>
            <p class="cart-item-price">₹{{ item.product.price.toFixed(2) }}</p>
          </div>
          <div class="qty-controls">
            <button @click="update(item.id, 'decrease')">−</button>
            <span>{{ item.quantity }}</span>
            <button @click="update(item.id, 'increase')">+</button>
          </div>
          <p class="item-subtotal">₹{{ (item.product.price * item.quantity).toFixed(2) }}</p>
          <button class="btn-danger" style="padding:8px 12px" @click="remove(item.id)">🗑</button>
        </div>
      </div>

      <div class="cart-summary">
        <h3 style="margin-bottom:16px;font-weight:700">Order Summary</h3>
        <div class="summary-row"><span>Items ({{ cartCount }})</span><span>₹{{ cartTotal.toFixed(2) }}</span></div>
        <div class="summary-row"><span>Shipping</span><span style="color:#00b894">Free</span></div>
        <div class="summary-divider"></div>
        <div class="summary-row total-row"><span>Total</span><span>₹{{ cartTotal.toFixed(2) }}</span></div>

        <div style="margin-top:20px">
          <label style="display:block;font-size:13px;font-weight:600;margin-bottom:6px">Payment Mode</label>
          <select v-model="paymentMode" style="margin-bottom:16px">
            <option value="COD">Cash on Delivery</option>
            <option value="ONLINE">Online Payment</option>
          </select>
        </div>

        <button class="btn-primary" style="width:100%" @click="checkout">
          Place Order
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  data() { return { paymentMode: 'COD' } },
  computed: {
    ...mapGetters('cart', ['cartItems', 'cartCount', 'cartTotal'])
  },
  mounted() { this.$store.dispatch('cart/fetchCart') },
  methods: {
    ...mapActions('cart', ['updateQuantity', 'removeFromCart']),
    update(cart_id, action) { this.updateQuantity({ cart_id, action }) },
    remove(cart_id) { this.removeFromCart(cart_id) },
    async checkout() {
      const user = this.$store.getters['auth/currentUser']
      for (const item of this.cartItems) {
        await this.$store.dispatch('orders/createOrder', {
          user_id: user.id,
          product_id: item.product.id,
          quantity: item.quantity,
          payment_mode: this.paymentMode
        })
        await this.$store.dispatch('cart/removeFromCart', item.id)
      }
      alert(' Order placed successfully!')
      this.$router.push('/orders')
    }
  }
}
</script>

<style scoped>
.cart-layout { display: flex; gap: 24px; align-items: flex-start; }
.cart-items { flex: 1; display: flex; flex-direction: column; gap: 16px; }
.cart-item {
  background: white; border-radius: 12px; padding: 16px;
  display: flex; align-items: center; gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.cart-img { width: 80px; height: 80px; border-radius: 10px; object-fit: cover; }
.cart-item-info { flex: 1; }
.cart-item-info h3 { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
.cart-item-price { color: #6c5ce7; font-weight: 600; }
.qty-controls { display: flex; align-items: center; gap: 10px; }
.qty-controls button {
  width: 30px; height: 30px; border-radius: 50%;
  background: #f0f0f0; color: #2d3436;
  font-size: 18px; display: flex; align-items: center; justify-content: center;
  padding: 0;
}
.qty-controls span { font-size: 16px; font-weight: 700; min-width: 24px; text-align: center; }
.item-subtotal { font-size: 16px; font-weight: 700; min-width: 80px; text-align: right; }
.cart-summary {
  width: 300px; flex-shrink: 0;
  background: white; border-radius: 16px; padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  position: sticky; top: 80px;
}
.summary-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 15px; }
.summary-divider { border-top: 1px solid #f0f0f0; margin: 12px 0; }
.total-row { font-size: 18px; font-weight: 800; color: #2d3436; }
</style>