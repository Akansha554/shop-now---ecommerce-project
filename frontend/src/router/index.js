import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const routes = [
  { path: '/',        name: 'Home',    component: () => import('@/views/HomeView.vue') },
  { path: '/cart',    name: 'Cart',    component: () => import('@/views/CartView.vue'),   meta: { requiresAuth: true } },
  { path: '/orders',  name: 'Orders',  component: () => import('@/views/OrdersView.vue'), meta: { requiresAuth: true } },
  { path: '/login',   name: 'Login',   component: () => import('@/views/LoginView.vue') },
  { path: '/product/:id', name: 'Product', component: () => import('@/views/ProductDetail.vue') },
  { path: '/wishlist', name: 'Wishlist', component: () => import('@/views/WishlistView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = store.getters['auth/isLoggedIn']
  if (to.meta.requiresAuth && !loggedIn) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router