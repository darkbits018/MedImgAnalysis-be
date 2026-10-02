import os
from google import genai
from google.genai import types
from app.core.config import settings

# Initialize the Gemini client
# Note: Ensure GEMINI_API_KEY is set in your .env file
client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None

def upload_file_to_gemini(file_path: str, mime_type: str):
    """Uploads a file to Gemini File API and returns the File URI."""
    if not client:
        raise ValueError("Gemini API key is not configured.")
        
    try:
        uploaded_file = client.files.upload(path=file_path, config={'mime_type': mime_type})
        return uploaded_file.name
    except Exception as e:
        print(f"Error uploading to Gemini: {e}")
        raise e

def ask_medical_question(message: str, file_uri: str = None, history: list = None) -> str:
    """Sends a question and optional file URI to the Gemini model."""
    if not client:
        raise ValueError("Gemini API key is not configured.")
    
    # Using a capable stable model version for the MVP
    model_name = "gemini-3.5-flash-lite" 
    
    system_instruction = (
        "You are an AI assistant helping to explain medical reports or images to a patient. "
        "If the user provides an image that is NOT medical (like a screenshot), describe what you see in the image to prove you received it, but remind them you need a medical report. "
        "CRITICAL RULE: You must always include a disclaimer that you are an AI and this is "
        "for educational purposes only, not a clinical diagnosis."
    )
    
    contents = []
    if history:
        for msg in history:
            role = 'user' if msg.role == 'user' else 'model'
            contents.append(types.Content(role=role, parts=[types.Part.from_text(msg.text)]))
            
    current_parts = [types.Part.from_text(message)]
    if file_uri:
        try:
            file_obj = client.files.get(name=file_uri)
            current_parts.append(types.Part.from_uri(file_uri=file_obj.uri, mime_type=file_obj.mime_type))
        except Exception as e:
            print(f"Failed to fetch file from Gemini: {e}")
            raise e
            
    contents.append(types.Content(role="user", parts=current_parts))

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise e
