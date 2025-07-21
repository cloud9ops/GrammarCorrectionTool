
# Overview

This project is a real-time desktop keylogger with integrated grammar correction. It captures user keystrokes, buffers them into full sentences, and processes them using both rule-based and machine learning grammar correction techniques. A graphical interface displays the original and polished sentences, and the original input is also logged to a file.

---

## File Structure

```
project-root/
├── keylogging.py        # Main script with GUI and keylogger logic
├── text_polish.py       # Grammar correction and sentence polishing module
├── requirements.txt     # Python dependencies (optional but recommended)
└── README.md            # Project documentation (this file)
```

---

## Module Breakdown

### text\_polish.py

This module is responsible for:

* Tokenizing and validating input size for model limits
* Detecting grammar issues using `language_tool_python`
* Polishing sentences using a pretrained transformer model (`prithivida/grammar_error_correcter_v1`)
* Providing structured results including polished text, issues found, and per-sentence analysis

### keylogging.py

This script runs a Tkinter-based GUI application that:

* Starts a background keylogger using `pynput`
* Buffers keystrokes and extracts full sentences using punctuation detection
* Sends sentences to the polishing engine (`text_polish.py`)
* Displays results in real time
* Writes the original input to `~/.corporate_keylog.txt`
* Offers Start and Stop buttons to control logging and clear the session

---

