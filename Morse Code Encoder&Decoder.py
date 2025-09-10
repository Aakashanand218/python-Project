import tkinter as tk
from tkinter import messagebox
import platform
import time

# Only import winsound if on Windows
if platform.system() == "Windows":
    import winsound

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',
    'D': '-..',   'E': '.',     'F': '..-.',
    'G': '--.',   'H': '....',  'I': '..',
    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',
    'S': '...',   'T': '-',     'U': '..-',
    'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': '/'
}

REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

# Encode Text to Morse
def encode_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

# Decode Morse to Text
def decode_from_morse(morse_code):
    words = morse_code.strip().split(' ')
    return ''.join(REVERSE_DICT.get(code, '') for code in words)

# Play Morse Code Beep Sound
def play_morse_audio(morse_code):
    if platform.system() != "Windows":
        messagebox.showinfo("Audio", "Audio beep is only supported on Windows.")
        return

    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(700, 100)  # short beep
        elif symbol == '-':
            winsound.Beep(700, 300)  # long beep
        elif symbol == ' ':
            time.sleep(0.2)          # gap between characters
        elif symbol == '/':
            time.sleep(0.4)          # gap between words

# GUI Functionality
def encode_action():
    
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text to encode.")
        return
    morse = encode_to_morse(input_text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, morse)

def decode_action():
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter Morse code to decode.")
        return
    decoded = decode_from_morse(input_text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, decoded)

def play_action():
    morse = output_box.get("1.0", tk.END).strip()
    if morse:
        play_morse_audio(morse)
    else:
        messagebox.showwarning("No Morse", "There is no Morse code to play!")

# GUI Setup
window = tk.Tk()
window.title("Morse Code Converter")
window.geometry("500x420")
window.config(bg="#1c1c1c")

tk.Label(window, text="Input Text / Morse Code", fg="white", bg="#1c1c1c", font=("Arial", 12)).pack(pady=5)
input_box = tk.Text(window, height=5, width=60, bg="#2e2e2e", fg="white", insertbackground="white")
input_box.pack()

# Buttons
button_frame = tk.Frame(window, bg="#1c1c1c")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Encode", command=encode_action, width=10, bg="#00bcd4", fg="white").grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Decode", command=decode_action, width=10, bg="#4caf50", fg="white").grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Play Beeps", command=play_action, width=10, bg="#f44336", fg="white").grid(row=0, column=2, padx=10)

tk.Label(window, text="Output", fg="white", bg="#1c1c1c", font=("Arial", 12)).pack(pady=5)
output_box = tk.Text(window, height=5, width=60, bg="#2e2e2e", fg="white", insertbackground="white")
output_box.pack()

window.mainloop()
