# HomeBuddy Full-Stack Application - Setup & Deployment Guide

## 📋 Project Structure

```
HomeBuddy/
├── Backend/                 # FastAPI backend application
│   ├── main.py             # Main FastAPI application
│   ├── dependencies.py      # Dependency injection setup
│   ├── db/                 # Database configuration
│   ├── models/             # SQLAlchemy models
│   ├── routers/            # API route handlers
│   ├── schemas/            # Pydantic schemas
│   ├── requirements.txt    # Python dependencies
│   └── myenv/              # Virtual environment (local dev)
├── Frontend/                # HTML, CSS, JavaScript
│   ├── html/               # HTML pages
│   ├── css/                # Stylesheets
│   └── js/                 # JavaScript files
├── api/
│   └── index.py           # Vercel serverless entry point
├── vercel.json            # Vercel deployment configuration
├── requirements.txt       # Root dependencies (same as Backend)
├── .env                   # Environment variables (local development)
├── .env.example           # Example environment file
├── run-dev.bat            # Windows development startup script
├── run-dev.sh             # Unix/Linux/Mac development startup script
└── README.md              # This file
```

## 🔧 Configuration & Environment

### Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```bash
# Development Environment
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/homebuddy
SECRET_KEY=your-dev-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_URL=http://localhost:3000
FRONTEND_URL=http://localhost:3000,http://127.0.0.1:3000
DEBUG=True
```

### For Production (Vercel)

These are set in Vercel environment variables:

```
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg2://user:pass@host:port/db
SECRET_KEY=secure-production-key
```

## 🚀 Development Setup

### Prerequisites

- Python 3.9 or higher
- PostgreSQL (local or cloud)
- Git
- Modern web browser

### Step 1: Clone & Setup

```bash
git clone <repository-url>
cd HomeBuddy

# Copy environment template
cp .env.example .env

# Update .env with your database credentials
```

### Step 2: Start Backend (Option A - Windows)

```bash
# Run the Windows batch script
run-dev.bat
```

The backend will start on `http://localhost:8000`

### Step 2: Start Backend (Option B - Linux/Mac)

```bash
# Run the bash script
bash run-dev.sh
```

Or manually:

```bash
cd Backend

# Create virtual environment
python -m venv myenv

# Activate it
# On Linux/Mac:
source myenv/bin/activate
# On Windows:
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3: Start Frontend

For development, you can open HTML files directly in your browser:

```bash
# Check API configuration
# Frontend/js/api-config.js automatically detects localhost:8000
```

Open your browser and navigate to:
- **Home**: `file:///path/to/Frontend/index.html`
- **User Login**: `file:///path/to/Frontend/html/user/login.html`
- **Provider Login**: `file:///path/to/Frontend/html/provider/provider-login.html`

## 🧪 Testing User Flow

### 1. **User Registration & Login**

1. Open `Frontend/html/user/login.html`
2. Click "Register" to sign up
3. Fill in the registration form:
   - Name, Email, Phone, Address, Password
4. Submit to create account
5. Login with your credentials
6. Should redirect to `Frontend/html/user/dashboard.html`

### 2. **Provider Registration & Login**

1. Open `Frontend/html/provider/provider-signup.html`
2. Register as a provider
3. Login at `Frontend/html/provider/provider-login.html`
4. Should redirect to `Frontend/html/provider/provider-dashboard.html`

### 3. **Admin Access**

1. Open `Frontend/html/user/login.html`
2. Use credentials: 
   - Email: `admin@homebuddy.com`
   - Password: `admin123`
3. Should redirect to `Frontend/html/admin/admin-dashboard.html`

### 4. **API Testing** (Optional)

Use Postman or curl:

```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "address": "123 Main St",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/unified_login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

## 📦 Production Deployment (Vercel)

### Step 1: Prepare for Deployment

1. Ensure all changes are committed to git
2. Update `.env` to production values
3. Test locally in production mode:

```bash
cd Backend
ENVIRONMENT=production python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 2: Deploy to Vercel

#### Using Vercel CLI:

```bash
# Install Vercel CLI (if not already installed)
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Using GitHub Integration:

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Set environment variables in Vercel dashboard
5. Deploy!

### Step 3: Configure Vercel Environment Variables

In Vercel project settings, add:

```
ENVIRONMENT=production
DATABASE_URL=your-production-database-url
SECRET_KEY=your-production-secret-key
```

## 🔍 Troubleshooting

### Issue: "Database connection error"

**Solution**: Ensure `DATABASE_URL` is correct in `.env`:
- For local: `postgresql+psycopg2://postgres:password@localhost:5432/homebuddy`
- For cloud (Supabase/AWS): Get the connection string from your provider

### Issue: "CORS error in production"

**Solution**: Update `CORS` origins in `Backend/main.py`:
```python
if ENVIRONMENT == "production":
    allowed_origins = [
        "https://your-domain.vercel.app",
        "https://your-domain.com"
    ]
```

### Issue: "API requests failing in production"

**Solution**: 
1. Open browser DevTools (F12) → Network tab
2. Check API URL in the request
3. Ensure backend is responding: Visit `https://api.your-domain.com/` (should show "Home Buddy API Running")
4. Check Vercel logs for errors

### Issue: "Static files not loading"

**Solution**: 
- Ensure `vercel.json` routes are correct
- Frontend assets should be in `Frontend/` directory
- Check Vercel deployment logs

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/provider/login` - Provider login
- `POST /api/auth/unified_login` - Login for all roles (recommended)
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/users` - Get all users

### Other Endpoints
- `GET /api/services` - List services
- `POST /api/bookings` - Create booking
- `GET /api/bookings/my` - Get user bookings
- `POST /api/reviews` - Submit review

See `Backend/routers/` for all available endpoints.

## 🔐 Security Best Practices

✅ **Production Setup**:
1. Use strong `SECRET_KEY`
2. Use environment variables for sensitive data
3. Set `ENVIRONMENT=production`
4. Restrict CORS origins
5. Use HTTPS only
6. Keep dependencies updated

❌ **Never In Production**:
- Use hardcoded credentials
- Expose API keys in frontend code
- Leave debug mode enabled
- Set `allow_origins=["*"]` without restrictions

## 📞 Support

For issues or questions:
1. Check Vercel logs: `vercel logs`
2. Check local backend logs
3. Review `.env` configuration
4. Check browser console for frontend errors

## 🎉 Success Indicators

✅ Backend running: Navigate to `http://localhost:8000/docs` (should show Swagger UI)
✅ Frontend working: All HTML pages load without CORS errors
✅ Database connected: Can register and login users
✅ Production ready: All endpoints respond correctly
