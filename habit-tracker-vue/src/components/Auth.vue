<template>
  <div :class="{'dark-mode': darkMode}" class="auth-container">
    <div class="auth-card">
      <h1 ref="headerTitle" class="header-title">Welcome to Habit Tracker 🎯</h1>
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
    <footer ref="footer" class="footer">
      Designed with ❤️ by 
      <a href="https://github.com/FionaG26/habit-tracker" class="footer-link">Fiona Githaiga</a>
    </footer>
  </div>
</template>

<script>
import API from '../services/api';
import { ref, watch, onMounted, nextTick } from 'vue';
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
    const headerTitle = ref(null);
    const footer = ref(null);

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
        alert(error.response?.data?.detail || 'Something went wrong!');
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

    onMounted(async () => {
      document.body.classList.toggle('dark-mode', darkMode.value);
      
      await nextTick(); // Ensures DOM elements are fully loaded before GSAP
      
      if (headerTitle.value) {
        gsap.from(headerTitle.value, { opacity: 0, y: -20, duration: 1 });
      }
      if (footer.value) {
        gsap.from(footer.value, { opacity: 0, y: 20, duration: 1 });
      }
    });

    return { isLogin, form, showPassword, toggleAuthMode, togglePasswordVisibility, handleSubmit, oauthLogin, playConfetti, confettiCanvas, loading, darkMode, toggleTheme, headerTitle, footer };
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed; /* Ensures it takes the full screen */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: none; /* Removes any background */
  overflow: hidden;
  padding: 20px; /* Adds space if needed */
}

.confetti-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none; /* Prevents blocking interactions */
  background: transparent; /* Ensures no background */
}

.auth-card {
  background: rgba(255, 255, 255, 0.95); /* Slight transparency to soften */
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
  width: 380px;
  text-align: center;
  transition: transform 0.3s ease-in-out;
}

.auth-card:hover {
  transform: scale(1.03);
}

.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 18px;
}

.theme-toggle input {
  display: none;
}

.toggle-icon {
  font-size: 24px;
  transition: transform 0.3s ease-in-out;
}


.dark-mode .toggle-icon {
  transform: rotate(180deg);
}

.header-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #ff758c;
  box-shadow: 0 0 8px rgba(255, 117, 140, 0.6);
  outline: none;
}

.password-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 15px;
  cursor: pointer;
  font-size: 20px;
}

.btn-custom {
  background: #ff758c;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
  font-weight: bold;
  transition: background 0.3s ease;
}

.btn-custom:hover {
  background: #e83e8c;
}

.oauth-buttons {
  margin-top: 20px;
}

.btn-google {
  background: #db4437;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  margin-bottom: 10px;
  transition: background 0.3s;
}

.btn-google:hover {
  background: #c1351d;
}

.btn-github {
  background: #24292e;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  transition: background 0.3s;
}

.btn-github:hover {
  background: #1b1f23;
}

.toggle-text {
  margin-top: 15px;
  color: blue;
  cursor: pointer;
  font-weight: bold;
}

.toggle-text:hover {
  text-decoration: underline;
}

.theme-toggle {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
  cursor: pointer;
}

.toggle-icon {
  font-size: 20px;
  margin-left: 10px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #ff758c;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 10px auto;
}

  .footer {
  position: absolute;
  bottom: 20px;
  font-size: 14px;
  color: black;
}

.footer-link {
  color: #4A90E2;
  text-decoration: none;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
