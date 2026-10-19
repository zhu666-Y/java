import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    {
      path: '/login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/home',
      component: () => import('../views/HomeView.vue')
    },
    // 404 兜底：输错地址时回到登录页，而不是白屏
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})

export default router
