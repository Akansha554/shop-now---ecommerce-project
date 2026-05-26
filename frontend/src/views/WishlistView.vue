<template>
  <div class="page-wrapper">
    <h2 class="section-title"> My Wishlist</h2>

    <div v-if="!wishlistItems.length" class="empty-state">
      Your wishlist is empty.
      <router-link to="/" style="color:#6c5ce7"> Browse products →</router-link>
    </div>

    <div v-else class="product-grid">
      <div v-for="item in wishlistItems" :key="item.id" class="wish-card">
        <router-link :to="`/product/${item.product.id}`">
          <img :src="item.product.image_url" :alt="item.product.title" class="wish-img" />
          <div class="wish-info">
            <p class="wish-category">{{ item.product.category }}</p>
            <h3 class="wish-title">{{ item.product.title }}</h3>
            <p class="wish-price">₹{{ item.product.price.toFixed(2) }}</p>
          </div>
        </router-link>
        <div class="wish-actions">
          <button class="btn-primary" style="flex:1"
            @click="moveToCart(item)">
             Add to Cart
          </button>
          <button class="btn-danger" style="padding:10px 14px"
            @click="$store.dispatch('wishlist/removeFromWishlist', item.id)">
            🗑
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters('wishlist', ['wishlistItems'])
  },
  mounted() {
    this.$store.dispatch('wishlist/fetchWishlist')
  },
  methods: {
    async moveToCart(item) {
      await this.$store.dispatch('cart/addToCart', { product_id: item.product.id })
      await this.$store.dispatch('wishlist/removeFromWishlist', item.id)
      this.$router.push('/cart')
    }
  }
}
</script>

<style scoped>
.product-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(220px,1fr)); gap:20px; }
.wish-card { background:white; border-radius:14px; overflow:hidden; box-shadow:0 2px 12px rgba(0,0,0,0.07); display:flex; flex-direction:column; }
.wish-img { width:100%; height:180px; object-fit:cover; }
.wish-info { padding:14px; flex:1; }
.wish-category { font-size:11px; text-transform:uppercase; color:#636e72; font-weight:600; margin-bottom:4px; }
.wish-title { font-size:15px; font-weight:700; margin-bottom:6px; }
.wish-price { font-size:18px; font-weight:800; color:#6c5ce7; }
.wish-actions { display:flex; gap:8px; padding:10px 14px 14px; }
</style>