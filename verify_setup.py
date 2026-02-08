#!/usr/bin/env python3
"""
File Structure Verification Script
Run this to check if your NoteMaster AI setup is correct
"""

import os
import sys

print("=" * 60)
print("🔍 NoteMaster AI - File Structure Verification")
print("=" * 60)
print()

required_files = {
    'Python Files': [
        'app.py',
        'config.py',
        'models.py',
        'routes.py',
        'utils.py',
        'requirements.txt',
    ],
    'Template Files': [
        'templates/index.html',
    ],
    'Static Files': [
        'static/js/script.js',
    ],
    'Config Files': [
        '.env',
        '.gitignore',
    ],
}

all_good = True

for category, files in required_files.items():
    print(f"\n📁 {category}:")
    for file in files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        if not exists:
            all_good = False

print("\n" + "=" * 60)

# Check .env content
if os.path.exists('.env'):
    print("\n🔐 Checking .env file:")
    with open('.env', 'r') as f:
        content = f.read()
        
    if 'GEMINI_API_KEY' in content and 'your-gemini-api-key-here' not in content:
        print("  ✅ GEMINI_API_KEY is set")
    else:
        print("  ❌ GEMINI_API_KEY is missing or not configured")
        all_good = False
        
    if 'SECRET_KEY' in content and 'your-secret-key-here' not in content:
        print("  ✅ SECRET_KEY is set")
    else:
        print("  ⚠️  SECRET_KEY not configured (will use default)")
else:
    print("\n❌ .env file not found!")
    print("   Create .env file with:")
    print("   GEMINI_API_KEY=your-api-key")
    print("   SECRET_KEY=any-random-text")
    all_good = False

# Check instance folder
print("\n📂 Checking folders:")
if os.path.exists('instance'):
    print("  ✅ instance/ folder exists")
else:
    print("  ⚠️  instance/ folder missing (will be created automatically)")

if os.path.exists('templates'):
    print("  ✅ templates/ folder exists")
else:
    print("  ❌ templates/ folder missing!")
    all_good = False

if os.path.exists('static/js'):
    print("  ✅ static/js/ folder exists")
else:
    print("  ❌ static/js/ folder missing!")
    all_good = False

# Check Python packages
print("\n📦 Checking Python packages:")
try:
    import flask
    print("  ✅ Flask installed")
except ImportError:
    print("  ❌ Flask not installed")
    all_good = False

try:
    import flask_sqlalchemy
    print("  ✅ Flask-SQLAlchemy installed")
except ImportError:
    print("  ❌ Flask-SQLAlchemy not installed")
    all_good = False

try:
    import google.generativeai
    print("  ✅ google-generativeai installed")
except ImportError:
    print("  ❌ google-generativeai not installed")
    all_good = False

try:
    import PyPDF2
    print("  ✅ PyPDF2 installed")
except ImportError:
    print("  ❌ PyPDF2 not installed")
    all_good = False

try:
    import dotenv
    print("  ✅ python-dotenv installed")
except ImportError:
    print("  ❌ python-dotenv not installed")
    all_good = False

print("\n" + "=" * 60)

if all_good:
    print("\n✅ All checks passed! Your setup looks good.")
    print("\nNext steps:")
    print("1. Run: python app.py")
    print("2. Open: http://127.0.0.1:5000")
    print("3. If still not working, check browser console (F12)")
else:
    print("\n❌ Some issues found! Please fix the items marked with ❌")
    print("\nQuick fixes:")
    print("1. Install packages: pip install -r requirements.txt")
    print("2. Create .env file with your GEMINI_API_KEY")
    print("3. Make sure files are in correct folders")

print("=" * 60)
