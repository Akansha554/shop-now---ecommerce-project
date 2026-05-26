import api from '@/api/axios'

export default {
  namespaced: true,
  state: () => ({
    all: [],
    mostBought: [],
    loading: false,
    filters: {
      search: '',
      category: '',
      minPrice: 0,
      maxPrice: 2000,
      is_sale: ''
    }
  }),
  getters: {
    filteredProducts: s => s.all,
    categories: s => [...new Set(s.all.map(p => p.category))],
    mostBought: s => s.mostBought
  },
  mutations: {
    SET_PRODUCTS(state, products) { state.all = products },
    SET_MOST_BOUGHT(state, products) { state.mostBought = products },
    SET_LOADING(state, val) { state.loading = val },
    SET_FILTER(state, { key, value }) { state.filters[key] = value }
  },
  actions: {
    async fetchProducts({ commit, state }) {
      commit('SET_LOADING', true)
      try {
        const params = {}
        const f = state.filters
        if (f.search)    params.search    = f.search
        if (f.category)  params.category  = f.category
        if (f.is_sale)   params.is_sale   = f.is_sale
        if (f.minPrice)  params.min_price = f.minPrice
        if (f.maxPrice < 2000) params.max_price = f.maxPrice
        const res = await api.get('/products/', { params })
        commit('SET_PRODUCTS', res.data)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchMostBought({ commit }) {
      try {
        const res = await api.get('/products/most-bought/')
        commit('SET_MOST_BOUGHT', res.data)
      } catch {}
    },
    setFilter({ commit, dispatch }, payload) {
      commit('SET_FILTER', payload)
      dispatch('fetchProducts')
    }
  }
}