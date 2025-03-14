<template>
  <div class="list-container">
    <h2 class="text-2xl font-bold mb-4">📋 Your Habits</h2>

    <!-- Progress Bar -->
    <div v-if="habits.length > 0" class="progress-container">
      <span class="block text-gray-700 font-semibold">Today's Progress: {{ completedCount }} / {{ habits.length }}</span>
      <div class="progress-bar">
        <div :style="{ width: progressPercentage }" class="progress-fill"></div>
      </div>
    </div>

    <!-- Filters & Export -->
    <div class="filters flex justify-between items-center mt-4">
      <label class="text-gray-700 font-semibold">Sort by: 
        <select v-model="sortBy" class="ml-2 p-2 border rounded">
          <option value="title">Title</option>
          <option value="date">Date Added</option>
          <option value="streak">Streak</option>
        </select>
      </label>
      <button @click="exportCSV" class="bg-blue-600 hover:bg-blue-800 text-white py-2 px-4 rounded transition-all">📂 Export to CSV</button>
    </div>

    <!-- Habit List -->
    <ul class="habit-list mt-4">
      <li v-for="habit in filteredHabits" :key="habit.id" class="habit-item">
        <div class="habit-info">
          <span class="habit-title font-semibold text-lg">{{ habit.title }}</span>
          <span class="habit-description text-gray-600">{{ habit.description }}</span>
          <span class="habit-streak text-green-600 font-bold">🔥 Streak: {{ habit.streak }} days</span>
        </div>
        <div class="habit-actions flex space-x-2">
          <button class="complete-btn" @click="toggleComplete(habit)">✅</button>
          <button class="delete-btn" @click="confirmDelete(habit.id)">🗑️</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      sortBy: "title",
    };
  },
  computed: {
    ...mapState(["habits"]),
    filteredHabits() {
      if (!this.habits) return [];

      let sorted = [...this.habits];
      if (this.sortBy === "title") {
        sorted.sort((a, b) => a.title.localeCompare(b.title));
      } else if (this.sortBy === "date") {
        sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      } else if (this.sortBy === "streak") {
        sorted.sort((a, b) => b.streak - a.streak);
      }
      return sorted;
    },
    completedCount() {
      return this.habits ? this.habits.filter(habit => habit.completed_today).length : 0;
    },
    progressPercentage() {
      return this.habits.length > 0 
        ? `${(this.completedCount / this.habits.length) * 100}%` 
        : "0%";
    }
  },
  methods: {
    ...mapActions(["updateHabit", "deleteHabit"]),
    toggleComplete(habit) {
      habit.completed_today = !habit.completed_today;
      if (habit.completed_today) {
        habit.streak += 1;
        let today = new Date().toISOString().split('T')[0]; 
        if (!habit.completed_dates.includes(today)) habit.completed_dates.push(today);
      } else {
        habit.streak = 0;
      }
      this.updateHabit(habit);
    },
    confirmDelete(habitId) {
      if (confirm("Are you sure you want to delete this habit?")) {
        this.deleteHabit(habitId);
      }
    },
    exportCSV() {
      let csvContent = "data:text/csv;charset=utf-8,";
      csvContent += "Title,Streak,Completed Dates\n";
      this.habits.forEach(habit => {
        csvContent += `"${habit.title}",${habit.streak},"${habit.completed_dates.join("," )}"\n`;
      });

      let encodedUri = encodeURI(csvContent);
      let link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "habit_tracker.csv");
      document.body.appendChild(link);
      link.click();
    }
  },
  mounted() {
    this.$store.dispatch("fetchHabits");
  }
};
</script>

<style scoped>
.list-container {
  padding: 20px;
  max-width: 600px;
  margin: auto;
}
.habit-list {
  list-style: none;
  padding: 0;
}
.habit-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 10px 0;
  padding: 12px;
  border-radius: 8px;
  transition: transform 0.2s;
}
.habit-item:hover {
  transform: scale(1.02);
}
.habit-actions button {
  margin-left: 5px;
}
.progress-container {
  margin-bottom: 20px;
}
.progress-bar {
  width: 100%;
  height: 10px;
  background: #ddd;
  border-radius: 5px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: #4caf50;
  transition: width 0.5s ease-in-out;
}
.complete-btn {
  background: #4caf50;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}
.complete-btn:hover {
  background: #388e3c;
}
.delete-btn {
  background: #f44336;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}
.delete-btn:hover {
  background: #d32f2f;
}
</style>
