import os
import uuid
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
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

TEMP_DIR = "/tmp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "AKRUM backend is live."}

@app.get("/upload", response_class=HTMLResponse)
async def upload_form():
    return """
    <html>
        <body>
            <h2>Upload a file to encrypt:</h2>
            <form action="/encrypt" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """

@app.post("/encrypt")
async def encrypt(file: UploadFile = File(...)):
    try:
        input_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
        encrypted_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_encrypted.bin")
        key_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_key.txt")

        contents = await file.read()
        with open(input_filename, "wb") as f:
            f.write(contents)

        seed = "110010101011"
        key_stream = rule30_ca_key_stream(seed, len(contents))

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
