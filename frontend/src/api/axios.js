import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000
})

api.interceptors.request.use(config => config, error => Promise.reject(error))

api.interceptors.response.use(
  response => response,
  error => {
    if (!error.response) {
      console.error('Network error — is the Django server running?')
    } else {
      const status = error.response.status
      if (status === 404) console.warn('Resource not found:', error.config.url)
      if (status === 500) console.error('Server error:', error.response.data)
    }
    return Promise.reject(error)
  }
)

export default api