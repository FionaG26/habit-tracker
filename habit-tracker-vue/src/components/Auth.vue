<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="text-2xl font-semibold">{{ isLogin ? 'Login' : 'Register' }}</h2>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">Username</label>
          <input v-model="form.username" type="text" class="form-control" id="username" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="form-control" id="password" required />
            <span class="toggle-password" @click="togglePasswordVisibility">
              {{ showPassword ? '🙈' : '👁️' }}
            </span>
          </div>
        </div>

        <button type="submit" class="btn-custom">{{ isLogin ? 'Login' : 'Register' }}</button>

        <div class="social-login">
          <p>Or continue with:</p>
          <button class="btn-social google" @click="socialLogin('google')">🔵 Google</button>
          <button class="btn-social github" @click="socialLogin('github')">⚫ GitHub</button>
        </div>
      </form>

      <p class="toggle-text" @click="toggleAuthMode">
        {{ isLogin ? "Don't have an account? Register here!" : "Already have an account? Login here!" }}
      </p>
    </div>
  </div>
</template>

<script>
import API from '../services/api';
import { ref } from 'vue';

export default {
  setup() {
    const isLogin = ref(true);
    const showPassword = ref(false);
    const form = ref({ username: '', password: '' });

    const toggleAuthMode = () => {
      isLogin.value = !isLogin.value;
    };

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
    };

    const handleSubmit = async () => {
      try {
        const endpoint = isLogin.value ? '/login' : '/register';
        const response = await API.post(endpoint, form.value);
        localStorage.setItem('token', response.data.access_token);
        alert(`${isLogin.value ? 'Logged in' : 'Registered'} successfully!`);
      } catch (error) {
        alert(error.response.data.detail || 'Something went wrong!');
      }
    };

    const socialLogin = async (provider) => {
      window.location.href = `http://127.0.0.1:8000/auth/${provider}`;
    };

    return { isLogin, form, showPassword, toggleAuthMode, togglePasswordVisibility, handleSubmit, socialLogin };
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f4f4f4;
}

.auth-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 350px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.password-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  cursor: pointer;
}

.btn-custom {
  background: #28a745;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

.btn-custom:hover {
  background: #218838;
}

.social-login {
  margin-top: 10px;
}

.btn-social {
  display: inline-block;
  padding: 8px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 5px;
}

.btn-social.google {
  background: #db4437;
  color: white;
}

.btn-social.github {
  background: #24292e;
  color: white;
}

.toggle-text {
  margin-top: 10px;
  color: blue;
  cursor: pointer;
}
</style>
