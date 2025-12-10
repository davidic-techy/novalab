import axios from "axios";

// Create a standalone Axios instance
const api = axios.create({
  baseURL: "", // Vite proxy handles the localhost:8000 part
  headers: {
    "Content-Type": "application/json",
  },
});

// --- INTERCEPTOR: Attach Token to Every Request ---
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// --- INTERCEPTOR: Handle 401 (Unauthorized) Errors ---
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried refreshing yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");
        // Call Django's refresh endpoint
        const response = await axios.post("/api/auth/token/refresh/", {
          refresh: refreshToken,
        });

        const { access } = response.data;

        // Save new token
        localStorage.setItem("access_token", access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails, user is truly logged out
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
