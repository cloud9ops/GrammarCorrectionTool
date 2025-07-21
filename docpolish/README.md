# Real-Time Grammar Correction Keylogger & Document Polishing Tool

## Overview

This project offers a two-fold solution for grammar correction and polishing:

1. **Real-time Keylogger with Grammar Feedback**:
   A desktop GUI application that listens to user keystrokes, buffers complete sentences, performs grammar checking and polishing using AI and rule-based models, and displays polished output live. Original sentences are logged for record-keeping.

2. **Document Grammar Correction Web Service**:
   A Flask-based web app that accepts `.docx` files, processes each paragraph for grammar issues, highlights differences, and returns a polished corrected document for download.

---

## File Structure

```
project-root/
├── app.py                  # Flask web app to upload, process, and download corrected DOCX files
├── checker.py              # Document processing logic, grammar correction, and highlighting
├── keylogging.py           # Real-time keylogger GUI with live grammar polishing
├── text_polish.py          # Text polishing engine using language_tool and transformer models
├── uploads/                # Directory to store uploaded files temporarily (created at runtime)
├── templates/
│   └── index.html          # HTML template for the Flask upload form
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Components

### Text Polishing Module (`text_polish.py`)

* Utilizes `language_tool_python` for rule-based grammar checks.
* Applies transformer-based correction using the pretrained model `prithivida/grammar_error_correcter_v1`.
* Splits text into sentences and processes each individually.
* Returns polished text with detailed grammar issues and token counts.

### Real-Time Keylogger (`keylogging.py`)

* Listens to keyboard input via `pynput`.
* Buffers input and extracts complete sentences based on punctuation.
* Sends sentences to the polishing module for correction.
* Displays original and polished sentences live in a Tkinter GUI.
* Logs original sentences to a hidden file (`~/.corporate_keylog.txt`).
* Provides Start/Stop controls for keylogging and log management.

### Document Polishing Web App (`app.py` & `checker.py`)

* Flask web application with a simple upload interface.
* Accepts `.docx` files and processes paragraphs using `language_tool_python`.
* Highlights corrected words in the new document and appends suggestions.
* Returns polished `.docx` files for download.
* Temporarily stores files in an `uploads/` directory and cleans up after processing.

---

## Usage

### Running the Keylogger GUI
1. install the dependencies
2. Run the keylogger:

```bash
python keylogging.py
```

3. Use the GUI to start and stop grammar-aware keylogging.

### Running the Flask Web Service

1. Install dependencies.
2. Run the server:

```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`.
4. Upload a `.docx` file to receive a grammar-polished version.

---

## Dependencies

Key Python packages include:

* `language_tool_python`
* `transformers`
* `pynput`
* `tkinter` (usually included in standard Python installations)
* `flask`
* `python-docx`
* `werkzeug`

---

## Notes

* Ensure the transformer model weights are downloaded correctly; internet access is required for the first run.
* The keylogger is designed for desktop environments with GUI support.
* The web app expects well-formed `.docx` files for paragraph-wise processing.


