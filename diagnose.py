#!/usr/bin/env python3
"""
Quick Fix Script for NoteMaster AI
This script will diagnose and attempt to fix common issues
"""

import os
import sys

print("=" * 70)
print("🔧 NoteMaster AI - Diagnostic & Fix Tool")
print("=" * 70)
print()

# Step 1: Check current directory
print("Step 1: Checking current directory...")
current_dir = os.getcwd()
print(f"  Current directory: {current_dir}")

# Check if we're in the right folder
if not os.path.exists('app.py'):
    print("\n  ❌ ERROR: app.py not found!")
    print("  You must run this script from the notemaster-ai folder")
    print("\n  To fix:")
    print("  1. Open terminal/command prompt")
    print("  2. Navigate to the project folder:")
    print("     cd path/to/notemaster-ai")
    print("  3. Run this script again")
    sys.exit(1)
else:
    print("  ✅ Found app.py - you're in the correct folder")

# Step 2: Check Python version
print("\nStep 2: Checking Python version...")
py_version = sys.version_info
print(f"  Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
    print("  ⚠️  Warning: Python 3.8+ recommended")
else:
    print("  ✅ Python version is good")

# Step 3: Create missing folders
print("\nStep 3: Creating missing folders...")
folders = ['instance', 'templates', 'static', 'static/js']
for folder in folders:
    if not os.path.exists(folder):
        print(f"  Creating {folder}/")
        os.makedirs(folder, exist_ok=True)
    else:
        print(f"  ✅ {folder}/ exists")

# Step 4: Check critical files
print("\nStep 4: Checking critical files...")
critical_files = {
    'app.py': 'Main application file',
    'config.py': 'Configuration',
    'models.py': 'Database models',
    'routes.py': 'API routes',
    'utils.py': 'Utility functions',
    'templates/index.html': 'Frontend template',
    'static/js/script.js': 'JavaScript file',
}

missing_files = []
for file, description in critical_files.items():
    if os.path.exists(file):
        print(f"  ✅ {file} - {description}")
    else:
        print(f"  ❌ {file} - MISSING!")
        missing_files.append(file)

if missing_files:
    print(f"\n  ❌ ERROR: {len(missing_files)} critical file(s) missing!")
    print("  Please make sure all project files are downloaded correctly.")
    sys.exit(1)

# Step 5: Check .env file
print("\nStep 5: Checking environment configuration...")
if not os.path.exists('.env'):
    print("  ❌ .env file not found!")
    print("\n  CREATING .env file from template...")
    
    if os.path.exists('.env.example'):
        # Copy from example
        with open('.env.example', 'r') as f:
            content = f.read()
        with open('.env', 'w') as f:
            f.write(content)
        print("  ✅ Created .env file from .env.example")
    else:
        # Create basic .env
        with open('.env', 'w') as f:
            f.write("SECRET_KEY=notemaster-dev-key-12345\n")
            f.write("GEMINI_API_KEY=your-gemini-api-key-here\n")
            f.write("DATABASE_URL=sqlite:///notemaster.db\n")
        print("  ✅ Created basic .env file")
    
    print("\n  ⚠️  IMPORTANT: You must edit .env and add your GEMINI_API_KEY!")
    print("  Get your API key from: https://makersuite.google.com/app/apikey")
else:
    print("  ✅ .env file exists")
    
    # Check if API key is configured
    with open('.env', 'r') as f:
        env_content = f.read()
    
    if 'your-gemini-api-key-here' in env_content or 'YOUR_API_KEY_HERE' in env_content:
        print("  ⚠️  WARNING: GEMINI_API_KEY not configured!")
        print("  Edit .env file and add your actual API key")
    elif 'GEMINI_API_KEY=' in env_content:
        # Check if there's a value after =
        for line in env_content.split('\n'):
            if line.startswith('GEMINI_API_KEY='):
                key = line.split('=', 1)[1].strip()
                if key and len(key) > 10:
                    print("  ✅ GEMINI_API_KEY appears to be configured")
                else:
                    print("  ⚠️  GEMINI_API_KEY looks empty or invalid")
    else:
        print("  ❌ GEMINI_API_KEY not found in .env")

# Step 6: Test imports
print("\nStep 6: Testing Python imports...")
packages = [
    ('flask', 'Flask'),
    ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
    ('dotenv', 'python-dotenv'),
    ('google.generativeai', 'google-generativeai'),
    ('PyPDF2', 'PyPDF2'),
]

missing_packages = []
for package, name in packages:
    try:
        __import__(package)
        print(f"  ✅ {name}")
    except ImportError:
        print(f"  ❌ {name} - NOT INSTALLED")
        missing_packages.append(name)

if missing_packages:
    print(f"\n  ❌ {len(missing_packages)} package(s) not installed!")
    print("\n  To fix, run:")
    print("  pip install -r requirements.txt")
    print("\n  Or install individually:")
    for pkg in missing_packages:
        print(f"  pip install {pkg}")

# Step 7: Database check
print("\nStep 7: Checking database...")
if os.path.exists('instance/notemaster.db'):
    size = os.path.getsize('instance/notemaster.db')
    print(f"  ✅ Database exists ({size} bytes)")
else:
    print("  ℹ️  Database doesn't exist yet (will be created on first run)")

# Summary
print("\n" + "=" * 70)
print("📋 SUMMARY")
print("=" * 70)

if missing_files:
    print("\n❌ CRITICAL: Missing files - cannot run")
    print("   Please download all project files")
elif missing_packages:
    print("\n⚠️  Missing Python packages")
    print("   Run: pip install -r requirements.txt")
elif 'your-gemini-api-key-here' in env_content or not os.path.exists('.env'):
    print("\n⚠️  .env file needs configuration")
    print("   1. Edit .env file")
    print("   2. Add your GEMINI_API_KEY")
    print("   3. Get key from: https://makersuite.google.com/app/apikey")
else:
    print("\n✅ Setup looks good!")
    print("\n   Next steps:")
    print("   1. Run: python app.py")
    print("   2. Open browser: http://127.0.0.1:5000")
    print("   3. If issues persist, press F12 in browser and check console")

print("\n" + "=" * 70)
print("\n💡 For detailed troubleshooting, see:")
print("   - DEBUGGING_GUIDE.md")
print("   - FUNCTIONALITY_TROUBLESHOOTING.md")
print("   - SETUP_TUTORIAL.md")
print("\n" + "=" * 70)
