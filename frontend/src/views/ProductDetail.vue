<template>
  <div class="page-wrapper">
    <div v-if="loading" class="empty-state">Loading...</div>
    <div v-else-if="product" class="detail-layout">

      <!-- Left: Image -->
      <div class="detail-image">
        <img :src="product.image_url" :alt="product.title" />
      </div>

      <!-- Right: Info -->
      <div class="detail-info">
        <p class="card-category">{{ product.category }}</p>
        <h1 style="font-size:28px;font-weight:800;margin-bottom:12px">{{ product.title }}</h1>

        <!-- Rating summary -->
        <div v-if="rating.total_reviews > 0" class="rating-summary">
          <span class="big-stars">{{ starDisplay }}</span>
          <span class="rating-text">{{ rating.avg_rating }} / 5 ({{ rating.total_reviews }} reviews)</span>
        </div>

        <div style="display:flex;gap:10px;align-items:center;margin-bottom:16px">
          <span style="font-size:26px;font-weight:800;color:#6c5ce7">₹{{ product.price.toFixed(2) }}</span>
          <span v-if="product.is_sale" class="badge-sale">ON SALE</span>
          <span v-if="product.sold" class="badge-sold">SOLD OUT</span>
        </div>

        <p style="color:#636e72;line-height:1.7;margin-bottom:24px">{{ product.description }}</p>

        <div style="display:flex;gap:12px;margin-bottom:16px">
          <button class="btn-primary" :disabled="product.sold" @click="addToCart" style="flex:1">
             Add to Cart
          </button>
          <button class="btn-outline" @click="toggleWishlist" style="flex:1">
            {{ isWishlisted ? ' Wishlisted' : ' Wishlist' }}
          </button>
        </div>
        <button class="btn-primary" :disabled="product.sold" @click="buyNow" style="width:100%">
          Buy Now
        </button>
      </div>
    </div>

    <!-- Reviews Section -->
    <div v-if="product" class="reviews-section">
      <h2 class="section-title"> Reviews & Ratings</h2>

      <!-- Write a review -->
      <div v-if="isLoggedIn" class="review-form">
        <h3 style="margin-bottom:16px;font-weight:700">Write a Review</h3>
        <div class="star-picker">
          <span
            v-for="n in 5" :key="n"
            @click="newReview.rating = n"
            :class="['star', { active: n <= newReview.rating }]">★</span>
        </div>
        <textarea
          v-model="newReview.comment"
          placeholder="Share your experience with this product..."
          rows="3"
          style="width:100%;margin-top:12px;padding:12px;border:1px solid #dfe6e9;border-radius:8px;font-size:14px;resize:vertical">
        </textarea>
        <button class="btn-primary" style="margin-top:12px" @click="submitReview">
          Submit Review
        </button>
      </div>
      <div v-else style="margin-bottom:20px">
        <router-link to="/login" style="color:#6c5ce7;font-weight:600">Login to write a review →</router-link>
      </div>

      <!-- Reviews list -->
      <div v-if="reviews.length" class="reviews-list">
        <div v-for="r in reviews" :key="r.id" class="review-card">
          <div class="review-header">
            <span class="reviewer-name"> {{ r.user_name }}</span>
            <span class="review-stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</span>
            <span class="review-date">{{ new Date(r.created_at).toLocaleDateString() }}</span>
          </div>
          <p class="review-comment">{{ r.comment }}</p>
        </div>
      </div>
      <div v-else class="empty-state" style="padding:24px">No reviews yet. Be the first!</div>
    </div>

    <div v-else-if="!loading" class="empty-state">Product not found.</div>
  </div>
</template>

