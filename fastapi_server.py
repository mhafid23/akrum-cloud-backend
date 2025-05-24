
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from akrum_ca_engine import encrypt_file, decrypt_file

app = FastAPI()

@app.post("/encrypt/")
async def encrypt(uploaded_file: UploadFile = File(...)):
    input_path = f"temp/{uploaded_file.filename}"
    encrypted_path = f"temp/encrypted_{uploaded_file.filename}"
    key_path = f"temp/key_{uploaded_file.filename}.txt"

    with open(input_path, "wb") as f:
        f.write(await uploaded_file.read())

    encrypt_file(input_path, encrypted_path, key_path)
    return {"encrypted_file": encrypted_path, "key_file": key_path}

@app.post("/decrypt/")
async def decrypt(uploaded_file: UploadFile = File(...), key_file: UploadFile = File(...)):
    input_path = f"temp/{uploaded_file.filename}"
    key_path = f"temp/key_{uploaded_file.filename}.txt"
    decrypted_path = f"temp/decrypted_{uploaded_file.filename}"

    with open(input_path, "wb") as f:
        f.write(await uploaded_file.read())
    with open(key_path, "wb") as f:
        f.write(await key_file.read())

    decrypt_file(input_path, decrypted_path, key_path)
    return FileResponse(decrypted_path)
