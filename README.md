# 🏛️ Automated FOIA Mailroom

A full-stack, asynchronous document processing engine built with **FastAPI**. This application simulates a Freedom of Information Act (FOIA) request pipeline, featuring a dual-role dashboard for Investigators and Government Agents, automated background OCR, and AI-powered document summarization.

---

## ✨ Key Features

* **Dual-Role Dashboard:** A modern, dark-mode, single-page UI allowing Investigators to submit requests and Government Agents to fulfill them via file upload.
* **Asynchronous Background Processing:** Heavy PDF parsing and OCR are handled in FastAPI `BackgroundTasks`, keeping the frontend UI lightning fast and responsive.
* **Intelligent OCR Fallback:** Uses `pdfplumber` for native digital text. If a scanned document is detected, it automatically falls back to a deep Optical Character Recognition pipeline using `poppler` and `tesseract`.
* **Cloud AI Summarization:** Integrates with the **Google Gemini API** to automatically read fulfilled documents and generate concise, 3-sentence executive summaries.
* **Automated Watchdog ("Alarm Clock Robot"):** An `asyncio` background loop that continuously monitors the SQLite database for overdue requests and updates their status automatically.

---

## 🛠️ Tech Stack

| Component | Technology |
| --- | --- |
| **Backend** | FastAPI, Python 3.12, Uvicorn |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3 (CSS Grid/Flexbox), Vanilla JS |
| **Document Pipeline** | pdfplumber, pdf2image, pytesseract |
| **AI Integration** | google-generativeai (Gemini 2.5 Flash) |
| **Environment** | python-dotenv |

---

## 🚀 Installation and Setup

Because this project uses system-level tools to process PDFs and extract text, there are a few system dependencies required before installing the Python packages.

### 1. System Dependencies (Windows)

To run the OCR pipeline, you must install **Poppler** (for PDF-to-Image) and **Tesseract** (for Image-to-Text).

* **Tesseract OCR:** 1. Download the Windows installer from [UB Mannheim](https://www.google.com/search?q=https://github.com/UB-Mannheim/tesseract/wiki).
2. Install it to the default directory: `C:\Program Files\Tesseract-OCR`.
* **Poppler:**
1. Download the latest Release .zip from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/).
2. Extract the folder to `C:\poppler` (or your preferred location).
3. **Crucial:** You must update the `poppler_path` inside `backroom.py` to point to the `\bin` folder of your extracted Poppler directory.



### 2. Python Environment Setup

Clone the repository and install the required Python libraries:

```bash
git clone https://github.com/YOUR_USERNAME/AutomatedFOIA.git
cd AutomatedFOIA
pip install fastapi uvicorn pdfplumber pdf2image pytesseract google-generativeai python-dotenv python-multipart

```

### 3. Environment Variables

This project uses the Google Gemini API for summarization. You will need a free API key from [Google AI Studio](https://aistudio.google.com/).

Create a file named `.env` in the root directory and add your API key:

```text
GEMINI_API_KEY=your_actual_api_key_here

```

---

## 💻 Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:boss_robot --reload

```

Once the server is running, open your browser and navigate to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

### 🔄 Usage Workflow

1. **Log in as an Investigator:** Submit a request for a specific agency and topic. You will receive a unique **Tracking Number**.
2. **Log in as the Government:** Refresh the incoming requests table. Enter the Tracking Number and upload a PDF document (scanned or digital).
3. **Check the Terminal:** Watch the backend dynamically route the document through the OCR pipeline and hand it to the Cloud AI.
4. **Check Status:** Return to the Investigator desk and enter the Tracking Number to read the newly generated AI summary.

---

## 📁 Project Structure

```bash
AutomatedFOIA/
├── main.py           # The Boss Robot: FastAPI routing, endpoints, and background tasks
├── frontend.py       # The UI: Contains the HTML/CSS/JS for the dashboard
├── database.py       # The Clipboard: SQLite database setup and schema
├── backroom.py       # The Workers: OCR pipeline, AI integration, and the Watchdog loop
├── .env              # Secure environment variables (Not tracked in Git)
├── .gitignore        # Git ignore rules
└── inbox/            # Temporary storage for uploaded PDFs during processing

```
