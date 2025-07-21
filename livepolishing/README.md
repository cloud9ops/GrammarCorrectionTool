
# Flask-Based Grammar Polishing Web App

This project provides a web interface for automatic grammar correction using the **Gramformer** library created by [Prithiviraj Damodaran (Prithivida)](https://github.com/PrithivirajDamodaran). It uses transformer-based models to detect and correct grammar in real-time.

---

## Features

* Accepts user text input through an HTML form.
* Provides two modes: full-text correction and sentence-by-sentence streaming.
* Returns corrected text using Flask routes.
* Real-time output with Server-Sent Events (SSE).
* REST API endpoint for external calls.

---

## Project Structure

```
project/
│
├── app.py                  # Flask server setup and route logic
├── text_polish.py          # Grammar correction logic using Gramformer
├── templates/
│   └── index.html          # Web interface for text input
```

---

## Routes Overview

### `/` — Home Page

Renders the HTML form where the user can input text for correction.

### `/stream` — SSE Streaming Endpoint

Streams corrected sentences back to the client one-by-one:

```python
@app.route('/stream', methods=['POST'])
def stream():
    ...
```

### `/auto-polish` — Single Sentence Correction API

Receives a JSON request with a sentence and returns a polished version:

```python
@app.route('/auto-polish', methods=['POST'])
def auto_polish():
    ...
```

---

## Backend Engine: `text_polish.py`

This script interfaces with **Gramformer** to apply grammar correction.

### Used Model

* `prithivida/grammar_error_correcter_v1`
  A transformer model based on **BART**, fine-tuned for grammar correction tasks.
  Provided as part of the Gramformer library by Prithivida.

### Core Functions

* `polish_full_text(text: str)`
  Returns a fully polished version of the input text.

* `stream_polish_sentences(text: str)`
  Generator that yields corrected sentences one at a time for streaming.

---

## Setup Instructions

### Dependencies

* Python 3.8+
* Flask
* Gramformer
* Transformers (HuggingFace)

### Installation

```bash
pip install flask git+https://github.com/PrithivirajDamodaran/Gramformer.git
```

---

## Credits

* Gramformer by [Prithivida](https://github.com/PrithivirajDamodaran)
* Model used: `prithivida/grammar_error_correcter_v1`
  (Available via HuggingFace Transformers)


