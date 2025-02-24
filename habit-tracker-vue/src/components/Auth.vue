<template>
  <div class="auth-container">
    <div class="auth-card">
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
        🌞 / 🌙
      </label>
    </div>
    <canvas ref="confettiCanvas" class="confetti-canvas"></canvas>
  </div>
</template>

<script>
import API from '../services/api';
import { ref, watch, onMounted } from 'vue';
import confetti from 'canvas-confetti';

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
    });

    return { isLogin, form, showPassword, toggleAuthMode, togglePasswordVisibility, handleSubmit, oauthLogin, playConfetti, confettiCanvas, loading, darkMode, toggleTheme };
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to bottom, #4f46e5, #3b82f6);
  padding: 20px;
  position: relative;
}

.auth-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.15);
  width: 400px;
  text-align: center;
  transition: transform 0.3s ease-in-out;
}

.title {
  font-size: 26px;
  font-weight: bold;
  color: #333;
}

.subtitle {
  font-size: 14px;
  color: #555;
  margin-bottom: 15px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4f46e5;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  animation: spin 1s linear infinite;
  margin: 10px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.theme-toggle {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
  cursor: pointer;
}

.dark-mode {
  background: #121212;
  color: white;
}
</style>
