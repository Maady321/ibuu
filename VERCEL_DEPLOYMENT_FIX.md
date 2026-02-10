# Vercel Deployment Fix Guide

## Problem
The login page on Vercel (https://full-stack-project-iota-five.vercel.app) was throwing "An error occurred" because the backend API wasn't properly configured for Vercel deployment.

## Solution Applied

### 1. Updated `Frontend/js/api-config.js`
- Changed from empty string to `window.location.origin` for production
- This ensures API calls go to the same domain as the frontend

### 2. Updated `vercel.json`
- Configured proper Python build for FastAPI backend
- Set up routes to direct `/api/*` requests to the backend handler

### 3. Created `Backend/api/index.py`
- Vercel serverless function handler using Mangum
- Wraps the FastAPI app for serverless deployment

### 4. Updated `Backend/requirements.txt`
- Added `mangum` package for AWS Lambda/Vercel compatibility

## Deployment Steps

### Option 1: Redeploy to Vercel (Recommended)

1. **Commit all changes**:
   ```bash
   git add .
   git commit -m "Fix Vercel deployment with proper backend configuration"
   git push
   ```

2. **Vercel will automatically redeploy** with the new configuration

3. **Wait for deployment** to complete (check Vercel dashboard)

4. **Test the login** at https://full-stack-project-iota-five.vercel.app/Frontend/html/user/login.html

### Option 2: Manual Vercel CLI Deployment

If auto-deployment doesn't work:

```bash
# Install Vercel CLI if not already installed
npm i -g vercel

# Deploy from project root
cd c:\Homebuddy_fullstack
vercel --prod
```

## Testing After Deployment

1. **Open the login page**: https://full-stack-project-iota-five.vercel.app/Frontend/html/user/login.html

2. **Try logging in** with existing credentials:
   - Email: `hari_kabadi@gmail.com`
   - Password: `hari123`

3. **Or register a new user** first at the registration page

4. **Check browser console** (F12) for any errors if it still doesn't work

## Troubleshooting

If you still get errors after deployment:

1. **Check Vercel Logs**:
   - Go to Vercel Dashboard → Your Project → Deployments
   - Click on the latest deployment
   - Check "Functions" tab for any errors

2. **Verify Environment Variables**:
   - Make sure `DATABASE_URL` is set in Vercel project settings
   - Go to Project Settings → Environment Variables
   - Add all variables from your `.env` file

3. **Check API Response**:
   - Open browser DevTools (F12)
   - Go to Network tab
   - Try logging in and check the `/api/auth/unified_login` request
   - See what error is returned

## Important Notes

- The backend now runs as a serverless function on Vercel
- Database connections should use connection pooling for serverless
- Cold starts may cause the first request to be slower

## Local Testing Still Works

The changes maintain local development compatibility:
- Frontend on `http://localhost:5500`
- Backend on `http://localhost:8000`
- `api-config.js` automatically detects localhost and uses port 8000
