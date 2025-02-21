<template>
  <div class="habit-form">
    <h2>Add New Habit</h2>
    <form @submit.prevent="addHabit">
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
      <button type="submit" class="btn btn-primary">Add Habit</button>
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
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>

