# AKRUM Cloud Backend

This backend supports AKRUM's browser-based encryption and decryption interface.

## Features
- FastAPI-based backend to handle encryption and decryption requests
- Cellular Automata entropy engine for key generation
- Supports large file uploads (adjustable with cloud hosting limits)

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn fastapi_server:app --reload
   ```

4. Launch the Streamlit UI:
   ```bash
   streamlit run streamlit_ui.py
   ```
