import axios from 'axios';

function getCookieValue(key: String) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(key + '=')) {
      return cookie.substring(key.length + 1);
    }
  }
  return null;
}

async function refreshAccessToken() {
  // Call the API to refresh the access token using the refresh token

  const response = await axios.post('/auth/token/refresh/', {
    refresh: getCookieValue('refresh'),
  });
  // Save the new access token in the cookie
  const accessToken = response.data.access;
  // Set the expiration time to be 5 minutes
  const expirationDate = new Date(Date.now() + 300 * 1000);
  document.cookie = `token=${accessToken}`;
  document.cookie = `expiration=${expirationDate.toUTCString()}`;
  return accessToken;
}

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

// Add an interceptor to include the access token in the request headers
instance.interceptors.request.use(async (config) => {
  const accessToken = getCookieValue('token');

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  const expirationString = getCookieValue('expiration');

  if (expirationString) {
    const expirationDate = new Date(decodeURIComponent(expirationString));
    const currentTime = Date.now();
    if (expirationDate.getTime() <= currentTime) {
      // Refresh the access token
      const refreshedToken = await refreshAccessToken();
      config.headers.Authorization = `Bearer ${refreshedToken}`;
    }
  }

  return config;
});

export default instance;
