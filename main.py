from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
import base64

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    image_bytes = await file.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}},
            "Identify this product. Return only the brand and model name."
        ]
    )

    product_name = response.text.strip()

    # Convert image to base64 to send to frontend
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return {
        "product_name": product_name,
        "image": image_base64
    }
