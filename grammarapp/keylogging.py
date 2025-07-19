import os
import re
import threading
import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard
from text_polish import polish_full_text

# === Global Variables ===
SENTENCE_BUFFER = ""
LOG_FILE = os.path.expanduser('~/.corporate_keylog.txt')
lock = threading.Lock()
listener = None
listener_running = False

# === Extract complete sentences ===
def extract_complete_sentences(text):
    sentences = re.findall(r'[^.!?]*[.!?]', text)
    remaining = re.sub(r'[^.!?]*[.!?]', '', text)
    return [s.strip() for s in sentences if len(s.strip()) > 5], remaining

# === Log and display polished output ===
def process_sentence(sentence, output_widget):
    result = polish_full_text(sentence)
    polished = result['polished_text']
    write_to_log(sentence)

    output = f"\n[Original]: {sentence}\n[Polished]: {polished}\n"
    output_widget.insert(tk.END, output)
    output_widget.see(tk.END)

# === Write original sentence to file ===
def write_to_log(text):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

# === Key press handler ===
def on_key_press(key, output_widget):
    global SENTENCE_BUFFER
    try:
        if key == keyboard.Key.space:
            SENTENCE_BUFFER += ' '
        elif key == keyboard.Key.enter:
            SENTENCE_BUFFER += '\n'
        elif key == keyboard.Key.backspace:
            SENTENCE_BUFFER = SENTENCE_BUFFER[:-1]
        elif hasattr(key, 'char') and key.char is not None:
            SENTENCE_BUFFER += key.char
    except:
        pass

    with lock:
        sentences, remaining = extract_complete_sentences(SENTENCE_BUFFER)
        SENTENCE_BUFFER = remaining
        for s in sentences:
            process_sentence(s, output_widget)

# === Start keylogger in thread ===
def start_keylogger(output_widget):
    global listener, listener_running

    if listener_running:
        return

    def keylogger_thread():
        global listener
        listener = keyboard.Listener(on_press=lambda key: on_key_press(key, output_widget))
        listener.start()
        listener.join()

    listener_running = True
    threading.Thread(target=keylogger_thread, daemon=True).start()

# === Stop keylogger and clear log ===
def stop_keylogger(output_widget):
    global listener, listener_running, SENTENCE_BUFFER

    if listener is not None:
        listener.stop()
        listener = None
    listener_running = False
    SENTENCE_BUFFER = ""

    # Clear log file
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('')

    # Show stopped status
    output_widget.insert(tk.END, "\n[✘] Logging stopped and log file cleared.\n")
    output_widget.see(tk.END)

# === UI Setup ===
def create_gui():
    window = tk.Tk()
    window.title("Live Grammar Keylogger")
    window.geometry("700x500")
    window.resizable(False, False)

    # === Text Area ===
    output = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("TkDefaultFont", 11), height=20)
    output.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # === Button Frame (pack instead of grid) ===
    button_frame = tk.Frame(window)
    button_frame.pack(pady=5)

    start_btn = tk.Button(button_frame, text="Start", width=15, bg="#4CAF50", fg="white",
                          command=lambda: start_keylogger(output))
    start_btn.pack(side=tk.LEFT, padx=10)

    stop_btn = tk.Button(button_frame, text="Stop", width=15, bg="#F44336", fg="white",
                         command=lambda: stop_keylogger(output))
    stop_btn.pack(side=tk.LEFT, padx=10)

    window.mainloop()


# === Run GUI ===
if __name__ == "__main__":
    create_gui()
