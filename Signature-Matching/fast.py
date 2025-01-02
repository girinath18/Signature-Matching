import argparse
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from signature import match
import shutil
import os
from io import BytesIO

# Match Threshold
THRESHOLD = 85

app = FastAPI()

def check_similarity(path1, path2):
    """
    Compare two signatures and return the similarity result.
    """
    try:
        result = match(path1=path1, path2=path2, show_image=False)  
        if result <= THRESHOLD:
            return {"status": "failure", "similarity": result}
        else:
            return {"status": "success", "similarity": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare-signatures/")
async def compare_signatures(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """
    API endpoint to compare two signature images.
    Accepts two image files via multipart/form-data.
    """
    # Create temporary file paths
    temp_file1 = "temp_signature1.jpg"
    temp_file2 = "temp_signature2.jpg"

    # Save file1 to a temporary file
    try:
        with open(temp_file1, "wb") as buffer:
            shutil.copyfileobj(file1.file, buffer)
        
        # Save file2 to a temporary file
        with open(temp_file2, "wb") as buffer:
            shutil.copyfileobj(file2.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error saving files")

    # Compare the two signature images
    result = check_similarity(temp_file1, temp_file2)

    # Remove temporary files after processing
    os.remove(temp_file1)
    os.remove(temp_file2)

    return JSONResponse(content=result)

# For testing purposes, run FastAPI with `uvicorn`
# Example: uvicorn main:app --reload
