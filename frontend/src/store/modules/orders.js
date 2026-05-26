import api from '@/api/axios'

export default {
  namespaced: true,
  state: () => ({
    orders: [],
    loading: false
  }),
  getters: {
    allOrders: s => s.orders
  },
  mutations: {
    SET_ORDERS(state, orders) { state.orders = orders },
    SET_LOADING(state, val) { state.loading = val }
  },
  actions: {
    async fetchOrders({ commit, rootGetters }) {
      const user = rootGetters['auth/currentUser']
      if (!user) return
      commit('SET_LOADING', true)
      try {
        const res = await api.get(`/orders/${user.id}/`)
        commit('SET_ORDERS', res.data)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createOrder({ dispatch }, payload) {
      const res = await api.post('/orders/create/', payload)
      await dispatch('fetchOrders')
      return res.data
    },
    async cancelOrder({ dispatch }, order_id) {
      await api.patch(`/orders/cancel/${order_id}/`)
      await dispatch('fetchOrders')
    }
  }
}