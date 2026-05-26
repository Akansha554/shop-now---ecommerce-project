import ProductCard from '@/components/ProductCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  components: { ProductCard, LoadingSpinner },
<template>
  <div class="page-wrapper">

    <!-- Most Bought Section -->
    <section v-if="mostBought.length" style="margin-bottom:40px">
      <h2 class="section-title"> Most Bought Products</h2>
      <div class="product-grid">
        <ProductCard
          v-for="p in mostBought" :key="'mb-'+p.id"
          :product="p" @add-to-cart="addToCart(p)" />
      </div>
    </section>

    <div class="shop-layout">

      <!-- Sidebar filters -->
      <aside class="sidebar">
        <h3 style="margin-bottom:16px;font-weight:700">Filters</h3>

        <div class="filter-section">
          <label>Search</label>
          <input v-model="searchInput" type="text" placeholder="Search products..." />
        </div>

        <div class="filter-section">
          <label>Category</label>
          <select v-model="selectedCategory" @change="applyFilter('category', selectedCategory)">
            <option value="">All Categories</option>
            <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>

        <div class="filter-section">
          <label>Price Range: ₹{{ priceRange[0] }} – ₹{{ priceRange[1] }}</label>
          <input type="range" v-model="priceRange[1]" min="0" max="2000" step="50"
            @input="applyFilter('maxPrice', priceRange[1])" style="width:100%;margin-top:8px" />
        </div>

        <div class="filter-section">
          <label>On Sale</label>
          <select v-model="saleFilter" @change="applyFilter('is_sale', saleFilter)">
            <option value="">All Products</option>
            <option value="true">On Sale</option>
            <option value="false">Regular Price</option>
          </select>
        </div>

        <button class="btn-outline" style="width:100%;margin-top:8px" @click="clearFilters">
          Clear Filters
        </button>
      </aside>

      <!-- Product grid -->
      <main class="product-area">
        <h2 class="section-title">All Products</h2>

        <LoadingSpinner v-if="loading" message="Fetching products..." />
        <div v-else-if="!products.length" class="empty-state">No products found.</div>
        <div v-else class="product-grid">
          <ProductCard
            v-for="p in products" :key="p.id"
            :product="p" @add-to-cart="addToCart(p)" />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex'
import ProductCard from '@/components/ProductCard.vue'

export default {
  components: { ProductCard },
  data() {
    return {
      searchInput: '',
      selectedCategory: '',
      saleFilter: '',
      priceRange: [0, 2000],
      debounceTimer: null
    }
  },
  computed: {
    ...mapGetters('products', ['filteredProducts', 'categories', 'mostBought']),
    ...mapState('products', ['loading']),
    products() { return this.filteredProducts }
  },
  watch: {
    searchInput(val) {
      clearTimeout(this.debounceTimer)
      this.debounceTimer = setTimeout(() => {
        this.applyFilter('search', val)
      }, 400)
    }
  },
  mounted() {
    this.$store.dispatch('products/fetchProducts')
    this.$store.dispatch('products/fetchMostBought')
    if (this.$store.getters['auth/isLoggedIn']) {
      this.$store.dispatch('cart/fetchCart')
    }
  },
  methods: {
    ...mapActions('products', ['setFilter']),
    applyFilter(key, value) {
      this.setFilter({ key, value })
    },
    clearFilters() {
      this.searchInput = ''
      this.selectedCategory = ''
      this.saleFilter = ''
      this.priceRange = [0, 2000]
      this.$store.commit('products/SET_FILTER', { key: 'search', value: '' })
      this.$store.commit('products/SET_FILTER', { key: 'category', value: '' })
      this.$store.commit('products/SET_FILTER', { key: 'is_sale', value: '' })
      this.$store.commit('products/SET_FILTER', { key: 'maxPrice', value: 2000 })
      this.$store.dispatch('products/fetchProducts')
    },
    async addToCart(product) {
      if (!this.$store.getters['auth/isLoggedIn']) {
        this.$router.push('/login')
        return
      }
      const ok = await this.$store.dispatch('cart/addToCart', { product_id: product.id })
      if (ok) this.$store.dispatch('cart/fetchCart')
    }
  }
}
</script>

<style scoped>
.shop-layout { display: flex; gap: 24px; align-items: flex-start; }
.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  position: sticky;
  top: 80px;
}
.product-area { flex: 1; }
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.filter-section { margin-bottom: 16px; }
.filter-section label { display: block; font-size: 12px; font-weight: 600; color: #636e72; margin-bottom: 6px; }
</style>