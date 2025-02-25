import { createRouter, createWebHistory } from 'vue-router';
import Auth from '../components/Auth.vue';

const routes = [
  { path: '/', component: Auth }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard (if needed in future)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/');  // Redirect unauthorized users to login page
  } else {
    next();
  }
});

export default router;
