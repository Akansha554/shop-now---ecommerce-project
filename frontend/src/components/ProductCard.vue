<template>
  <div class="product-card">
    <router-link :to="`/product/${product.id}`">
      <div class="card-image">
        <img :src="product.image_url" :alt="product.title" />
        <div class="card-badges">
          <span v-if="product.is_sale" class="badge-sale">SALE</span>
          <span v-if="product.sold" class="badge-sold">SOLD</span>
        </div>
        <button class="wish-btn" @click.prevent="toggleWishlist">
          {{ isWishlisted ? '❤️' : '🤍' }}
        </button>
      </div>
      <div class="card-body">
        <p class="card-category">{{ product.category }}</p>
        <h3 class="card-title">{{ product.title }}</h3>
        <div class="card-rating" v-if="product.avg_rating">
          <span class="stars">{{ starDisplay }}</span>
          <span class="rating-count">({{ product.total_reviews }})</span>
        </div>
        <p class="card-price">₹{{ product.price.toFixed(2) }}</p>
      </div>
    </router-link>
    <div class="card-footer">
      <button
        class="btn-primary"
        style="width:100%"
        :disabled="product.sold"
        @click="$emit('add-to-cart', product)">
        {{ product.sold ? 'Out of Stock' : 'Add to Cart' }}
      </button>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  props: { product: { type: Object, required: true } },
  emits: ['add-to-cart'],
  computed: {
    ...mapGetters('wishlist', ['isWishlisted', 'wishlistItems']),
    wishlisted() { return this.isWishlisted(this.product.id) },
    wishlistId() {
      const item = this.wishlistItems.find(i => i.product.id === this.product.id)
      return item ? item.id : null
    },
    starDisplay() {
      const r = Math.round(this.product.avg_rating || 0)
      return '★'.repeat(r) + '☆'.repeat(5 - r)
    }
  },
  methods: {
    ...mapActions('wishlist', ['addToWishlist', 'removeFromWishlist']),
    async toggleWishlist() {
      if (!this.$store.getters['auth/isLoggedIn']) {
        this.$router.push('/login')
        return
      }
      if (this.wishlisted) {
        await this.removeFromWishlist(this.wishlistId)
      } else {
        await this.addToWishlist(this.product.id)
      }
    }
  }
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}
.product-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
.card-image { position: relative; height: 180px; background: #f0f0f0; }
.card-image img { width: 100%; height: 100%; object-fit: cover; }
.card-badges { position: absolute; top: 10px; left: 10px; display: flex; gap: 6px; }
.wish-btn {
  position: absolute; top: 8px; right: 8px;
  background: white; border: none;
  border-radius: 50%; width: 32px; height: 32px;
  font-size: 16px; cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  display: flex; align-items: center; justify-content: center;
}
.card-body { padding: 14px 14px 8px; flex: 1; }
.card-category { font-size: 11px; text-transform: uppercase; color: #636e72; font-weight: 600; margin-bottom: 4px; }
.card-title { font-size: 15px; font-weight: 700; margin-bottom: 6px; color: #2d3436; line-height: 1.3; }
.card-rating { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; }
.stars { color: #f39c12; font-size: 13px; }
.rating-count { font-size: 12px; color: #636e72; }
.card-price { font-size: 18px; font-weight: 800; color: #6c5ce7; }
.card-footer { padding: 10px 14px 14px; }
</style>