import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print("=" * 60)
print("Testing Gemini API Key")
print("=" * 60)

if not api_key:
    print("❌ No API key found in .env file!")
    print("\nMake sure your .env file contains:")
    print("GEMINI_API_KEY=your-actual-key-here")
else:
    print(f"✅ API Key loaded: {api_key[:20]}...{api_key[-4:]}")
    
    # Try to use it
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content("Say 'Hello, I am working!'")
        
        print("\n✅ API Key is VALID!")
        print(f"\nTest Response: {response.text}")
        print("\n✅ Everything is working! You can now use the app.")
        
    except Exception as e:
        print(f"\n❌ API Key ERROR: {str(e)}")
        print("\nPossible issues:")
        print("1. API key is invalid or expired")
        print("2. API key doesn't have access to Gemini models")
        print("3. Get a new key from: https://aistudio.google.com/app/apikey")

print("=" * 60)