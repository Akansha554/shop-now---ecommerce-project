import api from '@/api/axios'

export default {
  namespaced: true,
  state: () => ({
    items: [],
    loading: false
  }),
  getters: {
    cartItems: s => s.items,
    cartCount: s => s.items.reduce((sum, i) => sum + i.quantity, 0),
    cartTotal: s => s.items.reduce((sum, i) => sum + i.product.price * i.quantity, 0)
  },
  mutations: {
    SET_ITEMS(state, items) { state.items = items },
    SET_LOADING(state, val) { state.loading = val }
  },
  actions: {
    async fetchCart({ commit, rootGetters }) {
      const user = rootGetters['auth/currentUser']
      if (!user) return
      commit('SET_LOADING', true)
      try {
        const res = await api.get(`/cart/${user.id}/`)
        commit('SET_ITEMS', res.data)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async addToCart({ dispatch, rootGetters }, { product_id, quantity = 1 }) {
      const user = rootGetters['auth/currentUser']
      if (!user) return false
      await api.post('/cart/add/', { user_id: user.id, product_id, quantity })
      await dispatch('fetchCart')
      return true
    },
    async updateQuantity({ dispatch }, { cart_id, action }) {
      await api.patch(`/cart/update/${cart_id}/`, { action })
      await dispatch('fetchCart')
    },
    async removeFromCart({ dispatch }, cart_id) {
      await api.delete(`/cart/remove/${cart_id}/`)
      await dispatch('fetchCart')
    }
  }
}