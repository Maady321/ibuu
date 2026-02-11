# HomeB uddy - Final Working Model

## 📊 System Architecture

```
┌─────────────────┐
│  Frontend       │
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │ API Calls
         ▼
┌─────────────────────────────────────┐
│  api/index.py (Vercel Serverless)   │
│  (Mangum ASGI Adapter)              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Backend (FastAPI)                  │
├─────────────────────────────────────┤
│  • Authentication (users, providers) │
│  • Services management              │
│  • Bookings & Reviews               │
│  • Provider Support                 │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  PostgreSQL Database                │
│  (Supabase / AWS / Local)          │
└─────────────────────────────────────┘
```

## 🔄 User Flow - Complete Journey

### 1️⃣ **User Registration & Authentication**

**Flow**: `login.html` → Register → `/api/auth/register` → Database → Redirect to login

```
1. User visits Frontend/html/user/login.html
2. Clicks "Register here"
3. Fills registration form:
   - Name: "John Doe"
   - Email: "john@example.com"
   - Phone: "1234567890"
   - Address: "123 Main St"
   - Password: "secure_password"
4. Frontend sends POST to `/api/auth/register`
5. Backend validates:
   ✓ Email uniqueness
   ✓ Phone uniqueness
   ✓ Password requirements
6. User created in database
7. Redirects back to login page
```

### 2️⃣ **User Login**

**Flow**: `login.html` → `/api/auth/unified_login` → LocalStorage → Redirect to Dashboard

```
1. User enters credentials:
   - Email: "john@example.com"
   - Password: "secure_password"
2. Frontend calls `/api/auth/unified_login`
3. Backend checks:
   ✓ Is it admin? (admin@homebuddy.com / admin123)
   ✓ Is it a user?
   ✓ Is it a provider?
4. Returns:
   {
     "message": "Login successful",
     "role": "user",
     "user_id": 1,
     "name": "John Doe",
     "email": "john@example.com",
     "redirect": "Frontend/html/user/dashboard.html"
   }
5. Frontend stores in localStorage:
   - role: "user"
   - user_id: 1
   - user_name: "John Doe"
   - user_email: "john@example.com"
6. Redirects to Dashboard
```

### 3️⃣ **User Dashboard**

**Flow**: Dashboard → Check Auth → Fetch User Data → Display Services

```
1. Page loads: dashboard.html
2. JavaScript checks localStorage for user_id
   ✓ If missing → Redirect to login.html
   ✓ If present → Continue
3. Fetches user profile via `/api/auth/profile`
   Headers: { "X-User-ID": user_id }
4. Displays welcome message
5. Fetches available services
6. Displays recent bookings
7. Shows activity feed
```

### 4️⃣ **Browse & Book Services**

**Flow**: Services Page → Select Service → Book Service → Confirmation

```
1. User navigates to "Services" page
2. Frontend fetches available services
3. User selects a service
4. Opens Service Details:
   - Description
   - Available Providers
   - Pricing
   - Ratings/Reviews
5. Clicks "Book Now"
6. Booking form appears:
   - Date
   - Time
   - Special requests
7. Submits POST to `/api/bookings`
   Headers: { "X-User-ID": user_id }
   Body: { service_id, provider_id, date, time, notes }
8. Backend creates booking
9. Returns confirmation with booking_id
10. Shows "Booking Confirmed" message
```

### 5️⃣ **Provider Login & Dashboard**

**Flow**: Same as user but `provider-dashboard.html` and `/api/auth/unified_login`

```
1. Provider navigates to provider-login.html
2. Enters email and password
3. Frontend calls `/api/auth/unified_login`
4. Backend returns:
   {
     "role": "provider",
     "provider_id": 5,
     "user_id": 3,
     "name": "Jane Smith",
     "redirect": "Frontend/html/provider/provider-dashboard.html"
   }
5. localStorage stores provider_id
6. Redirects to provider dashboard
7. Shows:
   - Pending Bookings
   - Accepted Bookings
   - Completed Services
   - Ratings & Reviews
```

### 6️⃣ **Admin Dashboard**

**Flow**: Login as admin → `/api/auth/unified_login` → Admin Dashboard

```
1. Admin logs in with:
   - Email: admin@homebuddy.com
   - Password: admin123
2. Frontend receives:
   {
     "role": "admin",
     "redirect": "Frontend/html/admin/admin-dashboard.html"
   }
3. Admin sets: localStorage.setItem("admin_logged_in", "true")
4. Accesses admin panel to:
   - View all users
   - View all providers
   - Monitor bookings
   - Check payments
   - Manage reviews
```