<script>
import api from '@/api/axios'
import { mapGetters } from 'vuex'
export default {
  data() {
    return {
      product: null,
      loading: true,
      reviews: [],
      rating: { avg_rating: 0, total_reviews: 0 },
      newReview: { rating: 5, comment: '' }
    }
  },
  computed: {
    ...mapGetters('auth', ['isLoggedIn', 'currentUser']),
    ...mapGetters('wishlist', ['isWishlisted', 'wishlistItems']),
    wishlisted() { return this.isWishlisted(this.product?.id) },
    wishlistItemId() {
      const item = this.wishlistItems.find(i => i.product.id === this.product?.id)
      return item ? item.id : null
    },
    starDisplay() {
      const r = Math.round(this.rating.avg_rating)
      return '★'.repeat(r) + '☆'.repeat(5 - r)
    }
  },
  async mounted() {
    const id = this.$route.params.id
    try {
      const [prodRes, reviewRes, ratingRes] = await Promise.all([
        api.get(`/products/${id}/`),
        api.get(`/reviews/${id}/`),
        api.get(`/reviews/rating/${id}/`)
      ])
      this.product = prodRes.data
      this.reviews = reviewRes.data
      this.rating  = ratingRes.data
    } finally {
      this.loading = false
    }
    if (this.isLoggedIn) {
      this.$store.dispatch('wishlist/fetchWishlist')
    }
  },
  methods: {
    async addToCart() {
      if (!this.isLoggedIn) { this.$router.push('/login'); return }
      await this.$store.dispatch('cart/addToCart', { product_id: this.product.id })
      this.$store.dispatch('cart/fetchCart')
    },
    async buyNow() {
      if (!this.isLoggedIn) { this.$router.push('/login'); return }
      await this.$store.dispatch('cart/addToCart', { product_id: this.product.id })
      this.$router.push('/cart')
    },
    async toggleWishlist() {
      if (!this.isLoggedIn) { this.$router.push('/login'); return }
      if (this.wishlisted) {
        await this.$store.dispatch('wishlist/removeFromWishlist', this.wishlistItemId)
      } else {
        await this.$store.dispatch('wishlist/addToWishlist', this.product.id)
      }
    },
    async submitReview() {
      if (!this.newReview.comment.trim()) return
      const user = this.currentUser
      await api.post('/reviews/create/', {
        user_id: user.id,
        product_id: this.product.id,
        rating: this.newReview.rating,
        comment: this.newReview.comment
      })
      const [reviewRes, ratingRes] = await Promise.all([
        api.get(`/reviews/${this.product.id}/`),
        api.get(`/reviews/rating/${this.product.id}/`)
      ])
      this.reviews = reviewRes.data
      this.rating  = ratingRes.data
      this.newReview = { rating: 5, comment: '' }
    }
  }
}
</script>

<style scoped>
.detail-layout { display:flex; gap:40px; align-items:flex-start; background:white; padding:32px; border-radius:16px; box-shadow:0 2px 16px rgba(0,0,0,0.07); margin-bottom:32px; }
.detail-image { width:400px; flex-shrink:0; border-radius:12px; overflow:hidden; }
.detail-image img { width:100%; height:360px; object-fit:cover; }
.detail-info { flex:1; }
.card-category { font-size:12px; text-transform:uppercase; color:#636e72; font-weight:600; margin-bottom:8px; }
.rating-summary { display:flex; align-items:center; gap:10px; margin-bottom:14px; }
.big-stars { color:#f39c12; font-size:20px; }
.rating-text { color:#636e72; font-size:14px; }
.reviews-section { background:white; padding:32px; border-radius:16px; box-shadow:0 2px 16px rgba(0,0,0,0.07); }
.review-form { background:#f8f9fa; padding:20px; border-radius:12px; margin-bottom:24px; }
.star-picker { display:flex; gap:6px; }
.star { font-size:28px; color:#dfe6e9; cursor:pointer; transition:color 0.15s; }
.star.active { color:#f39c12; }
.reviews-list { display:flex; flex-direction:column; gap:14px; }
.review-card { background:#f8f9fa; padding:16px; border-radius:10px; border-left:3px solid #6c5ce7; }
.review-header { display:flex; align-items:center; gap:12px; margin-bottom:8px; flex-wrap:wrap; }
.reviewer-name { font-weight:700; font-size:14px; }
.review-stars { color:#f39c12; font-size:14px; }
.review-date { font-size:12px; color:#636e72; margin-left:auto; }
.review-comment { color:#636e72; font-size:14px; line-height:1.6; }
</style>