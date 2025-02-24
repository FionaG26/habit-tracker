<template>
  <div class="container">
    <h1>Habit Tracker</h1>

    <!-- Quote Section -->
    <p id="quote" class="quote italic text-lg text-gray-200 mb-6">{{ quote }}</p>

    <Auth />
    <HabitForm />
    <HabitList />
    <ProgressBar />

    <button @click="toggleDarkMode" class="mt-4 p-2 rounded-lg bg-gray-700 text-white">
      Toggle Dark Mode
    </button>

    <!-- Footer -->
    <footer class="mt-6 text-center text-gray-300 text-sm">
      Designed with ❤️ by <a href="https://github.com/FionaG26/habit-tracker" class="text-blue-400 hover:text-blue-600 transition">Fiona Githaiga</a>
    </footer>
  </div>
</template>

<script>
import { defineAsyncComponent, watch, ref, onMounted } from 'vue';
import gsap from 'gsap';

const HabitForm = defineAsyncComponent(() => import('./components/HabitForm.vue'));
const HabitList = defineAsyncComponent(() => import('./components/HabitList.vue'));
const ProgressBar = defineAsyncComponent(() => import('./components/ProgressBar.vue'));
const Auth = defineAsyncComponent(() => import('./components/Auth.vue'));

export default {
  components: {
    Auth,
    HabitForm,
    HabitList,
    ProgressBar,
  },
  setup() {
    const darkMode = ref(localStorage.getItem('darkMode') === 'true');
    const quote = ref("Success is the sum of small efforts, repeated day in and day out. – Robert Collier");
    const quotes = [
      "Success is the sum of small efforts, repeated day in and day out. – Robert Collier",
      "Small changes make a big difference!",
      "Keep going, you're doing great! 💪",
      "Your habits shape your future. Make them count!",
      "Consistency is the key to success!",
      "Great things take time. Stay consistent!"
    ];

    const toggleDarkMode = () => {
      darkMode.value = !darkMode.value;
      localStorage.setItem('darkMode', darkMode.value);
      document.documentElement.classList.toggle('dark', darkMode.value);
    };

    watch(darkMode, (newVal) => {
      document.documentElement.classList.toggle('dark', newVal);
    });

    onMounted(() => {
      // Ensure dark mode is applied on page load
      if (darkMode.value) {
        document.documentElement.classList.add('dark');
      }

      // Change quote every 3 seconds
      setInterval(() => {
        quote.value = quotes[Math.floor(Math.random() * quotes.length)];
      }, 3000);

      // Simple animation for the header
      gsap.to("h1", { scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 });

      // Animate footer
      gsap.from("footer", { opacity: 0, y: 20, duration: 1 });
    });

    return { toggleDarkMode, quote };
  }
};
</script>

<style scoped>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import './style.css';

body {
  background: linear-gradient(to right, #4f46e5, #9333ea);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: background 0.5s ease-in-out, color 0.5s ease-in-out;
}

.container {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  
  width: 80vw;
  max-width: 900px;
  min-height: 60vh;
  max-height: 90vh;
  
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Dark mode styles */
.dark .container {
  background: rgba(0, 0, 0, 0.8);
  color: white;
}

/* Prevent quote section resizing */
.quote {
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  max-width: 500px;
  margin: auto;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

/* Footer styles */
footer a:hover {
  color: #ffcc00;
  transform: scale(1.1);
  transition: 0.3s;
}
</style>
