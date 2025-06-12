import tkinter as tk
from tkinter import ttk
import secrets
import os
import pyautogui
import threading
import time

WORDLIST_PATH = r"C:\Users\User\hash\english.txt"

def load_wordlist(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Wordlist not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return [word.strip() for word in f.readlines()]

def generate_mnemonic(wordlist, word_count):
    return " ".join(secrets.choice(wordlist) for _ in range(word_count))

class LoopingMnemonicApp:
    def __init__(self, root):
        self.root = root
        self.wordlist = load_wordlist(WORDLIST_PATH)
        self.word_count_var = tk.IntVar(value=12)
        self.running = True
        self.counter = 0

        self.setup_ui()
        threading.Thread(target=self.auto_loop, daemon=True).start()

    def setup_ui(self):
        self.root.title("🔁 Auto Mnemonic Generator & Typer")
        self.root.geometry("850x300")

        controls = ttk.Frame(self.root)
        controls.pack(pady=10)

        ttk.Label(controls, text="Words:").pack(side=tk.LEFT)
        ttk.Radiobutton(controls, text="12", variable=self.word_count_var, value=12).pack(side=tk.LEFT)
        ttk.Radiobutton(controls, text="24", variable=self.word_count_var, value=24).pack(side=tk.LEFT)

        stop_btn = ttk.Button(controls, text="Stop", command=self.stop_loop)
        stop_btn.pack(side=tk.LEFT, padx=20)

        self.status_label = ttk.Label(self.root, text="Starting auto typing loop...")
        self.status_label.pack()

        self.counter_label = ttk.Label(self.root, text="Mnemonics pasted: 0")
        self.counter_label.pack()

        self.phrase_box = tk.Text(self.root, height=3, font=("Courier", 12), wrap="word", width=100)
        self.phrase_box.pack(pady=10)
        self.phrase_box.configure(state="disabled")

    def stop_loop(self):
        self.running = False
        self.status_label.config(text="🛑 Loop stopped.")

    def auto_loop(self):
        while self.running:
            # Generate new phrase every loop
            phrase = generate_mnemonic(self.wordlist, self.word_count_var.get())

            # Update GUI text
            self.phrase_box.configure(state="normal")
            self.phrase_box.delete("1.0", tk.END)
            self.phrase_box.insert("1.0", phrase)
            self.phrase_box.configure(state="disabled")

            # Copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(phrase)
            self.root.update()

            self.status_label.config(text="📋 Copied. Auto-pasting in 3 seconds...")
            time.sleep(3)

            # Paste and press enter
            pyautogui.write(phrase)
            pyautogui.press("enter")

            delay = 60 / 140  # BPM
            for _ in range(13):
                if not self.running:
                    return
                time.sleep(delay)
                pyautogui.press("enter")

            self.counter += 1
            self.counter_label.config(text=f"Mnemonics pasted: {self.counter}")
            self.status_label.config(text="✅ Done. Generating next in 2s...")
            time.sleep(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoopingMnemonicApp(root)
    root.mainloop()
