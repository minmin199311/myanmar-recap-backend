from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import requests

app = FastAPI()

# Groq API Key (Render environment variables သို့မဟုတ် တိုက်ရိုက်ထည့်ရန်)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your_groq_api_key_here")

@app.get("/")
def home():
    return {"status": "running", "message": "Myanmar Movie Recap Backend with Groq API is live!"}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    try:
        # တင်လိုက်သော အသံဖိုင်ကို ယာယီသိမ်းဆည်းခြင်း
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Groq Audio Transcription API သို့ ပို့ဆောင်ခြင်း
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        
        with open(temp_file_path, "rb") as audio_file:
            files = {
                "file": (file.filename, audio_file, file.content_type)
            }
            data = {
                "model": "whisper-large-v3"
            }
            response = requests.post(url, headers=headers, files=files, data=data)
        
        # ယာယီဖိုင်ကို ပြန်ဖျက်ခြင်း
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=response.text)
            
        result = response.json()
        return {
            "status": "success",
            "filename": file.filename,
            "transcription": result.get("text", ""),
            "message": "Successfully transcribed using Groq Whisper API!"
        }
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"status": "error", "message": str(e)}
