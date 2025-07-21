````
# ✨ Grammar Polishing Web App

A clean and efficient Flask-based application that corrects grammar, improves sentence structure, and adjusts verb tenses based on context — with a little NLP magic.

---

## 🧠 What It Does

This app takes a sentence from the user and:

1. ✂️ Optionally removes LaTeX formatting using **Pandoc**
2. ✅ Fixes grammar issues using **LanguageTool**
3. 🔁 Adjusts tense and part-of-speech (POS) consistency using **spaCy** + **lemminflect**
4. ✨ Returns a polished version with a detailed list of all corrections

---

## 🧩 Core Components

### `app.py` – The Web Server 🖥️

- ⚙️ Initializes a **Flask** app
- 🧽 `strip_latex(raw)` – Uses `pandoc` to convert LaTeX to plain text
- 🌐 Route `/`:
  - **GET**: Loads the input form (`index.html`)
  - **POST**: 
    - Gets user input
    - Optionally strips LaTeX
    - Passes the input to `polish_text()` from `text_processor.py`
    - Renders:
      - Original sentence  
      - Polished sentence  
      - All identified issues  

---

### `text_processor.py` – The NLP Engine 🔬

#### 🛠️ Libraries Used:
- `spaCy` (`en_core_web_trf`) – Deep syntax analysis
- `lemminflect` – Smart verb inflection
- `language_tool_python` – Grammar checker
- `re` – Regex for spacing cleanup

#### 📦 Functions:

- `clean_spacing(text)`  
  🔹 Removes extra spaces and cleans up punctuation

- `detect_temporal_context(text)`  
  🔹 Detects if the sentence is talking about the **past**, **present**, or **future**

- `analyze_pos_agreement(text)`  
  🔹 Fixes:
  - Subject-verb agreement (`He go → He goes`)
  - Modal + past tense (`could went → could go`)
  - Pronoun + "be" verb mismatches (`They is → They are`)
  - Tense mismatch (`Yesterday he go → Yesterday he went`)

- `polish_text(text)`  
  🧪 The full polishing pipeline:
  1. LanguageTool grammar fixes  
  2. POS & tense corrections  
  3. Spacing cleanup  
  4. Outputs:  
     - Original sentence  
     - Polished version  
     - List of all corrections (with metadata)

---

## 🔄 Workflow Diagram

```mermaid
graph TD
    A[User inputs sentence] --> B[Flask receives POST request]
    B --> C[Optional: Strip LaTeX via Pandoc]
    C --> D[Polish Text using text_processor.py]
    D --> E[Apply LanguageTool corrections]
    E --> F[Fix grammar & tense via spaCy]
    F --> G[Return final output with issues]
    G --> H[Render index.html with results]
````

---

## 📦 Requirements

* Python 3.8+
* Flask
* spaCy + `en_core_web_trf`
* lemminflect
* language\_tool\_python
* Pandoc (CLI tool)

---

## ⚡ Example Correction

**Input**:
`He go to school yesterday.`

**Output**:
`He went to school yesterday.`

**Detected Issues**:

* Subject-verb disagreement
* Tense mismatch with past context

---

## 📁 Folder Structure

```
.
├── app.py                 # Flask app and routes
├── text_processor.py     # NLP correction logic
├── templates/
│   └── index.html        # User-facing form (not shown)
```

---

## 💡 Notes

* Pandoc must be installed and accessible via PATH
* `en_core_web_trf` must be downloaded with `python -m spacy download en_core_web_trf`
* Designed to be modular — can be extended with more rules or alternative models

---

Made for developers who want clean grammar and clean code ✍️🧼

```
```
