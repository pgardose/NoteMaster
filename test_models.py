import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print("=" * 60)
print("Testing Gemini API Key - UPDATED MODEL")
print("=" * 60)

if not api_key:
    print("❌ No API key found in .env file!")
    print("\nMake sure your .env file contains:")
    print("GEMINI_API_KEY=your-actual-key-here")
else:
    print(f"✅ API Key loaded: {api_key[:20]}...{api_key[-4:]}")
    
    # Try different models
    models_to_test = [
        'gemini-1.5-flash',
        'gemini-pro',
        'gemini-1.5-pro',
    ]
    
    for model_name in models_to_test:
        print(f"\n🔍 Testing model: {model_name}")
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello, I am working!'")
            
            print(f"  ✅ {model_name} WORKS!")
            print(f"  Response: {response.text[:50]}...")
            print(f"\n✅ Use this model in your config.py:")
            print(f"  GEMINI_MODEL = '{model_name}'")
            break  # Found a working model, stop testing
            
        except Exception as e:
            print(f"  ❌ {model_name} failed: {str(e)[:80]}...")
            continue
    else:
        print("\n❌ None of the models worked!")
        print("\nTry listing available models:")
        print("Run this Python code:")
        print("""
import google.generativeai as genai
genai.configure(api_key='your-key')
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
""")

print("=" * 60)