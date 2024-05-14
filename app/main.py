from fastapi import FastAPI,File, UploadFile
import shutil
import os
import uvicorn

app = FastAPI()


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

if __name__ == '__main__':
    uvicorn.run(app, port=8006, host="0.0.0.0")


