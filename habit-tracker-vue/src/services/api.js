import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000", // Adjust this if your backend is hosted elsewhere
  headers: {
    "Content-Type": "application/json",
  },
});

export default API;
