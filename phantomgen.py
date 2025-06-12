import tkinter as tk
from tkinter import ttk
import secrets
import os

# Path to your BIP-39 word list
WORDLIST_PATH = r"C:\Users\User\hash\english.txt"

def load_wordlist(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Wordlist not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return [word.strip() for word in f.readlines()]

# Generate one mnemonic
def generate_mnemonic(wordlist, word_count):
    return " ".join(secrets.choice(wordlist) for _ in range(word_count))

# GUI App
class MnemonicApp:
    def __init__(self, root):
        self.wordlist = load_wordlist(WORDLIST_PATH)

        root.title("BIP-39 Mnemonic Generator")
        root.geometry("850x600")

        # Options
        self.word_count_var = tk.IntVar(value=12)
        options_frame = ttk.Frame(root)
        options_frame.pack(pady=10)

        ttk.Label(options_frame, text="Mnemonic Length:").pack(side=tk.LEFT)
        ttk.Radiobutton(options_frame, text="12 words", variable=self.word_count_var, value=12).pack(side=tk.LEFT)
        ttk.Radiobutton(options_frame, text="24 words", variable=self.word_count_var, value=24).pack(side=tk.LEFT)
        ttk.Button(options_frame, text="Generate 20 Phrases", command=self.generate_all).pack(side=tk.LEFT, padx=10)

        # Result area with scrollbar
        self.canvas = tk.Canvas(root)
        self.frame = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def generate_all(self):
        # Clear previous phrases
        for widget in self.frame.winfo_children():
            widget.destroy()

        word_count = self.word_count_var.get()
        for i in range(20):
            phrase = generate_mnemonic(self.wordlist, word_count)
            row = ttk.Frame(self.frame)
            row.pack(fill=tk.X, pady=5, padx=10)

            text = tk.Text(row, height=2, wrap="word", font=("Courier", 10))
            text.insert("1.0", phrase)
            text.configure(state="disabled", width=70)
            text.pack(side=tk.LEFT, padx=(0, 10))

            copy_btn = ttk.Button(row, text="Copy", command=lambda p=phrase: self.copy_to_clipboard(p))
            copy_btn.pack(side=tk.LEFT)

    def copy_to_clipboard(self, phrase):
        root.clipboard_clear()
        root.clipboard_append(phrase)
        root.update()  # now it stays on the clipboard after the app is closed

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MnemonicApp(root)
    root.mainloop()
