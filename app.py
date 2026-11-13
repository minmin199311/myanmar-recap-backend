from fastapi import FastAPI, UploadFile, File
import whisper
import shutil
import os

app = FastAPI()

# Whisper မော်ဒယ်ကို တင်ခြင်း (cpu သို့မဟုတ် device အလိုက်)
model = whisper.load_model("base")

@app.get("/")
def home():
    return {"status": "running", "message": "Myanmar Movie Recap Backend is live!"}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # တင်လိုက်သော အသံဖိုင်ကို ယာယီသိမ်းဆည်းခြင်း
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Whisper ဖြင့် စာသားပြောင်းခြင်း (မြန်မာဘာသာ သို့မဟုတ် ဘာသာပြန်ရန်)
        result = model.transcribe(temp_file_path)
        extracted_text = result["text"]
        
        # ယာယီဖိုင်ကို ပြန်ဖျက်ခြင်း
        os.remove(temp_file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "transcription": extracted_text,
            "message": "Successfully transcribed using Local Whisper!"
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"status": "error", "message": str(e)}
