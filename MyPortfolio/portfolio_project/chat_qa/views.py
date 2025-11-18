import os
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a valid model name from list_models()
model = genai.GenerativeModel("models/gemini-2.0-flash")

@require_POST
@csrf_exempt
def ask_question(request):
    question = request.POST.get("question", "").strip()
    if not question:
        return JsonResponse({"response": "Please ask a valid question."}, status=400)

    try:
        system_prompt = os.getenv(
            "SYSTEM_PROMPT",
            "You are an AI assistant for a portfolio website. Respond professionally.",
        )
        response = model.generate_content(f"{system_prompt}\n\nUser question: {question}")
        answer = response.text if response else "I could not generate a response."
        return JsonResponse({"response": answer})
    except Exception as e:
        return JsonResponse({"response": f"Error: {str(e)}"}, status=500)
