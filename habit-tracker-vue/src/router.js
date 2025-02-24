import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "./components/Dashboard.vue";
import Auth from "./components/Auth.vue";

const routes = [
  { path: "/", redirect: "/login" },  // Default to login
  { path: "/login", component: Auth },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } }, // Protected
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard to check authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("token") !== null;
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");  // Redirect to login if not authenticated
  } else {
    next();
  }
});

export default router;
