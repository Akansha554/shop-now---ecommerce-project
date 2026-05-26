import api from '@/api/axios'

export default {
  namespaced: true,
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    loading: false,
    error: null
  }),
  getters: {
    isLoggedIn: s => !!s.user,
    currentUser: s => s.user
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    LOGOUT(state) {
      state.user = null
      localStorage.removeItem('user')
    },
    SET_LOADING(state, val) { state.loading = val },
    SET_ERROR(state, msg) { state.error = msg }
  },
  actions: {
    async sendOtp({ commit }, mobile) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const res = await api.post('/auth/send-otp/', { mobile })
        return res.data
      } catch (e) {
        commit('SET_ERROR', 'Failed to send OTP')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async verifyOtp({ commit }, payload) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const res = await api.post('/auth/verify-otp/', payload)
        commit('SET_USER', res.data.user)
        return res.data
      } catch (e) {
        commit('SET_ERROR', 'Invalid OTP')
        throw e
      } finally {
        commit('SET_LOADING', false)
      }
    },
    logout({ commit }) {
      commit('LOGOUT')
    }
  }
}