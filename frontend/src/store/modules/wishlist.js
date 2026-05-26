import api from '@/api/axios'

export default {
  namespaced: true,
  state: () => ({
    items: []
  }),
  getters: {
    wishlistItems: s => s.items,
    wishlistCount: s => s.items.length,
    isWishlisted: s => productId =>
      s.items.some(i => i.product.id === productId)
  },
  mutations: {
    SET_ITEMS(state, items) { state.items = items }
  },
  actions: {
    async fetchWishlist({ commit, rootGetters }) {
      const user = rootGetters['auth/currentUser']
      if (!user) return
      try {
        const res = await api.get(`/wishlist/${user.id}/`)
        commit('SET_ITEMS', res.data)
      } catch {}
    },
    async addToWishlist({ dispatch, rootGetters }, product_id) {
      const user = rootGetters['auth/currentUser']
      if (!user) return false
      try {
        await api.post('/wishlist/add/', { user_id: user.id, product_id })
        await dispatch('fetchWishlist')
        return true
      } catch { return false }
    },
    async removeFromWishlist({ dispatch }, wishlist_id) {
      await api.delete(`/wishlist/remove/${wishlist_id}/`)
      await dispatch('fetchWishlist')
    }
  }
}