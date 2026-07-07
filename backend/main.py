from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64
import numpy as np
from PIL import Image as PILImage
from modules.classifier import SkinDiseaseClassifier
from utils.data_loader import MedicalDataLinker


app = FastAPI(title="Skin Scanning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("AI 모델 및 데이터 베이스 로딩 중...")
classifier = SkinDiseaseClassifier()
linker = MedicalDataLinker()
print("로딩 완료!")

@app.post("/api/predict")
async def predict_skin_disease(file: UploadFile = File(...)):
    
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    
    pred_idx, cam_image = classifier.predict_and_explain(image)
    
    categories = ["진균_감염", "세균_감염", "피부염_습진"]
    predicted_category = categories[pred_idx % 3]
    
    disease_name, mma_data, dapa_data = linker.get_info_by_diagnosis(predicted_category)
    
    cam_pil = PILImage.fromarray(cam_image)
    buffered = io.BytesIO()
    cam_pil.save(buffered, format="JPEG")
    cam_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return {
        "status": "success",
        "result": {
            "disease_category": predicted_category,
            "disease_name": disease_name,
            "heatmap_image_base64": cam_base64, 
            "mma_data": mma_data,
            "dapa_data": dapa_data
        }
    }

@app.get("/")
def read_root():
    return {"message": "Skin Scanning API Server is running!"}