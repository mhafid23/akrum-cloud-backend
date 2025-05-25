
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import base64
import shutil

from akrum_ca_engine import encrypt_file, decrypt_file

# Ensure 'temp' directory exists
os.makedirs("temp", exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/encrypt")
async def encrypt(uploaded_file: UploadFile = File(...)):
    try:
        contents = await uploaded_file.read()
        input_path = os.path.join("temp", uploaded_file.filename)
        with open(input_path, "wb") as f:
            f.write(contents)

        encrypted_path, key_path = encrypt_file(input_path)

        return JSONResponse({
            "encrypted_file": encrypted_path,
            "key_file": key_path
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/decrypt")
async def decrypt(file: UploadFile = File(...), key: UploadFile = File(...)):
    try:
        encrypted_path = os.path.join("temp", file.filename)
        key_path = os.path.join("temp", key.filename)

        with open(encrypted_path, "wb") as f:
            f.write(await file.read())

        with open(key_path, "wb") as f:
            f.write(await key.read())

        original_path = decrypt_file(encrypted_path, key_path)

        return JSONResponse({
            "original_file": original_path
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
