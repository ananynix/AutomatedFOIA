# main.py
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from contextlib import asynccontextmanager
import sqlite3
import os
import asyncio
from datetime import datetime, timedelta

# --- IMPORT OUR NEW MODULES ---
from frontend import html_content
from database import setup_clipboard
from backroom import alarm_clock_robot, read_heavy_document

# Setup
os.makedirs("inbox", exist_ok=True)
setup_clipboard()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(alarm_clock_robot())
    yield
    task.cancel()

boss_robot = FastAPI(title="FOIA Boss Robot", lifespan=lifespan)

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

@boss_robot.post("/upload-response/{tracking_number}")
def upload_document(tracking_number: int, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    filepath = f"inbox/{file.filename}"
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    # Save the filepath to the database so we know where it is later!
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = ?, filepath = ? WHERE id = ?", 
                   ("PROCESSING - Backroom is reading the file", filepath, tracking_number))
    conn.commit()
    conn.close()

    background_tasks.add_task(read_heavy_document, tracking_number, filepath)
    return {"message": "Got it! The backroom is reading it."}

@boss_robot.get("/download/{tracking_number}")
def download_document(tracking_number: int):
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT filepath FROM requests WHERE id = ?", (tracking_number,))
    result = cursor.fetchone()
    conn.close()
    
    # If we found the path in the database, and the file actually exists in the folder...
    if result and result[0] and os.path.exists(result[0]):
        # Send the file to the user's browser!
        return FileResponse(path=result[0], filename=os.path.basename(result[0]), media_type='application/pdf')
    
    return {"error": "File not found on the server."}