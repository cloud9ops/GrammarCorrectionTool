
# AutoTextPolish - Real-Time Text Polishing Web App

A Flask-based web interface for real-time, sentence-by-sentence text enhancement using the powerful [Gramformer](https://github.com/PrithivirajDamodaran/Gramformer) correction engine, built upon Prithivida’s T5 model.

---

## File: `app.py`

This is the core server-side file responsible for handling web routes, streaming polished output, and serving frontend content.

---

## Routes and Logic

### `/` (GET)
- Renders the `index.html` template — the main UI.

---

### `/stream` (POST)
**Purpose**:  
Streams polished text in real-time, sentence by sentence.

**Input**:  
- `user_text`: Raw multiline input from the user (e.g., a paragraph)

**Workflow**:
1. Grabs user input from the POST request form.
2. If input is empty, returns a 400 response.
3. Internally:
   - Calls the generator function `stream_polish_sentences()` from `text_polish`.
   - Converts each sentence result into JSON format.
   - Sends each one back as a Server-Sent Event (SSE) stream to the frontend.

**Output**:  
A `text/event-stream` response where each line is:
```text
data: {"original": "...", "polished": "..."}
````

---

### `/auto-polish` (POST)

**Purpose**:
Returns a single corrected version of a sentence.

**Input (JSON)**:

```json
{
  "sentence": "Your original sentence here"
}
```

**Workflow**:

1. Grabs sentence from JSON.
2. Validates non-empty input.
3. Passes it into `stream_polish_sentences()` to get polished candidates.
4. Returns only the first result as JSON.

**Output**:

```json
{
  "original": "...",
  "polished": "..."
}
```

---

## Flask Settings

* `threaded=True`: Allows multiple requests to be processed in parallel.
* `host="0.0.0.0"`: Makes the app externally accessible (e.g., in containers or remote VMs).

---

## Behind the Scenes: Gramformer

This app relies on [Gramformer](https://github.com/PrithivirajDamodaran/Gramformer), a library developed by [Prithiviraj Damodaran](https://github.com/PrithivirajDamodaran), which corrects grammar using pretrained T5 models fine-tuned for:

* Grammar correction
* Text generation
* Syntax refinement

The T5 base model used is `prithivida/grammar_error_correcter_v1`, designed specifically for grammatical error correction tasks.

---

## Summary

This Flask app:

* Supports real-time polishing via streaming SSE
* Offers on-demand single-sentence correction via a lightweight JSON API
* Harnesses the power of Transformer models in a developer-friendly interface

