<template>
  <div class="auth-container">
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
import { ref, onMounted } from 'vue';
import confetti from 'canvas-confetti';
import gsap from "gsap";

export default {
  setup() {
    const isLogin = ref(true);
    const showPassword = ref(false);
    const form = ref({ username: '', password: '' });
    const confettiCanvas = ref(null);
    const loading = ref(false);

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

    onMounted(() => {
      gsap.from(".header-title", { opacity: 0, y: -20, duration: 1 });
      gsap.from(".title", { opacity: 0, y: -20, duration: 1 });
      gsap.from(".footer", { opacity: 0, y: 20, duration: 1 });
    });

    return { isLogin, form, showPassword, toggleAuthMode, togglePasswordVisibility, handleSubmit, oauthLogin, playConfetti, confettiCanvas, loading };
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: transparent; /* Removed background color */
  padding: 20px;
}

.auth-card {
  background: rgba(255, 255, 255, 0.9); /* Slight transparency for a modern look */
  padding: 50px;
  display: flex;
  justify-content: center;
  border-radius: 15px;
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
  width: 550px; /* Made wider */
  max-width: 90%;
  text-align: center;
  transition: transform 0.3s ease-in-out;
}

.auth-card:hover {
  transform: scale(1.03);
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

.btn-google, .btn-github {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: bold;
  transition: background 0.3s;
}

.btn-google {
  background: #db4437;
  color: white;
}

.btn-google:hover {
  background: #c1351d;
}

.btn-github {
  background: #24292e;
  color: white;
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

/* Footer Styling */
.footer {
  margin-top: auto;
  text-align: center;
  font-size: 14px;
  color: #666;
  padding: 20px;
  width: 100%;
}

.footer-link {
  color: blue;
  text-decoration: none;
  font-weight: bold;
}

.footer-link:hover {
  text-decoration: underline;
}
</style>
