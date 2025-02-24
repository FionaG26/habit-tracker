<template>
  <div class="habit-form">
    <h2 class="text-2xl font-semibold">Add New Habit</h2>
    <form @submit.prevent="addHabit" class="mt-4">
      <div class="form-group">
        <label for="title">Habit Title</label>
        <input v-model="title" type="text" class="form-control" id="title" required />
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <input v-model="description" type="text" class="form-control" id="description" />
      </div>
      <div class="form-group">
        <label for="reminder">Reminder (HH:MM)</label>
        <input v-model="reminder" type="time" class="form-control" id="reminder" />
      </div>
      <button type="submit" class="btn-custom">Add Habit</button>
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
      await this.$store.dispatch('addHabit', {
        title: this.title,
        description: this.description,
        reminder: this.reminder,
        streak: 0,
      });
      this.title = '';
      this.description = '';
      this.reminder = '';
    },
  },
};
</script>

<style scoped>
.habit-form {
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  backdrop-filter: blur(8px);
}

/* Custom Button */
.btn-custom {
  @apply bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded-lg transition-all;
}
</style>
