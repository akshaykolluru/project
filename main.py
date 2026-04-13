from fastapi import FastAPI, UploadFile, File
from google import genai
import os

app = FastAPI()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    
    # Using Gemini to convert image to a searchable product string
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}},
            "Identify this product. Return only the brand and model name."
        ]
    )
    product_name = response.text.strip()
    return {"product_name": product_name}