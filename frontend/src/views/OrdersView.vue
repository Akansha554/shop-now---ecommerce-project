<template>
  <div class="page-wrapper">
    <h2 class="section-title"> My Orders</h2>

    <div v-if="loading" class="empty-state">Loading orders...</div>
    <div v-else-if="!orders.length" class="empty-state">
      No orders yet. <router-link to="/" style="color:#6c5ce7">Start shopping →</router-link>
    </div>

    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card" :class="{ cancelled: order.is_cancelled }">
        <div class="order-image">
          <img :src="order.product.image_url" :alt="order.product.title" />
        </div>
        <div class="order-info">
          <h3>{{ order.product.title }}</h3>
          <p>Qty: <strong>{{ order.quantity }}</strong> &nbsp;|&nbsp; Price: <strong>₹{{ order.price.toFixed(2) }}</strong></p>
          <p>Total: <strong style="color:#6c5ce7">₹{{ (order.price * order.quantity).toFixed(2) }}</strong></p>
          <p style="font-size:13px;color:#636e72;margin-top:4px">
            Payment: {{ order.payment_mode }} &nbsp;|&nbsp;
            Date: {{ new Date(order.ordered_at).toLocaleDateString() }}
          </p>
        </div>
        <div class="order-status">
          <span v-if="order.is_cancelled" class="badge-sold">Cancelled</span>
          <span v-else class="badge-sale">Active</span>
          <button
            v-if="!order.is_cancelled"
            class="btn-danger"
            style="margin-top:10px;padding:8px 14px;font-size:13px"
            @click="cancel(order.id)">
            Cancel Order
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'
export default {
  computed: {
    ...mapGetters('orders', ['allOrders']),
    ...mapState('orders', ['loading']),
    orders() { return this.allOrders }
  },
  mounted() { this.$store.dispatch('orders/fetchOrders') },
  methods: {
    ...mapActions('orders', ['cancelOrder']),
    async cancel(order_id) {
      if (confirm('Cancel this order?')) {
        await this.cancelOrder(order_id)
      }
    }
  }
}
</script>

<style scoped>
.orders-list { display: flex; flex-direction: column; gap: 16px; }
.order-card {
  background: white; border-radius: 14px; padding: 20px;
  display: flex; gap: 20px; align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  border-left: 4px solid #6c5ce7;
}
.order-card.cancelled { border-left-color: #d63031; opacity: 0.7; }
.order-image img { width: 90px; height: 90px; border-radius: 10px; object-fit: cover; }
.order-info { flex: 1; }
.order-info h3 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.order-info p { font-size: 14px; color: #636e72; margin-bottom: 4px; }
.order-status { display: flex; flex-direction: column; align-items: flex-end; min-width: 110px; }
</style>