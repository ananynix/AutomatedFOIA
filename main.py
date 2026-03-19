# main.py
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from contextlib import asynccontextmanager
import sqlite3
import os
import asyncio
from datetime import datetime, timedelta
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel
from dotenv import load_dotenv

# --- IMPORT OUR NEW MODULES ---
from frontend import html_content
from database import setup_clipboard
from backroom import alarm_clock_robot, read_heavy_document

# Setup & Configuration
load_dotenv(override=True) # Loads your AES_SECRET_KEY from .env
os.makedirs("inbox", exist_ok=True)
setup_clipboard()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(alarm_clock_robot())
    yield
    task.cancel()

boss_robot = FastAPI(title="FOIA Boss Robot", lifespan=lifespan)

# --- SECURITY PROTOCOLS ---
class LoginData(BaseModel):
    username: str
    password: str

@boss_robot.post("/login")
def authenticate_user(credentials: LoginData):
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (credentials.username, credentials.password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"success": True, "role": result[0]}
    return {"success": False, "error": "Invalid credentials. Access Denied."}


# --- ROUTES ---
@boss_robot.get("/", response_class=HTMLResponse)
def build_front_desk():
    return html_content

@boss_robot.post("/submit-request")
def receive_form(agency: str, topic: str):
    deadline = (datetime.now() + timedelta(seconds=10)).isoformat()
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO requests (agency, topic, status, extracted_text, due_date, filepath) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (agency, topic, "SUBMITTED - Waiting for reply", "", deadline, None))
    conn.commit()
    tracking_number = cursor.lastrowid 
    conn.close()
    return {"message": "Request sent!", "tracking_number": tracking_number, "due_date": deadline}

@boss_robot.get("/check-status/{tracking_number}")
def check_clipboard(tracking_number: int):
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT agency, topic, status, extracted_text, summary FROM requests WHERE id = ?", (tracking_number,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "agency": result[0], 
            "topic": result[1], 
            "status": result[2], 
            "summary": result[4], 
            "full_document_text": result[3]
        }
    return {"error": "Hmm, I don't have a record of that number."}

@boss_robot.get("/all-requests")
def get_all_requests():
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, agency, topic, status, due_date FROM requests")
    rows = cursor.fetchall()
    conn.close()
    
    requests_list = [{"tracking_number": r[0], "agency": r[1], "topic": r[2], "status": r[3], "due_date": r[4]} for r in rows]
    return requests_list

# --- SECURE UPLOAD / DOWNLOAD ---
@boss_robot.post("/upload-response/{tracking_number}")
def upload_document(tracking_number: int, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    filepath = f"inbox/{file.filename}.enc" # Add .enc extension
    raw_pdf_bytes = file.file.read()
    
    # AES-256 GCM ENCRYPTION
    key = base64.urlsafe_b64decode(os.getenv("AES_SECRET_KEY"))
    aesgcm = AESGCM(key)
    nonce = os.urandom(12) # 12-byte unique cryptographic salt
    encrypted_data = aesgcm.encrypt(nonce, raw_pdf_bytes, None)
    
    # Write the securely encrypted payload to the disk
    with open(filepath, "wb") as buffer:
        buffer.write(nonce + encrypted_data)

    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = ?, filepath = ? WHERE id = ?", 
                   ("PROCESSING - Decrypting and Reading...", filepath, tracking_number))
    conn.commit()
    conn.close()

    background_tasks.add_task(read_heavy_document, tracking_number, filepath)
    return {"message": "Data secured. Backroom is decrypting for AI analysis."}

@boss_robot.get("/download/{tracking_number}")
def download_document(tracking_number: int):
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT filepath FROM requests WHERE id = ?", (tracking_number,))
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0] and os.path.exists(result[0]):
        # Read the encrypted data
        with open(result[0], "rb") as f:
            encrypted_payload = f.read()
            
        # AES-256 GCM DECRYPTION
        key = base64.urlsafe_b64decode(os.getenv("AES_SECRET_KEY"))
        aesgcm = AESGCM(key)
        nonce = encrypted_payload[:12] # Extract the salt
        ciphertext = encrypted_payload[12:]
        decrypted_pdf = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Save it to a temporary unencrypted file to send back
        temp_path = "inbox/temp_download.pdf"
        with open(temp_path, "wb") as temp:
            temp.write(decrypted_pdf)
            
        return FileResponse(path=temp_path, filename="DECRYPTED_DATABLOCK.pdf", media_type='application/pdf')
    
    return {"error": "File not found or corrupted."}