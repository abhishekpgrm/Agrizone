# 🔧 Troubleshooting Guide - Agrizone on Render

## Common Issues & Solutions

---

## Issue 1: "no such table: disease_diseasedetection"

### Symptoms
- Disease detection page shows error
- Error message mentions missing table
- Happens after uploading image

### Cause
- Database migrations not run
- Using SQLite on ephemeral filesystem
- DATABASE_URL not set

### Solution
```bash
# Option A: Set up PostgreSQL (recommended)
1. Create PostgreSQL database on Render
2. Add DATABASE_URL to environment variables
3. Redeploy

# Option B: Manual migration
python manage.py migrate disease
```

### Verification
```bash
# Check if table exists
python manage.py dbshell
# Then run: SELECT * FROM disease_diseasedetection;
```

---

## Issue 2: Pest Alerts - "An error occurred"

### Symptoms
- Pest alerts page loads but search fails
- Generic error message
- No specific error details

### Cause
- Database not configured
- Pest alerts data not populated
- Database connection failed

### Solution
```bash
# Step 1: Ensure DATABASE_URL is set
# Check in Render Dashboard → Environment

# Step 2: Run migrations
python manage.py migrate

# Step 3: Populate data
python manage.py populate_alerts

# Step 4: Verify
python manage.py shell
>>> from pest_alerts.models import PestAlert
>>> PestAlert.objects.count()
# Should return 8
```

### Verification
- Visit /alerts/
- Search for crop: "wheat"
- Should show Yellow Rust alert

---

## Issue 3: Build Fails on Render

### Symptoms
- Deployment fails during build
- Error in build logs
- Service doesn't start

### Common Causes & Solutions

#### A. Missing Dependencies
```bash
# Error: "No module named 'psycopg2'"
# Solution: Check requirements.txt has:
psycopg2-binary>=2.9.9
```

#### B. Migration Errors
```bash
# Error: "Migration failed"
# Solution: Check migration files exist:
disease/migrations/0001_initial.py
pest_alerts/migrations/0001_initial.py
```

#### C. Build Script Permissions
```bash
# Error: "Permission denied: ./build.sh"
# Solution: Make executable locally:
chmod +x build.sh
git add build.sh
git commit -m "Fix build.sh permissions"
git push
```

#### D. Python Version
```bash
# Error: "Python version mismatch"
# Solution: Check render.yaml has:
PYTHON_VERSION: 3.11.0
```

---

## Issue 4: Database Connection Failed

### Symptoms
- "could not connect to server"
- "connection refused"
- "authentication failed"

### Solutions

#### A. Check DATABASE_URL Format
```
Correct format:
postgresql://user:password@host:port/database

Example:
postgresql://agrizone_user:abc123@dpg-xyz.oregon-postgres.render.com/agrizone_db
```

#### B. Verify Database Status
```
1. Go to Render Dashboard
2. Click on PostgreSQL database
3. Status should be "Available"
4. If not, wait or restart database
```

#### C. Check Region
```
Database and web service should be in same region
- Both in Oregon, or
- Both in Frankfurt, etc.
```

#### D. Use Internal URL
```
Use "Internal Database URL" not "External"
Internal: postgresql://...render.com/...
External: postgresql://...render.com:5432/...
```

---

## Issue 5: Pest Alerts Show No Results

### Symptoms
- Search completes successfully
- Weather data shows
- But no alerts displayed

### Cause
- Data not populated
- Crop name mismatch
- Weather conditions don't match

### Solution
```bash
# Check if data exists
python manage.py shell
>>> from pest_alerts.models import PestAlert
>>> PestAlert.objects.all()
# Should show 8 alerts

# If empty, populate:
python manage.py populate_alerts

# Check specific crop:
>>> PestAlert.objects.filter(crop='wheat')
# Should show Yellow Rust alert
```

### Verification
Try these known working combinations:
- Crop: wheat → Should show Yellow Rust
- Crop: rice → Should show Brown Planthopper, Blast Disease
- Crop: tomato → Should show Late Blight
- Crop: cotton → Should show American Bollworm

---

## Issue 6: Images Not Uploading

### Symptoms
- Upload button doesn't work
- Image upload fails
- "File too large" error

### Solutions

