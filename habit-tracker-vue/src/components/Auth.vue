<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="title">Habit Tracker</h2>

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
  </div>
</template>

<script>
import API from '../services/api';
import { ref, onMounted } from 'vue';
import confetti from 'canvas-confetti';

export default {
  setup() {
    const isLogin = ref(true);
    const showPassword = ref(false);
    const form = ref({ username: '', password: '' });
    const confettiCanvas = ref(null);

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
        const endpoint = isLogin.value ? '/auth/login' : '/auth/register';
        const response = await API.post(endpoint, form.value);

        localStorage.setItem('token', response.data.access_token);
        alert(`${isLogin.value ? 'Logged in' : 'Registered'} successfully!`);
        if (!isLogin.value) playConfetti();
        window.location.href = "/dashboard";
      } catch (error) {
        alert(error.response.data.detail || 'Something went wrong!');
      }
    };

    const oauthLogin = (provider) => {
      window.location.href = `http://127.0.0.1:8000/auth/${provider}/login`;
    };

    return { isLogin, form, showPassword, toggleAuthMode, togglePasswordVisibility, handleSubmit, oauthLogin, playConfetti, confettiCanvas };
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
  width: 380px;
  text-align: center;
  transition: transform 0.3s ease-in-out;
}

.auth-card:hover {
  transform: translateY(-5px);
}

.title {
  font-size: 26px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border 0.3s;
}

.form-control:focus {
  border-color: #4f46e5;
  outline: none;
}

.password-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 12px;
  cursor: pointer;
  font-size: 18px;
  color: #4f46e5;
}

.btn-custom {
  background: #4f46e5;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
  font-weight: bold;
  transition: background 0.3s ease, transform 0.2s;
}

.btn-custom:hover {
  background: #3b82f6;
  transform: scale(1.05);
}

.oauth-buttons {
  margin-top: 15px;
}

.btn-google,
.btn-github {
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
  font-weight: bold;
  transition: opacity 0.3s ease-in-out;
}

.btn-google {
  background: #db4437;
  color: white;
  margin-bottom: 10px;
}

.btn-github {
  background: #24292e;
  color: white;
}

.btn-google:hover,
.btn-github:hover {
  opacity: 0.85;
}

.toggle-text {
  margin-top: 15px;
  font-size: 14px;
  color: #4f46e5;
  cursor: pointer;
  transition: color 0.3s;
}

.toggle-text:hover {
  color: #3b82f6;
}

.confetti-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
