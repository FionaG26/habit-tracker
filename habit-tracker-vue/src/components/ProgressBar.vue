<template>
  <div class="progress-container">
    <p>Habits Completed: {{ completedHabits }}/{{ totalHabits }}</p>
    <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
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
  height: 20px;
  background: #ddd;
  border-radius: 5px;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background: #28a745;
}
</style>

