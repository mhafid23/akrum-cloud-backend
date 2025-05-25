import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from akrum_ca_engine import rule30_ca_key_stream

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File directory for temporary storage
TEMP_DIR = "/tmp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/encrypt")
async def encrypt(file: UploadFile = File(...)):
    try:
        # Generate unique filenames
        input_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
        encrypted_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_encrypted.bin")
        key_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_key.txt")

        # Save uploaded file
        with open(input_filename, "wb") as f:
            contents = await file.read()
            f.write(contents)

        # Generate key stream based on Rule 30 CA
        seed = "110010101011"  # Example fixed seed
        key_stream = rule30_ca_key_stream(seed, len(contents))

        # XOR encryption
        encrypted = bytes([b ^ int(k) for b, k in zip(contents, key_stream)])
        with open(encrypted_filename, "wb") as ef:
            ef.write(encrypted)
        with open(key_filename, "w") as kf:
            kf.write(key_stream)

        return JSONResponse({
            "encrypted_file": encrypted_filename,
            "key_file": key_filename
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})