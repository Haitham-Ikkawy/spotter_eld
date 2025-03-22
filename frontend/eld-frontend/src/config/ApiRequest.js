import axios from "axios";
import { toast } from "react-toastify"; // Import toast notifications

const BASE_URL = "http://127.0.0.1:8000/api/";
// const BASE_URL = "https://haithamakk.pythonanywhere.com/api/";

const ApiRequest = axios.create({
    baseURL: BASE_URL,
    timeout: 60000,
});

// Function to get token from local storage
const getAccessToken = () => localStorage.getItem("access_token");
const getRefreshToken = () => localStorage.getItem("refresh_token");

// Function to refresh the token
const refreshToken = async () => {
    try {
        const refresh = getRefreshToken();
        if (!refresh) throw new Error("No refresh token available");

        const response = await axios.post(`${BASE_URL}token/refresh/`, {
            refresh: refresh,
        });

        const newAccessToken = response.data.access;
        localStorage.setItem("access_token", newAccessToken);
        return newAccessToken;
    } catch (error) {
        console.error("Refresh token failed:", error);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login"; // Redirect to login page
        return null;
    }
};

// Request interceptor to add Authorization header
ApiRequest.interceptors.request.use(
    (config) => {
        const token = getAccessToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token expiration
ApiRequest.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If token is expired and the request has not been retried yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true; // Mark request as retried

            const newAccessToken = await refreshToken();
            if (newAccessToken) {
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                return ApiRequest(originalRequest); // Retry the failed request
            }
        }

        console.log(error.response.data)

                // Extract error message for toast notification
        const errorMessage =
            error.response?.data?.detail || // Django default error message
            error.response?.data?.message || // Other API error messages
            error.response?.data?.error || // Other API error messages
            "An unexpected error occurred."; // Default message

        toast.warning(errorMessage); // Show error message in toast

        return Promise.reject(error);
    }
);

export default ApiRequest;
