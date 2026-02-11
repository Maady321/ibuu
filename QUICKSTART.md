# HomeBuddy - Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Clone & Setup Environment

```bash
# Clone the project
git clone <repository-url>
cd HomeBuddy

# Copy environment template
cp .env.example .env
```

### 2. Configure Database

Edit `.env` with your database connection:

**Local PostgreSQL:**
```
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/homebuddy
```

**Cloud (Supabase/AWS):**
```
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database
```

### 3. Start Backend

**Windows:**
```bash
run-dev.bat
```

**Linux/Mac:**
```bash
bash run-dev.sh
```

This starts the API server on `http://localhost:8000`

### 4. Access the Application

Open your browser and navigate to:

- **Home Page**: `file:///path/to/index.html`
- **User Login**: `file:///path/to/Frontend/html/user/login.html`
- **Provider Login**: `file:///path/to/Frontend/html/provider/provider-login.html`
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)

## 🔐 Test Credentials

### Admin User
```
Email: admin@homebuddy.com
Password: admin123
```

### Test User (after registration)
Create your own or use any registered credentials

## 📝 First Steps

1. **Register as User**
   - Go to User Login page
   - Click "Register here"
   - Fill in all fields
   - Login with new credentials

2. **Register as Provider**
   - Go to Provider Signup
   - Fill registration form
   - Login to provider dashboard

3. **Browse Services**
   - Login as user
   - Go to Services page
   - Browse available services

4. **Create Booking**
   - Select a service
   - Click "Book Now"
   - Fill booking details
   - Confirm booking

## 🐛 If Something Doesn't Work

1. **Check Backend is Running**
   - Visit `http://localhost:8000`
   - Should show: `{"message": "Home Buddy API Running"}`

2. **Check Database Connection**
   - Verify `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Check terminal for database errors

3. **Check Frontend Paths**
   - Open browser DevTools (F12)
   - Check Network tab for failed requests
   - Look for CORS or 404 errors

4. **Check Console Logs**
   - Backend: Terminal output
   - Frontend: Browser DevTools → Console tab

## 📚 More Information

- **Detailed Setup**: See `SETUP_GUIDE.md`
- **Architecture**: See `FINAL_MODEL.md`
- **API Reference**: Visit `http://localhost:8000/docs`

## 🚀 Deploy to Production

1. Push code to GitHub
2. Connect to Vercel (vercel.com)
3. Set environment variables
4. Deploy!

That's it! Your app is live.

---

**Need Help?** Check the documentation files or review terminal/console logs.
