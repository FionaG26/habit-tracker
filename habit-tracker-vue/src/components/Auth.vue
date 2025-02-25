<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="header-title">Welcome to Habit Tracker 🎯</h1>
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

        <button type="submit" class="btn-custom" :disabled="loading">
          {{ isLogin ? 'Login' : 'Register' }}
        </button>

        <div v-if="loading" class="loading-spinner"></div>

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

<script setup>
import { ref, reactive } from 'vue';

// Reactive state
const isLogin = ref(true);
const showPassword = ref(false);
const loading = ref(false);
const confettiCanvas = ref(null);
const form = reactive({ username: '', password: '' });

// Toggle login/register mode
const toggleAuthMode = () => {
  isLogin.value = !isLogin.value;
};

// Show/hide password
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// Handle form submission
const handleSubmit = () => {
  loading.value = true;
  setTimeout(() => {
    loading.value = false;
    playConfetti();
  }, 1500);
};

// OAuth login placeholder
const oauthLogin = (provider) => {
  alert(`Logging in with ${provider}...`);
};

// Confetti animation effect
const playConfetti = () => {
  const canvas = confettiCanvas.value;
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const particles = Array.from({ length: 50 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 4 + 1,
    dx: Math.random() * 4 - 2,
    dy: Math.random() * 4 - 2,
    color: `hsl(${Math.random() * 360}, 100%, 50%)`
  }));

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.dx;
      p.y += p.dy;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    });
    requestAnimationFrame(animate);
  };
  animate();
};
// GSAP animations
onMounted(() => {
  if (header.value && footer.value) {
    gsap.from(header.value, { opacity: 0, y: -20, duration: 1 });
    gsap.from(footer.value, { opacity: 0, y: 20, duration: 1, delay: 0.5 });
  }
});
</script>


<style scoped>
/* Base Styling */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background: none;
}
.dark-mode {
  --bg: #1e1e1e;
  --text: #fff;
  --card: #333;
}
.auth-card {
 background: hsla(0, 0%, 0%, 0.3);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 100%;
  max-width: 400px;
}
.header-title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: white;
}
.subtitle {
  font-size: 1rem;
  color: gray;
  margin-bottom: 1rem;
}

/* Form */
.form-group {
  text-align: left;
  margin-bottom: 1rem;
}
.form-control {
  width: 100%;
  padding: 0.8rem;
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

/* Buttons */
.btn-custom {
  width: 100%;
  padding: 0.8rem;
  background: #5c67f2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 1rem;
}
.btn-custom:disabled {
  background: gray;
  cursor: not-allowed;
}
.btn-google, .btn-github {
  width: 100%;
  padding: 0.8rem;
  margin-top: 0.5rem;
  border: none;
  cursor: pointer;
}
.btn-google {
  background: #db4437;
  color: white;
}
.btn-github {
  background: #333;
  color: white;
}

btn-custom.loading {
  position: relative;
}
.btn-custom.loading::after {
  content: "";
  position: absolute;
  right: 10px;
  top: 50%;
  width: 14px;
  height: 14px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  transform: translateY(-50%);
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Toggle Switch */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
  cursor: pointer;
}
.toggle-icon {
  font-size: 1.5rem;
}

/* Footer */
.footer {
  margin-top: 1rem;
  font-size: 0.8rem;
  color: black
}
.footer-link {
  color: #5c67f2;
  text-decoration: none;
}

/* Confetti */
.confetti-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.theme-toggle input {
  display: none;
}
.theme-toggle span {
  display: inline-block;
  width: 40px;
  height: 20px;
  background: #ddd;
  border-radius: 10px;
  position: relative;
  transition: background 0.3s ease;
}
.theme-toggle span::before {
  content: "";
  position: absolute;
  width: 18px;
  height: 18px;
  background: white;
  border-radius: 50%;
  top: 1px;
  left: 2px;
  transition: transform 0.3s ease;
}
input:checked + .toggle-icon {
  background: #5c67f2;
}
input:checked + .toggle-icon::before {
  transform: translateX(20px);
}
@media (max-width: 400px) {
  .auth-card {
    width: 90%;
    padding: 1.5rem;
  }
}
/* Footer */
.footer {
  margin-top: 1rem;
  font-size: 0.8rem;
}
.footer-link {
  color: #5c67f2;
  text-decoration: none;
}
</style>
