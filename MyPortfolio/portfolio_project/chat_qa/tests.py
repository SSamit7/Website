import google.generativeai as genai

API_KEY = "AIzaSyDsL0sMk8ZRMyo9GPhYl18QAcVXW_BBqV8"

try:
    genai.configure(api_key=API_KEY)
    
    print("=" * 60)
    print("🔍 DISCOVERING AVAILABLE MODELS")
    print("=" * 60)
    
    all_models = genai.list_models()
    
    print("📋 ALL MODELS:")
    for i, m in enumerate(all_models):
        methods = ", ".join(m.supported_generation_methods)
        print(f"{i+1:2d}. {m.name}")
        print(f"    Methods: {methods}")
        print(f"    Description: {m.description}")
        print()
    
    print("🎯 MODELS THAT SUPPORT generateContent:")
    working_models = []
    for m in all_models:
        if 'generateContent' in m.supported_generation_methods:
            working_models.append(m.name)
            print(f"  ✅ {m.name}")
    
    print(f"\n📊 Summary: {len(working_models)} models support generateContent")
    
    # Test the first working model
    if working_models:
        test_model = working_models[0]
        print(f"\n🧪 Testing model: {test_model}")
        try:
            model = genai.GenerativeModel(test_model)
            response = model.generate_content("Say 'SUCCESS' in one word")
            print(f"✅ Test successful: {response.text}")
        except Exception as e:
            print(f"❌ Test failed: {e}")
    else:
        print("❌ No working models found!")
        
except Exception as e:
    print(f"❌ Configuration error: {e}")