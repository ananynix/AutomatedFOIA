# backroom.py
import sqlite3
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv

# The brand new Google AI Library!
from google import genai

# --- CONFIGURATION ---
load_dotenv(override=True)
my_secret_key = os.getenv("GEMINI_API_KEY")

print(f"=== DEBUG: THE KEY IS: {my_secret_key} ===")

# Create the AI client with the key from your safe
client = genai.Client(api_key=my_secret_key)

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
            # We convert the PDF to images in the background just in case we need them
            print("Backroom Reader: Preparing document layers...")
            pdf_images = convert_from_path(filepath, poppler_path=r"C:\Users\Aradhy Srivastava\poppler-25.12.0\Library\bin")
            
            # Go through the document page by page
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                
                # THE MAGIC TRICK: Does this page have pictures? Or is it empty?
                if len(page.images) > 0 or text.strip() == "":
                    print(f"Backroom Reader: Found pictures on Page {i+1}! Using OCR Decoder Ring...")
                    # Run OCR on this specific page to capture BOTH the native text and the picture text
                    ocr_text = pytesseract.image_to_string(pdf_images[i])
                    full_text += ocr_text + "\n\n"
                else:
                    print(f"Backroom Reader: Page {i+1} is plain text. Reading normally...")
                    full_text += text + "\n\n"

        status_update = "COMPLETED - Document Parsed successfully!"
    
    except Exception as e:
        status_update = "ERROR - Could not read the document."
        full_text = str(e)
        print(f"Backroom Reader Error: {e}")

    # === NEW: THE CLOUD AI SUMMARIZER (v2 SDK) ===
    ai_summary = "No text to summarize."
    if full_text.strip() != "":
        print("Backroom Reader: Handing text to the Cloud AI for summarization...")
        try:
            prompt = f"Please provide a concise, 3-sentence summary of this government document:\n\n{full_text[:5000]}"
            
            # The NEW v2 syntax for generating content!
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            ai_summary = response.text
            print("Backroom Reader: Cloud AI Summary complete!")
        except Exception as e:
            ai_summary = f"Cloud AI got confused: {e}"
            print(f"AI Error: {e}")

    # Update Clipboard
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = ?, extracted_text = ?, summary = ? WHERE id = ?", 
                   (status_update, full_text, ai_summary, tracking_number))
    conn.commit()
    conn.close()
    print(f"Backroom Reader: Finished request {tracking_number}!")