<template>
  <div class="app-container">
    <!-- Title -->
    <h1 class="text-4xl font-bold mb-4 animate-bounce">🚀 Welcome to Habit Tracker!</h1>
    
    <!-- Quote Section -->
    <p id="quote" class="italic text-lg text-gray-200 mb-6">{{ quote }}</p>

    <!-- Get Started Button -->
    <button @click="startApp" class="btn-custom">Get Started</button>

    <!-- Main Content -->
    <div class="glass-card mt-6">
      <ProgressBar />
      <HabitForm />
      <HabitList />
    </div>
  </div>
</template>

<script>
import gsap from 'gsap';
import confetti from 'canvas-confetti';
import HabitForm from './components/HabitForm.vue';
import HabitList from './components/HabitList.vue';
import ProgressBar from './components/ProgressBar.vue';

export default {
  components: {
    HabitForm,
    HabitList,
    ProgressBar,
  },
  data() {
    return {
      quotes: [
        "Success is the sum of small efforts, repeated day in and day out. – Robert Collier",
        "Small changes make a big difference!",
        "Keep going, you're doing great! 💪",
        "Your habits shape your future. Make them count!",
        "Consistency is the key to success!",
        "Great things take time. Stay consistent!"
      ],
      quote: "Success is the sum of small efforts, repeated day in and day out. – Robert Collier"
    };
  },
  mounted() {
    // Change quote every 3 seconds
    setInterval(() => {
      this.quote = this.quotes[Math.floor(Math.random() * this.quotes.length)];
    }, 3000);
  },
  methods: {
    startApp() {
      // Scale animation
      gsap.to(".glass-card", { scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 });

      // Confetti explosion
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });

      // Play success sound
      new Audio("https://www.myinstants.com/media/sounds/success-fanfare.mp3").play();
    }
  }
};
</script>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';

/* Background */
body {
  @apply bg-gradient-to-r from-blue-500 to-purple-600 text-white min-h-screen flex items-center justify-center;
}

/* Main Container */
.app-container {
  text-align: center;
  width: 100%;
  max-width: 800px;
}

/* Glassmorphism Card */
.glass-card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  width: 100%;
}

/* Custom Button */
.btn-custom {
  @apply bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded-lg transition-all;
}
</style>
