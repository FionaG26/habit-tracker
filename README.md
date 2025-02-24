# Vue + FastAPI Habit Tracker

## Overview
This project integrates **Vue.js** for the frontend and **FastAPI** for the backend to create a **habit tracker application**. The application allows users to add, manage, and track their daily habits.

## Features
### Backend (FastAPI)
- **User Authentication** (JWT-based login/signup)
- **Habit Management** (Create, Read, Update, Delete habits)
- **Reminder System** (Set time-based reminders)
- **Progress Tracking** (Track habit streaks)
- **Automatic API Documentation** via [Swagger UI](http://127.0.0.1:8000/docs)

### Frontend (Vue.js)
- **Responsive UI** with Tailwind CSS
- **Dark Mode Toggle** 🌙
- **Live Habit Tracking**
- **Real-time Progress Bar**
- **Animated UI with GSAP**

---
## Installation

### 1. Backend Setup (FastAPI)
```sh
$ mkdir backend && cd backend
$ python -m venv venv
$ source venv/bin/activate  # For Linux/Mac
$ venv\Scripts\activate  # For Windows
$ pip install fastapi uvicorn SQLAlchemy pydantic bcrypt python-jose
```

#### Create `main.py`
```python
from fastapi import FastAPI
from routers import habits, users

app = FastAPI()

app.include_router(habits.router)
app.include_router(users.router)
```

Run the server:
```sh
$ uvicorn main:app --reload
```
Visit the API docs at: [Swagger UI](http://127.0.0.1:8000/docs)

---
### 2. Frontend Setup (Vue.js)
```sh
$ mkdir frontend && cd frontend
$ npm create vite@latest habit-tracker --template vue
$ cd habit-tracker
$ npm install
$ npm run dev
```

---
## API Endpoints

### Authentication
- **`POST /register`** – Create a new user
- **`POST /login`** – Get access token

### Habits
- **`GET /habits`** – Fetch all habits
- **`POST /habits`** – Add a new habit
- **`PUT /habits/{id}`** – Update a habit
- **`DELETE /habits/{id}`** – Remove a habit

### Reminders
- **`GET /reminders`** – Fetch reminders
- **`POST /reminders`** – Create a reminder

---
## Frontend Implementation
### Vue Components
- **`HabitForm.vue`** – Add new habits
- **`HabitList.vue`** – Display habits
- **`ProgressBar.vue`** – Track progress
- **`DarkModeToggle.vue`** – Switch themes

### API Integration
**`services/api.js`**
```javascript
import axios from 'axios';
const API = axios.create({ baseURL: 'http://127.0.0.1:8000' });
export default API;
```

Example Vue component fetching habits:
```vue
<template>
  <div>
    <h1>My Habits</h1>
    <ul>
      <li v-for="habit in habits" :key="habit.id">{{ habit.title }}</li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import API from '../services/api';
export default {
  setup() {
    const habits = ref([]);
    onMounted(async () => { habits.value = (await API.get('/habits')).data; });
    return { habits };
  },
};
</script>
```

---
## Conclusion
This **Vue + FastAPI Habit Tracker** is a scalable, full-stack application that allows users to build productive habits efficiently. 🚀
