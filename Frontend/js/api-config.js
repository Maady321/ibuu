/**
 * API Configuration
 * Automatically detects the correct API base URL based on environment
 */

const API_BASE_URL = (() => {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;

    // Development environment - localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        const port = window.location.port;
        return `${protocol}//${hostname}:8000`;
    }

    // Production environment - Vercel deployment
    if (hostname.includes('vercel.app') || hostname.includes('homebuddy')) {
        // Use same origin for production
        return window.location.origin;
    }

    // Default fallback to relative path
    return '';
})();

// Request wrapper with better error handling
async function makeRequest(endpoint, options = {}) {
    const url = API_BASE_URL ? `${API_BASE_URL}${endpoint}` : endpoint;
    
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });
        
        return response;
    } catch (error) {
        console.error(`Request failed for ${url}:`, error);
        throw error;
    }
}

console.log('API Base URL configured:', API_BASE_URL || '(relative paths)');

