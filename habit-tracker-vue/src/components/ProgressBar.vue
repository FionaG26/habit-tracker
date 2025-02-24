<template>
  <div class="progress-container">
    <p class="mb-2">Habits Completed: {{ completedHabits }}/{{ totalHabits }}</p>
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    completedHabits() {
      return this.$store.state.habits.filter(h => h.completed).length;
    },
    totalHabits() {
      return this.$store.state.habits.length;
    },
    progressPercentage() {
      return (this.completedHabits / this.totalHabits) * 100 || 0;
    },
  },
};
</script>

<style scoped>
.progress-container {
  margin: 20px 0;
  text-align: center;
}

/* Progress Bar */
.progress-bar-container {
  width: 100%;
  height: 10px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #4ade80;
  transition: width 0.5s ease-in-out;
}
</style>
