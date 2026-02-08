import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print("=" * 70)
print("🔍 Checking Your Gemini API Key and Available Models")
print("=" * 70)

if not api_key:
    print("\n❌ ERROR: No API key found!")
    print("Make sure you have a .env file with:")
    print("GEMINI_API_KEY=your-actual-key")
    exit(1)

print(f"\n✅ API Key found: {api_key[:15]}...{api_key[-8:]}")
print(f"   Length: {len(api_key)} characters")

# Check if key format looks correct
if not api_key.startswith('AIzaSy'):
    print("\n⚠️  WARNING: API key doesn't start with 'AIzaSy'")
    print("   Google API keys typically start with 'AIzaSy'")
    print("   Are you sure this is the correct key?")

print("\n" + "=" * 70)
print("Attempting to connect to Gemini API...")
print("=" * 70)

try:
    genai.configure(api_key=api_key)
    print("✅ API key accepted by Google")
    
    print("\n📋 Listing available models...")
    print("-" * 70)
    
    models = list(genai.list_models())
    
    if not models:
        print("⚠️  No models returned (but API key is valid)")
        print("This might be a temporary API issue. Try again in a few minutes.")
    else:
        print(f"\n✅ Found {len(models)} models:\n")
        
        generate_content_models = []
        
        for m in models:
            model_name = m.name.replace('models/', '')
            methods = ', '.join(m.supported_generation_methods)
            
            if 'generateContent' in m.supported_generation_methods:
                generate_content_models.append(model_name)
                print(f"  ✅ {model_name}")
                print(f"     Methods: {methods}")
            else:
                print(f"  ⚠️  {model_name} (doesn't support generateContent)")
                print(f"     Methods: {methods}")
            print()
        
        if generate_content_models:
            print("=" * 70)
            print("🎯 RECOMMENDED MODELS FOR YOUR APP:")
            print("=" * 70)
            for model in generate_content_models:
                print(f"  • {model}")
            
            print("\n" + "=" * 70)
            print("✅ UPDATE YOUR config.py:")
            print("=" * 70)
            print(f"\nUse one of these in config.py:\n")
            for model in generate_content_models[:3]:  # Show top 3
                print(f"  GEMINI_MODEL = '{model}'")
            print("\nPick the one that looks most like 'flash' or 'pro'")
        else:
            print("=" * 70)
            print("❌ NO MODELS SUPPORT generateContent!")
            print("=" * 70)
            print("\nThis means your API key might not have access to Gemini models.")
            print("Possible reasons:")
            print("1. API key is from wrong Google Cloud project")
            print("2. Gemini API not enabled for your project")
            print("3. API key doesn't have correct permissions")
            print("\n🔧 SOLUTION:")
            print("1. Go to: https://aistudio.google.com/app/apikey")
            print("2. Create a NEW API key")
            print("3. Make sure you select a project with Gemini API enabled")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\n" + "=" * 70)
    print("🔧 TROUBLESHOOTING:")
    print("=" * 70)
    
    error_str = str(e).lower()
    
    if '403' in error_str or 'permission' in error_str:
        print("\n❌ PERMISSION DENIED")
        print("Your API key doesn't have permission to access Gemini API")
        print("\nFix:")
        print("1. Go to: https://aistudio.google.com/app/apikey")
        print("2. Make sure Gemini API is enabled")
        print("3. Create a NEW API key")
        print("4. Update your .env file with the new key")
        
    elif '400' in error_str or 'invalid' in error_str:
        print("\n❌ INVALID API KEY")
        print("The API key format is incorrect or the key is invalid")
        print("\nFix:")
        print("1. Double-check you copied the ENTIRE key")
        print("2. Make sure there are no spaces or line breaks")
        print("3. Get a fresh key from: https://aistudio.google.com/app/apikey")
        
    elif '404' in error_str:
        print("\n❌ MODEL NOT FOUND")
        print("The API key is valid but can't find the model")
        print("\nThis script should have listed available models above.")
        print("If no models were listed, your API key might need proper setup.")
        
    else:
        print(f"\n❌ UNKNOWN ERROR: {e}")
        print("\nGeneral troubleshooting:")
        print("1. Check internet connection")
        print("2. Verify API key is correct (no typos)")
        print("3. Try creating a new API key")
        print("4. Visit: https://aistudio.google.com/app/apikey")

print("\n" + "=" * 70)