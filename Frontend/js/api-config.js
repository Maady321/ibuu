const API_BASE_URL = (() => {
    const hostname = window.location.hostname;

    // Check if running on localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:8000';
    }

    // For Vercel deployment
    if (hostname.includes('vercel.app')) {
        // Use the current origin for same-domain deployment
        return window.location.origin;
    }

    // Default: use current origin
    return window.location.origin;
})();

console.log('API Base URL:', API_BASE_URL);
console.log('Current hostname:', window.location.hostname);
