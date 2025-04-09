// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL, // Use the environment variable
});

export default api;
