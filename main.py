import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from services import FrameExtractorService
import tempfile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
frame_service = FrameExtractorService()

@app.post("/extract-frames")
async def extract_frames(video_file: UploadFile = File(...), frame_interval: int = 30):
    if frame_interval <= 0:
        raise HTTPException(status_code=400, detail="Frame interval must be a positive integer")
    
    try:
        # Geçici bir dosya yolu oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
            video_path = temp_video_file.name
            # Yüklenen dosyayı geçici dosyaya yaz
            with open(video_path, "wb") as buffer:  
                shutil.copyfileobj(video_file.file, buffer)
        
        # Frame'leri çıkar
        frames_dir = frame_service.extract_frames(video_path, frame_interval)
        return {"message": "Frames extracted successfully", "frames_directory": frames_dir}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CORS Middleware ekleyin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Frontend'in çalıştığı URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)