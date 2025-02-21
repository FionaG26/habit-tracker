import { createStore } from 'vuex';
import axios from 'axios';

export const store = createStore({
  state() {
    return {
      habits: [],
    };
  },
  mutations: {
    setHabits(state, habits) {
      state.habits = habits;
    },
  },
  actions: {
    async fetchHabits({ commit }) {
      const response = await axios.get('http://localhost:8000/habits');
      commit('setHabits', response.data);
    },
  },
});

