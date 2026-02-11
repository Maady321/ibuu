# HomeBuddy - Production Deployment Guide

## 🚀 Deploying to Vercel

### Prerequisites

- GitHub account with repository
- Vercel account (free tier available)
- Production database (Supabase, AWS RDS, or similar)
- Custom domain (optional)

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Production ready version"
git push origin main
```

### Step 2: Create/Connect Vercel Project

**Option A: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

**Option B: Using Web Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Select "Import Git Repository"
4. Choose your GitHub repository
5. Configure project settings
6. Deploy

### Step 3: Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables, add:

```
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database
SECRET_KEY=your-secret-key-here (generate with: python -c 'import secrets; print(secrets.token_hex(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=https://yourdomain.vercel.app
```

**To generate a strong SECRET_KEY:**

```python
import secrets
print(secrets.token_hex(32))
```

Or use this online: https://tools.ietf.org/html/rfc4648

### Step 4: Set Up Production Database

Choose one of the following:

#### Option A: Supabase (Recommended for beginners)

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Copy the connection string
4. Add to Vercel environment variables as `DATABASE_URL`

Example connection string:
```
postgresql+psycopg2://postgres.xxxx:password@aws-0-region.pooler.supabase.com:6543/postgres
```

#### Option B: AWS RDS

1. Create RDS PostgreSQL instance
2. Set security groups to allow Vercel IPs
3. Copy connection string
4. Add to Vercel environment variables

#### Option C: Other Cloud Providers

- **Google Cloud SQL**
- **Azure Database for PostgreSQL**
- **DigitalOcean Managed Databases**
- **Heroku PostgreSQL**

All follow similar setup patterns.

### Step 5: Test Production Deployment

1. Visit your Vercel deployment URL
2. Test user registration and login
3. Test API endpoints
4. Check admin dashboard
5. Review Vercel logs for errors

```bash
# View deployment logs
vercel logs
```

## 📋 Production Checklist

### Before Deployment
- [ ] `.env` has production values
- [ ] `DATABASE_URL` is set correctly
- [ ] `SECRET_KEY` is strong and unique
- [ ] CORS origins are restricted
- [ ] HTTPS is enabled (automatic with Vercel)
- [ ] Database backups are configured
- [ ] All tests pass locally

### After Deployment
- [ ] API is responding (`/api` endpoint)
- [ ] User registration works
- [ ] Login works for all roles
- [ ] Database queries are fast
- [ ] No errors in Vercel logs
- [ ] Frontend loads without CORS errors
- [ ] Static files serve correctly

## 🔒 Security Configurations

### API Keys & Secrets

Never commit these to GitHub:
```
✗ Database passwords
✗ API keys
✗ Secret keys
✗ OAuth tokens
```

Always use Vercel environment variables.

### CORS in Production

The app automatically restricts CORS to:
```
https://homebuddy.vercel.app
https://www.homebuddy.vercel.app
```

To allow custom domains, add to `.env`:
```
FRONTEND_URL=https://yourdomain.com,https://www.yourdomain.com
```

### HTTPS Only

Vercel automatically:
- Uses HTTPS for all deployments
- Redirects HTTP to HTTPS
- Provides SSL certificates

### Database Security

For Supabase:
1. Enable SSL connections (already required)
2. Set IP allowlist (if available)
3. Use strong passwords
4. Enable backups
5. Restrict database roles

## 🐛 Troubleshooting Production

### No Response from API

**Check:**
1. Vercel deployment status
2. `DATABASE_URL` environment variable
3. Database connection from Vercel
4. Firewall rules

**Debug:**
```bash
# Check logs
vercel logs

# Check environment variables are set
curl https://your-domain.vercel.app/
```

### Database Connection Errors

**Check:**
1. `DATABASE_URL` format is correct
2. Database is accessible from Vercel
3. Database credentials are valid
4. IP allowlist includes Vercel IPs

**Vercel IPs:** Vercel uses dynamic IPs, so use % in allowlist or disable IP restrictions.

### CORS Errors

**Check:**
1. Frontend domain is in CORS allowlist
2. API response has correct headers
3. Browser console shows specific error

**Fix:**
Update `CORS origins` in `Backend/main.py` or `FRONTEND_URL` env variable.

### Slow API Responses

**Solutions:**
1. Add database indexes
2. Optimize queries
3. Add caching
4. Use connection pooling (already configured)
5. Scale database resources

### Static Files Not Loading

**Check:**
1. `vercel.json` routes are correct
2. Files exist in `Frontend/` directory
3. File paths in HTML are correct
4. Vercel deployment includes all files

## 📊 Monitoring Production

### Vercel Dashboard

- **Deployments**: See all deployed versions
- **Analytics**: Traffic and performance
- **Logs**: Real-time server logs
- **Rollback**: Revert to previous version

### Application Monitoring

Add these to your monitoring stack:
- **Sentry** (Error tracking)
- **LogRocket** (Session replay)
- **New Relic** (Performance monitoring)
- **Datadog** (Comprehensive monitoring)

### Database Monitoring

Monitor your database provider's dashboard:
- Connection count
- Query performance
- Disk usage
- Backup status

## 🔄 CI/CD Pipeline

### Automatic Deployment

Vercel automatically deploys when:
1. Code is pushed to `main` branch
2. Pull request is created (preview deployment)

### Manual Deployment

```bash
# Deploy to production
vercel --prod

# Deploy to preview
vercel

# Rollback to previous
vercel rollback
```

## 📈 Scaling for Growth

As your application grows:

1. **Database**
   - Upgrade PostgreSQL resources
   - Add read replicas
   - Implement caching (Redis)

2. **Backend**
   - Already serverless (auto-scaling)
   - Optimize code
   - Add background jobs (Celery)

3. **Frontend**
   - Use CDN (Vercel default)
   - Implement lazy loading
   - Optimize images

4. **Monitoring**
   - Set up alerts
   - Monitor error rates
   - Track performance metrics

## 🛣️ Custom Domain Setup

1. **Register Domain**
   - GoDaddy, Namecheap, Google Domains, etc.

2. **Point to Vercel**
   - Update DNS records
   - Follow Vercel's domain instructions

3. **Verify Domain**
   - Vercel verifies domain ownership
   - SSL certificate auto-generated

4. **Test**
   - Visit your custom domain
   - Verify HTTPS works
   - Check all features

## 💰 Costs

### Vercel (Free tier includes)
- 100 GB bandwidth/month
- Unlimited deployments
- Serverless function executions
- SSL certificates
- Global CDN

### Database Costs

**Supabase:**
- Free tier: Good for startups
- Paid: Based on storage & usage

**AWS RDS:**
- Small instance: ~$15/month
- Scales with usage

## 📞 Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Supabase Docs**: https://supabase.com/docs

## ✅ Deployment Completed!

Your HomeBuddy application is now live in production! 🎉

**Next Steps:**
1. Monitor performance
2. Gather user feedback
3. Plan feature updates
4. Optimize based on usage

---

**Last Updated**: February 2026
**Version**: 1.0.0 - Production Ready
