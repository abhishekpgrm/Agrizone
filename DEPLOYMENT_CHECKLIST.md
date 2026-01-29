# 🎯 Agrizone Deployment Checklist

## Pre-Deployment ✅

- [x] Code fixes applied
- [x] PostgreSQL support added
- [x] Build script updated
- [x] Documentation created
- [ ] Changes committed to git
- [ ] Changes pushed to repository

## Render Setup 🚀

### Step 1: Create PostgreSQL Database
- [ ] Login to Render Dashboard
- [ ] Click "New +" → "PostgreSQL"
- [ ] Name: `agrizone-db`
- [ ] Plan: Free
- [ ] Region: Same as web service
- [ ] Click "Create Database"
- [ ] Wait for status: "Available" ✓

### Step 2: Get Database Credentials
- [ ] Open the database you just created
- [ ] Find "Connections" section
- [ ] Copy "Internal Database URL"
- [ ] Save it temporarily (you'll need it in next step)

### Step 3: Configure Web Service
- [ ] Go to your "agrizone" web service
- [ ] Click "Environment" tab
- [ ] Click "Add Environment Variable"
- [ ] Add: `DATABASE_URL` = [paste URL]
- [ ] Click "Save Changes"
- [ ] Service starts redeploying automatically

### Step 4: Monitor Deployment
- [ ] Click "Logs" tab
- [ ] Watch for these messages:
  - [ ] "Installing dependencies..."
  - [ ] "Running migrations..."
  - [ ] "Successfully populated 8 pest alerts"
  - [ ] "Build successful"
  - [ ] "Starting gunicorn..."
- [ ] Wait for "Live" status

## Testing 🧪

### Test Pest Alerts
- [ ] Visit: https://agrizone-59m2.onrender.com/alerts/
- [ ] Page loads without error
- [ ] Enter Crop: `wheat`
- [ ] Enter Location: `keorak` (or any city)
- [ ] Click "Scan for Threats"
- [ ] Should show:
  - [ ] Weather information
  - [ ] Yellow Rust alert
  - [ ] Symptoms, prevention, treatment
  - [ ] No error messages

### Test Disease Detection
- [ ] Visit: https://agrizone-59m2.onrender.com/disease/upload/
- [ ] Page loads without error
- [ ] Upload a plant leaf image
- [ ] Click submit
- [ ] Should show:
  - [ ] Disease prediction
  - [ ] Confidence score
  - [ ] Treatment suggestions
  - [ ] No error messages

### Test Other Features
- [ ] Home page loads
- [ ] Crop Recommendation works
- [ ] Weather forecast works
- [ ] AI Assistant works (if API key set)

## Verification 🔍

### Check Database
- [ ] Go to PostgreSQL database on Render
- [ ] Status shows "Available"
- [ ] No error messages in logs

### Check Environment Variables
- [ ] Go to web service → Environment
- [ ] Verify these are set:
  - [ ] DATABASE_URL ✓
  - [ ] SECRET_KEY ✓
  - [ ] DEBUG = False ✓
  - [ ] OPENWEATHER_API_KEY (optional)
  - [ ] OPENAI_API_KEY (optional)

### Check Logs
- [ ] No migration errors
- [ ] No database connection errors
- [ ] No 500 errors
- [ ] Application starts successfully

## Troubleshooting 🔧

If something doesn't work:

### Pest Alerts Still Failing
- [ ] Check if DATABASE_URL is set correctly
- [ ] Check logs for "populate_alerts" errors
- [ ] Verify PostgreSQL database is "Available"
- [ ] Try manual setup: `python setup_database.py`

### Disease Detection Still Failing
- [ ] Check logs for migration errors
- [ ] Verify DATABASE_URL is set
- [ ] Check if disease app is in INSTALLED_APPS
- [ ] Try: `python manage.py migrate disease`

### Database Connection Issues
- [ ] Verify DATABASE_URL format: `postgresql://user:pass@host/db`
- [ ] Check if PostgreSQL database is running
- [ ] Ensure web service and database are in same region
- [ ] Check database logs for connection attempts

### Build Fails
- [ ] Check if requirements.txt has psycopg2-binary
- [ ] Verify build.sh has execute permissions
- [ ] Check Python version (should be 3.11.0)
- [ ] Look for specific error in build logs

## Post-Deployment 📝

### Optional: Create Admin User
```bash
# If you have Render Shell access
python manage.py createsuperuser
```

### Optional: Verify Data
- [ ] Login to admin: https://agrizone-59m2.onrender.com/admin/
- [ ] Check Pest Alerts: Should have 8 entries
- [ ] Check Disease Detections: Should be empty initially

### Monitor
- [ ] Check logs regularly for errors
- [ ] Monitor database usage
- [ ] Test all features periodically

## Success Criteria ✨

Your deployment is successful when:
- ✅ All pages load without errors
- ✅ Pest Alerts shows weather and threats
- ✅ Disease Detection accepts and processes images
- ✅ No database errors in logs
- ✅ Data persists across deployments

## Time Estimate ⏱️

- Database setup: 2-3 minutes
- Configuration: 1-2 minutes
- Deployment: 3-5 minutes
- Testing: 2-3 minutes
- **Total: ~10-15 minutes**

## Support Resources 📚

- Quick Guide: `QUICK_FIX.md`
- Detailed Guide: `RENDER_DEPLOYMENT_FIX.md`
- Summary: `DEPLOYMENT_FIX_SUMMARY.md`
- Manual Setup: `setup_database.py`

## Notes 📌

- PostgreSQL Free tier is sufficient for this app
- Database persists across deployments
- Media files still on ephemeral storage (consider S3 later)
- Local development still uses SQLite (no changes needed)

---

**Once all checkboxes are checked, your Agrizone app is fully deployed! 🎉**
