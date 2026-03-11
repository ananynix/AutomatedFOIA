# backroom.py
import os
from dotenv import load_dotenv
import sqlite3
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import google.generativeai as genai
import asyncio
from datetime import datetime

# --- CONFIGURATION ---
# This line unlocks the safe (reads the .env file)
load_dotenv()

# This line grabs the specific key out of the safe
my_secret_key = os.getenv("GEMINI_API_KEY")

# Now we pass the key to the AI!
genai.configure(api_key=my_secret_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Point it exactly to the Tesseract tool
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- THE ALARM CLOCK ROBOT ---
async def alarm_clock_robot():
    while True:
        await asyncio.sleep(5) 
        conn = sqlite3.connect("clipboard.db")
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute("""
            SELECT id, agency FROM requests 
            WHERE status = 'SUBMITTED - Waiting for reply' AND due_date < ?
        """, (now,))
        
        late_requests = cursor.fetchall()
        
        for request in late_requests:
            tracking_number = request[0]
            agency = request[1]
            print(f"🚨 ALARM CLOCK ROBOT: {agency} is late on Request {tracking_number}! Sending angry email...")
            cursor.execute("UPDATE requests SET status = ? WHERE id = ?", 
                           ("OVERDUE - Nagging the Agency!", tracking_number))
            conn.commit()
        conn.close()

# --- THE BACKROOM READERS ---
def read_heavy_document(tracking_number: int, filepath: str):
    print(f"Backroom Reader: Opening {filepath}...")
    full_text = ""
    
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        
        if full_text.strip() == "":
            print("Backroom Reader: Magic glasses failed! Putting on the OCR Super Decoder Ring...")
            images = convert_from_path(filepath, poppler_path=r"C:\Users\Aradhy Srivastava\poppler-25.12.0\Library\bin")
            for img in images:
                full_text += pytesseract.image_to_string(img) + "\n"

        status_update = "COMPLETED - Document Parsed successfully!"
    
    except Exception as e:
        status_update = "ERROR - Could not read the document."
        full_text = str(e)
        print(f"Backroom Reader Error: {e}")

    # The AI Summarizer
    ai_summary = "No text to summarize."
    if full_text.strip() != "":
        print("Backroom Reader: Handing text to the Cloud AI for summarization...")
        try:
            prompt = f"Please provide a concise, 3-sentence summary of this government document:\n\n{full_text[:5000]}"
            response = model.generate_content(prompt)
            ai_summary = response.text
            print("Backroom Reader: Cloud AI Summary complete!")
        except Exception as e:
            ai_summary = "Cloud AI got confused: " + str(e)
            print(f"AI Error: {e}")

    # Update Clipboard
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = ?, extracted_text = ?, summary = ? WHERE id = ?", 
                   (status_update, full_text, ai_summary, tracking_number))
    conn.commit()
    conn.close()
    print(f"Backroom Reader: Finished request {tracking_number}!")