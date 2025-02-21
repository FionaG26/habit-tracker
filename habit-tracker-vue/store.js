import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    habits: [],
  },
  mutations: {
    SET_HABITS(state, habits) {
      state.habits = habits;
    },
    ADD_HABIT(state, habit) {
      state.habits.push(habit);
    },
    UPDATE_HABIT(state, updatedHabit) {
      const index = state.habits.findIndex(h => h.id === updatedHabit.id);
      if (index !== -1) {
        state.habits[index] = updatedHabit;
      }
    },
    DELETE_HABIT(state, habitId) {
      state.habits = state.habits.filter(h => h.id !== habitId);
    }
  },
  actions: {
    async fetchHabits({ commit }) {
      try {
        const response = await axios.get("http://127.0.0.1:8000/habits");
        commit("SET_HABITS", response.data);
      } catch (error) {
        console.error("Error fetching habits:", error);
      }
    },
    async addHabit({ commit }, habit) {
      try {
        const response = await axios.post("http://127.0.0.1:8000/habits", habit);
        commit("ADD_HABIT", response.data);
      } catch (error) {
        console.error("Error adding habit:", error);
      }
    },
    async updateHabit({ commit }, habit) {
      try {
        await axios.put(`http://127.0.0.1:8000/habits/${habit.id}`, habit);
        commit("UPDATE_HABIT", habit);
      } catch (error) {
        console.error("Error updating habit:", error);
      }
    },
    async deleteHabit({ commit }, habitId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/habits/${habitId}`);
        commit("DELETE_HABIT", habitId);
      } catch (error) {
        console.error("Error deleting habit:", error);
      }
    }
  },
  getters: {
    allHabits: (state) => state.habits,
  }
});

