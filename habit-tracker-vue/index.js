import { createRouter, createWebHistory } from 'vue-router';
import Auth from '../components/Auth.vue';
import Dashboard from '../components/Dashboard.vue';

const routes = [
  { path: '/', component: Auth },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard: Redirect unauthorized users
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router;
