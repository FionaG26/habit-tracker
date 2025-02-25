<template>
  <div :class="{'dark-mode': darkMode}" class="auth-container">
    <div class="auth-card">
      <h1 class="header-title">Welcome to Habit Tracker 🎯</h1>
      <h2 class="title">Habit Tracker 🎯</h2>
      <p class="subtitle">Track your progress & build better habits!</p>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">Username</label>
          <input v-model="form.username" type="text" class="form-control" id="username" required placeholder="Enter your username" />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="form-control" id="password" required placeholder="Create a strong password" />
            <span class="toggle-password" @click="togglePasswordVisibility">
              {{ showPassword ? '🙈' : '👁️' }}
            </span>
          </div>
        </div>

        <button type="submit" class="btn-custom" @click="playConfetti">
          {{ isLogin ? 'Login' : 'Register' }}
        </button>

        <div class="loading-spinner" v-if="loading"></div>

        <div class="oauth-buttons">
          <button @click="oauthLogin('google')" class="btn-google">Login with Google</button>
          <button @click="oauthLogin('github')" class="btn-github">Login with GitHub</button>
        </div>
      </form>

      <p class="toggle-text" @click="toggleAuthMode">
        {{ isLogin ? "Don't have an account? Register here!" : "Already have an account? Login here!" }}
      </p>
      
      <label class="theme-toggle">
        <input type="checkbox" v-model="darkMode" @change="toggleTheme" />
        <span class="toggle-icon">🌞 / 🌙</span>
      </label>
    </div>
    <canvas ref="confettiCanvas" class="confetti-canvas"></canvas>

    <!-- Footer -->
    <footer class="footer">
      Designed with ❤️ by 
      <a href="https://github.com/FionaG26/habit-tracker" class="footer-link">Fiona Githaiga</a>
    </footer>
  </div>
</template>

<script>
import API from '../services/api';
import { ref, watch, onMounted } from 'vue';
import confetti from 'canvas-confetti';
import gsap from "gsap";

export default {
  setup() {
    const isLogin = ref(true);
    const showPassword = ref(false);
    const form = ref({ username: '', password: '' });
    const confettiCanvas = ref(null);
    const loading = ref(false);
    const darkMode = ref(localStorage.getItem('darkMode') === 'true');

    const toggleAuthMode = () => {
      isLogin.value = !isLogin.value;
    };

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
    };

    const playConfetti = () => {
      if (!isLogin.value) {
        confetti({
          particleCount: 150,
          spread: 80,
          origin: { y: 0.6 }
        });
      }
    };

    const handleSubmit = async () => {
      try {
        loading.value = true;
        const endpoint = isLogin.value ? '/auth/login' : '/auth/register';
        const response = await API.post(endpoint, form.value);

        localStorage.setItem('token', response.data.access_token);
        setTimeout(() => {
          alert(`${isLogin.value ? '🎉 Logged in' : '🎊 Registered'} successfully!`);
          playConfetti();
          window.location.href = "/dashboard";
        }, 500);
      } catch (error) {
        alert(error.response.data.detail || 'Something went wrong!');
      } finally {
        loading.value = false;
      }
    };

    const oauthLogin = (provider) => {
      window.location.href = `http://127.0.0.1:8000/auth/${provider}/login`;
    };

    const toggleTheme = () => {
      darkMode.value = !darkMode.value;
      document.body.classList.toggle('dark-mode', darkMode.value);
      localStorage.setItem('darkMode', darkMode.value);
    };

    onMounted(() => {
      document.body.classList.toggle('dark-mode', darkMode.value);
      
      if (document.querySelector(".header-title")) {
        gsap.from(".header-title", { opacity: 0, y: -20, duration: 1 });
      }
      
      if (document.querySelector(".title")) {
        gsap.from(".title", { opacity: 0, y: -20, duration: 1 });
      }

      if (document.querySelector(".footer")) {
        gsap.from(".footer", { opacity: 0, y: 20, duration: 1 });
      }
    });

    return { isLogin, form, showPassword, toggleAuthMode, togglePasswordVisibility, handleSubmit, oauthLogin, playConfetti, confettiCanvas, loading, darkMode, toggleTheme };
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: var(--background-color, #ffffff);
  padding: 20px;
}

.dark-mode {
  --background-color: #121212;
  color: white;
}

.auth-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
  width: 420px;
  text-align: center;
}

.footer {
  position: absolute;
  bottom: 20px;
  font-size: 14px;
  color: gray;
}

.footer-link {
  color: #4A90E2;
  text-decoration: none;
}
</style>
