<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="title">{{ isLogin ? 'Login' : 'Register' }}</h2>

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

        <button type="submit" class="btn-custom">
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
        const endpoint = isLogin.value ? '/auth/login' : '/auth/register';
        const response = await API.post(endpoint, form.value);

        // Save token in localStorage
        localStorage.setItem('token', response.data.access_token);

        alert(`${isLogin.value ? 'Logged in' : 'Registered'} successfully!`);
        window.location.href = "/dashboard"; // Redirect to dashboard
      } catch (error) {
        alert(error.response.data.detail || 'Something went wrong!');
      }
    };

    const oauthLogin = (provider) => {
      window.location.href = `http://127.0.0.1:8000/auth/${provider}/login`;
    };

    return { isLogin, form, showPassword, toggleAuthMode, togglePasswordVisibility, handleSubmit, oauthLogin };
  }
};
</script>

<style scoped>
/* Center container */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to bottom, #4f46e5, #3b82f6);
  padding: 20px;
}

/* Card container */
.auth-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.15);
  width: 380px;
  text-align: center;
  transition: transform 0.3s ease-in-out;
}

/* Card hover effect */
.auth-card:hover {
  transform: translateY(-5px);
}

/* Title */
.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

/* Form group */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}

/* Form input fields */
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

/* Password wrapper */
.password-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

/* Password toggle icon */
.toggle-password {
  position: absolute;
  right: 12px;
  cursor: pointer;
  font-size: 18px;
  color: #4f46e5;
}

/* Custom submit button */
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
  transition: background 0.3s ease;
}

.btn-custom:hover {
  background: #3b82f6;
}

/* OAuth Buttons */
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

/* Toggle between login & register */
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
</style>
