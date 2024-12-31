from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import cv2
import numpy as np
from signature import match  # Assuming match function is available

# Match Threshold
THRESHOLD = 85

app = FastAPI()

def check_similarity(path1: str, path2: str):
    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        return JSONResponse(
            status_code=400,
            content={"message": f"Signatures are {result}% similar. Signatures do not match."},
        )
    else:
        return JSONResponse(
            status_code=200,
            content={"message": f"Signatures are {result}% similar. Signatures match."},
        )


@app.post("/compare_signatures/")
async def compare_signatures(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        # Save the uploaded images temporarily
        file1_path = f"./temp/{file1.filename}"
        file2_path = f"./temp/{file2.filename}"

        # Ensure temp directory exists
        if not os.path.exists("./temp"):
            os.makedirs("./temp")

        with open(file1_path, "wb") as f1:
            f1.write(await file1.read())

        with open(file2_path, "wb") as f2:
            f2.write(await file2.read())

        # Check similarity between the two uploaded files
        return check_similarity(file1_path, file2_path)

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"An error occurred: {str(e)}"})


# Test endpoint for file browsing (to test the match functionality)
@app.get("/test/")
async def test():
    return {"message": "Upload two images via POST /upload_signature to compare them."}
