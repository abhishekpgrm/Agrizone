# Render Deployment Fix Guide

## Problem
The disease detection and pest alerts features are not working because:
1. Render uses ephemeral filesystem - SQLite database gets reset on each deployment
2. Database tables are not persisting between deployments
3. Pest alerts data is not being populated

## Solution
Use PostgreSQL database on Render (free tier available)

## Steps to Fix

### 1. Create PostgreSQL Database on Render

1. Go to your Render Dashboard: https://dashboard.render.com/
2. Click "New +" button → Select "PostgreSQL"
3. Configure:
   - **Name**: `agrizone-db`
   - **Database**: `agrizone`
   - **User**: (auto-generated)
   - **Region**: Same as your web service
   - **Plan**: Free
4. Click "Create Database"
5. Wait for database to be created (takes 1-2 minutes)

### 2. Get Database URL

1. Once created, click on your database
2. Scroll down to "Connections" section
3. Copy the **Internal Database URL** (starts with `postgresql://`)
   - Example: `postgresql://user:password@host/database`

### 3. Add Database URL to Web Service

1. Go to your web service: https://dashboard.render.com/
2. Click on your "agrizone" web service
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL you copied
6. Click "Save Changes"

### 4. Redeploy

The service will automatically redeploy with the new database configuration.

The build script will:
- Install dependencies
- Run migrations (create tables)
- Populate pest alerts data
- Collect static files

### 5. Verify

After deployment completes:
1. Visit: https://agrizone-59m2.onrender.com/alerts/
2. Test pest alerts with:
   - Crop: wheat
   - Location: keorak
3. Visit: https://agrizone-59m2.onrender.com/disease/upload/
4. Upload a plant image to test disease detection

## Alternative: Use Render Disk (Not Recommended)

If you prefer to keep SQLite:

1. Go to your web service settings
2. Add a persistent disk:
   - Mount Path: `/opt/render/project/src/data`
   - Size: 1GB (free)
3. Update settings.py database path to use the disk mount path
4. Redeploy

**Note**: PostgreSQL is recommended for production applications.

## Troubleshooting

### If migrations fail:
```bash
# SSH into your Render service (if available) or use Render Shell
python manage.py migrate --run-syncdb
python manage.py populate_alerts
```

### If pest alerts are empty:
The `populate_alerts` command runs automatically during build. If it fails:
1. Check build logs for errors
2. Ensure DATABASE_URL is set correctly
3. Manually run: `python manage.py populate_alerts`

### Check logs:
1. Go to your web service on Render
2. Click "Logs" tab
3. Look for migration and populate_alerts output

## What Was Fixed

1. **build.sh**: Added `python manage.py populate_alerts` to populate pest data
2. **requirements.txt**: Added PostgreSQL support (`psycopg2-binary`, `dj-database-url`)
3. **settings.py**: Updated to use PostgreSQL when DATABASE_URL is set
4. **views.py**: Added better error handling for database issues

## Files Modified

- `build.sh` - Added populate_alerts command
- `requirements.txt` - Added PostgreSQL dependencies
- `agrizone/settings.py` - Added PostgreSQL configuration
- `pest_alerts/views.py` - Added error handling

## Next Steps

After fixing the database:
1. Test all features thoroughly
2. Consider adding a superuser: `python manage.py createsuperuser`
3. Access admin panel: https://agrizone-59m2.onrender.com/admin/
4. Monitor logs for any errors

## Support

If issues persist:
1. Check Render logs for specific errors
2. Verify all environment variables are set
3. Ensure PostgreSQL database is running
4. Check that migrations completed successfully
