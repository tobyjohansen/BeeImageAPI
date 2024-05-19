from fastapi import FastAPI,File, UploadFile
from ultralytics import YOLO
from fastapi.responses import JSONResponse
import io
import numpy as np
from PIL import Image
import shutil
import os
import uvicorn

app = FastAPI()

# Load Yolov8 model
model = YOLO('mlmodel/best.pt')

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

def allowed_image(filename):
    AllowedExtensions = {'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in AllowedExtensions


@app.post("/V1/images/uploadsingle/")
async def upload_image_single(file: UploadFile = File(...)):
    # Check file extension
    if not allowed_image(file.filename):
        return {"error": "Only image files (jpg, jpeg) are allowed"}

    # Define the directory where you want to save images
    directory = "images"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save image file
    with open(os.path.join("images", file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return Json response
    return {"filename": file.filename, "detection": True, "count": 3}

# POST /upload/?user_id=123
@app.post("/V1/images/upload/")
async def upload_image(user_id: str, file: UploadFile = File(...)):
    # Check file extension
    if not allowed_image(file.filename):
        return {"error": "Only image files (jpg, jpeg) are allowed"}

    # Define the directory where you want to save images
    directory = "images"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save image file
    with open(os.path.join("images", file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return Json response
    return {"UserID": user_id, "filename": file.filename, "detection": True, "count": 3}

@app.post("/V1/images/cameraupload/")
async def upload_image(user_id: str, camera_id: str, file: UploadFile = File(...)):
    # Check file extension
    if not allowed_image(file.filename):
        return {"error": "Only image files (jpg, jpeg) are allowed"}

    # Define the directory where you want to save images
    directory = "images"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save image file
    with open(os.path.join("images", file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return Json response
    return {"UserID": user_id, "filename": file.filename, "camera_id": camera_id, "detection": True, "count": 3}

@app.post("/V1/images/uploadML/")
async def upload_image(user_id: str, file: UploadFile = File(...)):
    # Read image file
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    # Convert to numpy array
    image_np = np.array(image)

    # Perform prediction
    results = model.predict(source=image_np)

    count = 0
    # Process results
    for result in results:
        count +=1

    # Return Json response
    return {"UserID": user_id, "filename": file.filename, "detection": True, "count": count}

@app.post("/V1/images/uploadML2/")
async def upload_image(user_id: str, file: UploadFile = File(...)):
    # Check file extension
    if not allowed_image(file.filename):
        return {"error": "Only image files (jpg, jpeg) are allowed"}

    # Define the directory where you want to save images
    directory = "images"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save image file
    file_path = os.path.join("images", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model(file_path)

    count = 0
    # Process results
    for result in results:
        for box in result.boxes:
            count += 1

    # Return Json response
    return {"UserID": user_id, "filename": file.filename, "detection": True, "count": count}

if __name__ == '__main__':
    uvicorn.run(app, port=8006, host="0.0.0.0")


