#!/usr/bin/env python
"""
Manual Database Setup Script
Run this if automatic setup fails during deployment
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrizone.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def check_database():
    """Check if database is accessible"""
    try:
        connection.ensure_connection()
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def run_migrations():
    """Run database migrations"""
    try:
        print("\nRunning migrations...")
        call_command('migrate', '--noinput')
        print("✓ Migrations completed")
        return True
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False

def populate_alerts():
    """Populate pest alerts data"""
    try:
        print("\nPopulating pest alerts...")
        call_command('populate_alerts')
        print("✓ Pest alerts populated")
        return True
    except Exception as e:
        print(f"✗ Failed to populate alerts: {e}")
        return False

def check_tables():
    """Check if required tables exist"""
    try:
        from disease.models import DiseaseDetection
        from pest_alerts.models import PestAlert
        
        disease_count = DiseaseDetection.objects.count()
        alert_count = PestAlert.objects.count()
        
        print(f"\n✓ Disease detections: {disease_count}")
        print(f"✓ Pest alerts: {alert_count}")
        return True
    except Exception as e:
        print(f"✗ Table check failed: {e}")
        return False

def main():
    print("=" * 50)
    print("Agrizone Database Setup")
    print("=" * 50)
    
    # Check database connection
    if not check_database():
        print("\nPlease check your DATABASE_URL environment variable")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("\nMigration failed. Check error messages above.")
        sys.exit(1)
    
    # Populate data
    if not populate_alerts():
        print("\nFailed to populate alerts. Check error messages above.")
        sys.exit(1)
    
    # Verify tables
    check_tables()
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("=" * 50)

if __name__ == '__main__':
    main()
