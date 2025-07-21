
# 🧠 Flask-based Grammar Polisher

This is a web application built with **Flask** that takes user-submitted text, processes it using a grammar correction engine based on **Gramformer**, and returns the polished version of the text.

---

## 🚀 Workflow

### 🔹 1. User Interaction (via `index.html`)
- Users submit raw text through a simple web form.
- The form sends the input via a `POST` request to the Flask app.

### 🔹 2. Flask Server (`app.py`)
- Handles routing (`/`) with support for both `GET` and `POST` methods.
- Upon form submission:
  - Extracts user text from the form field `user_text`.
  - Passes it to `polish_full_text()` from `text_polish.py`.
  - If errors occur (e.g., empty input), they are caught and returned as an error message.
- Renders `index.html` with the result (corrected text or error).

---

## 🛠️ Grammar Correction Logic (`text_polish.py`)

### ✨ Core Function: `polish_full_text(text)`
- Validates that input is non-empty and a string.
- Uses **Gramformer**, a powerful NLP model, to suggest grammatical corrections.
- Detects differences between original and corrected sentences.
- Returns:
  - The original sentence.
  - The corrected version.
  - A list of specific changes (word-by-word diff highlighting insertions and deletions).

---

## 📦 Under the Hood: Gramformer

This project uses the [**Gramformer**](https://github.com/PrithivirajDamodaran/Gramformer) library by **Prithiviraj Damodaran (@PrithivirajDamodaran)**.

### 🔍 What is Gramformer?
Gramformer is a modern NLP library that supports:
- **Grammar Error Correction (GEC)**
- **Text Generation**
- **Paraphrasing**

It uses transformer-based architectures under the hood.

### 🧠 Model Used: `prithivida/grammar_error_correcter_v1`
This model is hosted on [Hugging Face](https://huggingface.co/prithivida/grammar_error_correcter_v1). It is built using a fine-tuned **T5 Transformer** and is capable of correcting:
- Spelling mistakes
- Grammar issues
- Sentence structuring problems

This model provides suggestions via beam search, enabling top-k correction candidates.

---

## 📂 Project Structure

```
├── app.py              # Flask app logic
├── text_polish.py      # Grammar correction engine using Gramformer
├── templates/
│   └── index.html      # HTML form interface
```

---

## 🌐 Running the App

Make sure you have:

* Python 3.8+
* Flask
* Gramformer and its dependencies installed

### 🧪 Run with:

```bash
python app.py
```

Then visit `http://localhost:5000` to access the web app.

---

## 🙏 Acknowledgements

* **Gramformer** by [Prithiviraj Damodaran](https://github.com/PrithivirajDamodaran/Gramformer)
* Hugging Face model: [`prithivida/grammar_error_correcter_v1`](https://huggingface.co/prithivida/grammar_error_correcter_v1)


