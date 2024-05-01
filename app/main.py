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

# POST /upload/?user_id=123
@app.post("/V1/images/upload/")
async def upload_image(user_id: int, file: UploadFile = File(...)):
    # Check file extension
    if not allowed_image(file.filename):
        return {"error": "Only image files (jpg, jpeg) are allowed"}

    # Save image file
    with open(os.path.join("images", file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return Json response
    return {"UserID": user_id, "filename": file.filename}

if __name__ == '__main__':
    uvicorn.run(app, port=8006, host="0.0.0.0")


