<template>
  <div class="habit-form">
    <h2 class="text-2xl font-semibold flex items-center gap-2">
      ➕ Add New Habit
    </h2>
    
    <form @submit.prevent="addHabit" class="mt-4">
      <div class="form-group">
        <label for="title">Habit Title</label>
        <input v-model="title" type="text" class="form-control" id="title" placeholder="e.g., Morning Run" required />
      </div>
      
      <div class="form-group">
        <label for="description">Description</label>
        <input v-model="description" type="text" class="form-control" id="description" placeholder="Brief description..." />
      </div>
      
      <div class="form-group">
        <label for="reminder">Reminder ⏰ (HH:MM)</label>
        <input v-model="reminder" type="time" class="form-control" id="reminder" />
      </div>
      
      <button type="submit" class="btn-custom">🎯 Add Habit</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: '',
      description: '',
      reminder: '',
    };
  },
  methods: {
    async addHabit() {
      if (!this.title.trim()) {
        alert("Please enter a habit title!");
        return;
      }
      
      await this.$store.dispatch('addHabit', {
        title: this.title,
        description: this.description,
        reminder: this.reminder,
        streak: 0,
      });
      
      this.resetForm();
    },
    resetForm() {
      this.title = '';
      this.description = '';
      this.reminder = '';
    }
  }
};
</script>

<style scoped>
.habit-form {
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.form-group {
  margin-bottom: 12px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

/* Custom Button */
.btn-custom {
  @apply bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-all;
}

.btn-custom:hover {
  transform: scale(1.05);
}
</style>