#### A. Check File Size
```python
# In settings.py, add:
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

#### B. Check Media Configuration
```python
# Verify in settings.py:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### C. Check File Type
```
Allowed: .jpg, .jpeg, .png, .webp
Not allowed: .gif, .bmp, .tiff
```

---

## Issue 7: Static Files Not Loading

### Symptoms
- Page loads but no CSS
- Images missing
- JavaScript not working

### Solution
```bash
# Run collectstatic
python manage.py collectstatic --noinput

# Verify settings.py has:
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Check middleware includes:
'whitenoise.middleware.WhiteNoiseMiddleware',
```

---

## Issue 8: Environment Variables Not Working

### Symptoms
- API keys not found
- DEBUG mode wrong
- SECRET_KEY error

### Solution
```bash
# Check in Render Dashboard → Environment
# Ensure these are set:
- SECRET_KEY (auto-generated)
- DEBUG = False
- DATABASE_URL = postgresql://...
- OPENWEATHER_API_KEY = your_key
- OPENAI_API_KEY = your_key

# After adding/changing, service auto-redeploys
```

---

## Issue 9: 500 Internal Server Error

### Symptoms
- Page shows generic 500 error
- No specific error message

### Debug Steps
```bash
# Step 1: Check logs
Render Dashboard → Logs tab
Look for Python traceback

# Step 2: Enable debug temporarily
Set DEBUG=True in environment
(Remember to set back to False!)

# Step 3: Check database
Verify DATABASE_URL is set
Check database is running

# Step 4: Check migrations
python manage.py showmigrations
All should have [X] marks
```

---

## Issue 10: Deployment Succeeds but Features Don't Work

### Symptoms
- Build completes successfully
- Service shows "Live"
- But features still broken

### Checklist
```bash
# 1. Verify migrations ran
Check logs for: "Running migrations..."

# 2. Verify data populated
Check logs for: "Successfully populated 8 pest alerts"

# 3. Check database connection
python manage.py dbshell
# Should connect without error

# 4. Verify tables exist
python manage.py inspectdb
# Should show all models

# 5. Manual verification
python setup_database.py
```

---

## Diagnostic Commands

### Check Database
```bash
python manage.py dbshell
\dt  # List all tables (PostgreSQL)
.tables  # List all tables (SQLite)
```

### Check Migrations
```bash
python manage.py showmigrations
# All should have [X]
```

### Check Models
```bash
python manage.py shell
>>> from disease.models import DiseaseDetection
>>> from pest_alerts.models import PestAlert
>>> DiseaseDetection.objects.count()
>>> PestAlert.objects.count()
```

### Check Settings
```bash
python manage.py diffsettings
# Shows all settings and their values
```

---

## Getting Help

### Check Logs
```
Render Dashboard → Your Service → Logs
Look for:
- Red error messages
- Python tracebacks
- Database connection errors
```

### Check Database Logs
```
Render Dashboard → PostgreSQL Database → Logs
Look for:
- Connection attempts
- Authentication errors
- Query errors
```

### Manual Setup
```bash
# If all else fails, run manual setup:
python setup_database.py
```

---

## Prevention Tips

1. **Always use PostgreSQL on Render** (not SQLite)
2. **Set DATABASE_URL** before first deployment
3. **Check logs** after each deployment
4. **Test features** immediately after deployment
5. **Keep backups** of database (Render does this automatically)
6. **Monitor** database usage and limits
7. **Use environment variables** for all secrets
8. **Test locally** before deploying

---

## Quick Reference

### Working Configuration
```yaml
# render.yaml
DATABASE_URL: postgresql://...
DEBUG: False
SECRET_KEY: (auto-generated)
```

### Working Database
```
Status: Available
Plan: Free
Storage: < 1GB
Tables: 8+ tables
Pest Alerts: 8 records
```

### Working Features
```
✅ Pest Alerts: Shows weather + threats
✅ Disease Detection: Uploads + predicts
✅ Crop Recommendation: Works
✅ Weather: Shows forecast
✅ AI Assistant: Responds (if API key set)
```

---

## Still Having Issues?

1. Read `QUICK_FIX.md` for setup steps
2. Read `RENDER_DEPLOYMENT_FIX.md` for detailed guide
3. Run `python setup_database.py` for manual setup
4. Check Render documentation: https://render.com/docs
5. Check Django documentation: https://docs.djangoproject.com/

---

**Most issues are resolved by ensuring DATABASE_URL is set correctly! 🎯**
