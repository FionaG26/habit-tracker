<template>
  <div class="container">
    <h1>Habit Tracker</h1>
    <ProgressBar />
    <HabitForm />
    <HabitList />
  </div>
</template>

<script>
import HabitForm from './components/HabitForm.vue';
import HabitList from './components/HabitList.vue';
import ProgressBar from './components/ProgressBar.vue';

export default {
  components: {
    HabitForm,
    HabitList,
    ProgressBar,
  },
};
</script>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import './style.css';

.container {
  max-width: 700px;
  margin: auto;
  text-align: center;
}
</style>

