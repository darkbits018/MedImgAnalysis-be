import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.gemini import upload_file_to_gemini

router = APIRouter()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    try:
        # Create a temporary file to save the uploaded content before sending to Gemini
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
            
        # Upload to Gemini File API
        file_uri = upload_file_to_gemini(temp_file_path, file.content_type)
        
        # Clean up the temporary file locally
        os.remove(temp_file_path)
        
        return {
            "filename": file.filename, 
            "file_uri": file_uri, 
            "message": "File uploaded successfully to AI backend."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
