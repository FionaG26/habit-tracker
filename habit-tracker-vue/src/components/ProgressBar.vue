<template>
  <div class="progress-container">
    <p class="mb-2">Habits Completed: {{ completedHabits }}/{{ totalHabits }}</p>
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
    </div>
    <div v-if="progressPercentage === 100" class="celebration">
      🎉 Great job! All habits completed! 🎉
    </div>
    <div v-if="milestoneAchieved" class="milestone">
      🏆 Achievement Unlocked: {{ milestoneMessage }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      milestoneMessage: '',
    };
  },
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
    milestoneAchieved() {
      if (this.completedHabits === 5) {
        this.milestoneMessage = '5 Habits Completed!';
        return true;
      } else if (this.completedHabits === 10) {
        this.milestoneMessage = '10-Day Streak!';
        return true;
      }
      return false;
    },
  },
};
</script>

<style scoped>
.progress-container {
  margin: 20px 0;
  text-align: center;
  position: relative;
}

.progress-bar-container {
  width: 100%;
  height: 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #ff6b6b, #feca57, #1dd1a1);
  transition: width 0.5s ease-in-out;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.8; }
  100% { opacity: 1; }
}

.celebration {
  font-size: 18px;
  color: #ff9f43;
  font-weight: bold;
  margin-top: 10px;
  animation: bounce 1s infinite;
}

.milestone {
  font-size: 16px;
  color: #1dd1a1;
  font-weight: bold;
  margin-top: 10px;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
