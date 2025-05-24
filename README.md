
# AKRUM Encryption/Decryption Demo

This project contains a simple demo for file encryption and decryption using FastAPI and Streamlit.

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI backend:
```bash
uvicorn fastapi_server:app --reload
```

3. Run the Streamlit frontend:
```bash
streamlit run streamlit_ui.py
```

## Features
- Upload any file to encrypt using AKRUM's engine
- Generates encrypted file and key
- Decrypts using uploaded key + encrypted file
