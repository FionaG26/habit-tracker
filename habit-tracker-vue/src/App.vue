<template> 
  <div class="container">
    <h1>Habit Tracker</h1>
    <!-- Quote Section -->
    <p id="quote" class="italic text-lg text-gray-200 mb-6">{{ quote }}</p>
    
    <ProgressBar />
    <HabitForm />
    <HabitList />
    <button @click="toggleDarkMode" class="mt-4 p-2 rounded-lg bg-gray-700 text-white">Toggle Dark Mode</button>
  </div>
</template>

<script>
import { defineAsyncComponent, watch, ref } from 'vue';
import gsap from 'gsap';

const HabitForm = defineAsyncComponent(() => import('./components/HabitForm.vue'));
const HabitList = defineAsyncComponent(() => import('./components/HabitList.vue'));
const ProgressBar = defineAsyncComponent(() => import('./components/ProgressBar.vue'));

export default {
  components: {
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
      document.body.classList.toggle('dark', darkMode.value);
    };
    
    watch(() => darkMode.value, (newVal) => {
      document.body.classList.toggle('dark', newVal);
    });
    
    setInterval(() => {
      quote.value = quotes[Math.floor(Math.random() * quotes.length)];
    }, 3000);
    
    return { toggleDarkMode, quote };
  },
  mounted() {
    gsap.to("#start-btn", { scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 });
  }
};
</script>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import './style.css';

body {
  background: linear-gradient(to right, #4f46e5, #9333ea);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: background 0.3s ease;
}

.container {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.dark {
  background: #1a202c;
  color: white;
}
</style>
