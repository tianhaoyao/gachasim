import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

// Add an interceptor to include the access token in the request headers
instance.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('accessToken');
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

export default instance;