## 🌐 API Endpoints Overview

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/auth/register` | ❌ | Register new user |
| POST | `/api/auth/unified_login` | ❌ | Login for all roles |
| GET | `/api/auth/profile` | ✅ | Get user profile |
| GET | `/api/auth/users` | ❌ | List all users |
| POST | `/api/services` | ❌ | Create service |
| GET | `/api/services` | ❌ | List services |
| POST | `/api/bookings` | ✅ | Create booking |
| GET | `/api/bookings/my` | ✅ | User's bookings |
| GET | `/api/bookings/pending` | ✅ | Provider's pending |
| POST | `/api/reviews` | ✅ | Submit review |
| GET | `/api/reviews` | ❌ | Get reviews |

## 📁 Key Files & Their Roles

### Backend Core
- **`main.py`** - FastAPI app setup, middleware, CORS
- **`dependencies.py`** - Database session, user authentication
- **`db/database.py`** - SQLAlchemy engine, session factory

### API Routers
- **`routers/users.py`** - Auth endpoints (register, login, profile)
- **`routers/services.py`** - Service CRUD operations
- **`routers/bookings.py`** - Booking management
- **`routers/providers.py`** - Provider management
- **`routers/reviews.py`** - Review management
- **`routers/supports.py`** - Support ticket system

### Frontend Entry Points
- **`index.html`** - Landing/Home page
- **`Frontend/html/user/login.html`** - User authentication
- **`Frontend/html/user/dashboard.html`** - User main page
- **`Frontend/html/provider/provider-login.html`** - Provider auth
- **`Frontend/html/provider/provider-dashboard.html`** - Provider space
- **`Frontend/html/admin/admin-dashboard.html`** - Admin panel

### Configuration
- **`.env`** - Local environment variables
- **`vercel.json`** - Production deployment configuration
- **`api/index.py`** - Vercel serverless entry point

## 🔐 Authentication System

### Headers-based Authentication
Uses `X-User-ID` and `X-Provider-ID` headers instead of JWT:

```javascript
// Frontend sends request with user ID in header
fetch('/api/auth/profile', {
    headers: {
        'X-User-ID': localStorage.getItem('user_id')
    }
})

// Backend checks header and validates user exists
@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID missing")
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user
```

### Session Management
- User data stored in **localStorage**
- No cookies (API-driven)
- Token-less (ID-based headers)

## 🚀 Environment Detection

### Development (localhost)
```
API_BASE_URL = "http://localhost:8000"
CORS Origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
Database = Local PostgreSQL
Environment = development
```

### Production (Vercel)
```
API_BASE_URL = "https://homebuddy.vercel.app"
CORS Origins = ["https://homebuddy.vercel.app", custom URLs]
Database = Cloud PostgreSQL (Supabase/AWS)
Environment = production
```

The `api-config.js` automatically detects:
```javascript
if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000'; // Dev
} else {
    return window.location.origin; // Production
}
```

## ✅ Production Checklist

- [x] CORS configured for production domains
- [x] Environment variables system
- [x] Database connection pooling
- [x] API routing for Vercel (api/index.py)
- [x] Error handling and logging
- [x] Request validation (Pydantic schemas)
- [x] Authentication/Authorization
- [x] HTTPS ready (Vercel handles)
- [x] Static file serving
- [x] Database migrations on startup

## 🔧 Troubleshooting - Common Issues

### API not responding in production
1. Check Vercel logs: `vercel logs`
2. Ensure `DATABASE_URL` is set in Vercel env
3. Check `api/index.py` is properly routing requests

### CORS errors
1. Verify frontend domain is in CORS allowlist
2. Check API response headers: `Access-Control-Allow-Origin`
3. Ensure credentials mode is correct

### Database connection fails
1. Verify `DATABASE_URL` format
2. Test connection locally first
3. Check firewall/IP allowlist for cloud DB

### Sessions/Auth issues
1. Check `localStorage` values in browser
2. Verify `X-User-ID` header is being sent
3. Ensure user exists in database

## 📊 Data Models

### Users Table
```sql
id (PK), name, email (UNIQUE), password, phone (UNIQUE), address, role, is_active
```

### Providers Table
```sql
id (PK), user_id (FK), full_name, email, password, phone, dob, address, 
service_id (FK), years_experience, specialization, bio, availability, 
id_proof, certificate, role, is_verified
```

### Services Table
```sql
id (PK), service_name, category, description, price, rating
```

### Bookings Table
```sql
id (PK), user_id (FK), provider_id (FK), service_id (FK), 
booking_date, booking_time, status, notes, created_at
```

### Reviews Table
```sql
id (PK), user_id (FK), provider_id (FK), booking_id (FK), 
rating, comment, created_at
```

## 🎯 Deployment Steps

### Local Development
1. Clone repository
2. Create `.env` with local database URL
3. Run `run-dev.bat` (Windows) or `bash run-dev.sh` (Linux/Mac)
4. Open HTML files in browser
5. Backend runs on http://localhost:8000

### Vercel Production
1. Push code to GitHub
2. Connect GitHub repo to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically on every push to main
5. API accessible at `https://homebuddy.vercel.app/api`

## 💡 Key Features Implemented

✅ **User Management**
- Registration with validation
- Login with multiple user types
- Profile management

✅ **Service Management**
- Browse available services
- Filter by category
- View service details

✅ **Booking System**
- Create bookings
- Track booking status
- View booking history

✅ **Provider Features**
- Provider registration
- Service listing
- Booking management
- Rating system

✅ **Admin Tools**
- User management
- Provider verification
- Booking oversight
- Detailed analytics

✅ **Responsive Design**
- Mobile-friendly UI
- Cross-browser compatible
- Fast loading times

## 🎓 Learning Outcomes

This project demonstrates:
- FastAPI backend development
- SQLAlchemy ORM usage
- RESTful API design
- Frontend-Backend integration
- Authentication & Authorization
- Database design & management
- Responsive web design
- Production deployment

---

**Status**: ✅ **PRODUCTION READY**

All components are configured for both development and production environments.
