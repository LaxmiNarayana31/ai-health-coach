import axios from 'axios';

// Create an axio instance with base URL configuration
const client = axios.create({
    // VITE_API_URL will be set in production (e.g., in Vercel/Netlify dashboard)
    // If not set, it falls back to '/' which works with the Vite proxy in development
    baseURL: import.meta.env.VITE_API_URL || '/',
    headers: {
        'Content-Type': 'application/json',
    }
});

export default client;
