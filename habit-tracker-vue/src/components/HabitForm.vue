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
  width: 90%;
  max-width: 600px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  margin: 20px auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

/* Custom Button */
.btn-custom {
  width: 100%;
  background: #38a169;
  color: white;
  font-size: 1.1rem;
  font-weight: bold;
  padding: 12px;
  border-radius: 10px;
  transition: all 0.3s;
}

.btn-custom:hover {
  background: #2f855a;
  transform: scale(1.05);
}
</style>
