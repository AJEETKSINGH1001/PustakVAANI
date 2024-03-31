import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from PyPDF2 import PdfReader
import pyttsx3
import threading
from googletrans import Translator

# Function to open file dialog and select PDF book
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        threading.Thread(target=read_pdf, args=(file_path,)).start()

# Function to read PDF, translate, and narrate the text with the selected voice
def read_pdf(file_path):
    global engine
    global paused
    paused = False

    # Extract text from PDF
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    # Translate text to the desired language
    translator = Translator()
    translated_text = translator.translate(text, dest=selected_language.get()).text

    # Set properties for more human-like voice
    engine.setProperty('rate', speech_rate.get())
    engine.setProperty('volume', volume.get() / 100)  # Adjust volume (0.0 to 1.0)
    engine.setProperty('pitch', 0.8)

    selected_voice = voice_combobox.get()

    # Set voice based on the selected option
    if selected_voice == "Male":
        engine.setProperty('voice', 'english')
    elif selected_voice == "Female":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')  # Female voice ID for English

    # Narrate the translated text
    engine.say(translated_text)
    engine.runAndWait()

# Function to increase speech rate
def increase_speed():
    current_speed = speech_rate.get()
    speech_rate.set(current_speed + 50)

# Function to decrease speech rate
def decrease_speed():
    current_speed = speech_rate.get()
    speech_rate.set(max(current_speed - 50, 50))  # Ensure minimum speed is 50

# Function to increase volume
def increase_volume():
    current_volume = volume.get()
    volume.set(min(current_volume + 10, 100))  # Ensure maximum volume is 100

# Function to decrease volume
def decrease_volume():
    current_volume = volume.get()
    volume.set(max(current_volume - 10, 0))  # Ensure minimum volume is 0

# Function to pause narration
def pause_narration():
    global paused
    if not paused:
        engine.pause()
        paused = True
    else:
        engine.resume()
        paused = False

# Create root window
root = tk.Tk()
root.title("PustakVAANI")
root.geometry("500x450")
root.resizable(False, False)
root.configure(background="#f0f0f0")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Default speech rate and volume
default_speed = 150
default_volume = 70

# Create Combobox for voice selection
voices = ["Male", "Female"]
voice_combobox = ttk.Combobox(root, values=voices)
voice_combobox.set("Male")  # Default selection
voice_combobox.pack(pady=5)

# Create a scale widget for adjusting speech rate
speech_rate = tk.IntVar()
speech_rate.set(default_speed)  # Default speed
speed_label = ttk.Label(root, text="Speech Rate")
speed_label.pack()
speed_scale = ttk.Scale(root, variable=speech_rate, from_=50, to=400, length=200, orient="horizontal")
speed_scale.pack()

# Create a scale widget for adjusting volume
volume = tk.IntVar()
volume.set(default_volume)  # Default volume
volume_label = ttk.Label(root, text="Volume")
volume_label.pack()
volume_scale = ttk.Scale(root, variable=volume, from_=0, to=100, length=200, orient="horizontal")
volume_scale.pack()

# Load icon images
speed_up_icon = Image.open("speed_up_icon.png").resize((25, 25))
speed_up_img = ImageTk.PhotoImage(speed_up_icon)

speed_down_icon = Image.open("speed_down_icon.png").resize((25, 25))
speed_down_img = ImageTk.PhotoImage(speed_down_icon)

volume_up_icon = Image.open("volume_up_icon.png").resize((25, 25))
volume_up_img = ImageTk.PhotoImage(volume_up_icon)

volume_down_icon = Image.open("volume_down_icon.png").resize((25, 25))
volume_down_img = ImageTk.PhotoImage(volume_down_icon)

pause_icon = Image.open("pause_icon.png").resize((25, 25))
pause_img = ImageTk.PhotoImage(pause_icon)

# Create buttons for adjusting speech rate and volume
speed_up_button = ttk.Button(root, image=speed_up_img, command=increase_speed)
speed_up_button.pack(pady=5)
speed_down_button = ttk.Button(root, image=speed_down_img, command=decrease_speed)
speed_down_button.pack(pady=5)
volume_up_button = ttk.Button(root, image=volume_up_img, command=increase_volume)
volume_up_button.pack(pady=5)
volume_down_button = ttk.Button(root, image=volume_down_img, command=decrease_volume)
volume_down_button.pack(pady=5)

# Create button for pausing/resuming narration
pause_button = ttk.Button(root, image=pause_img, command=pause_narration)
pause_button.pack(pady=5)

# Create Open File button
open_button = ttk.Button(root, text="Open PDF Book", command=open_file)
open_button.pack(pady=10)

# Create Combobox for selecting translation language
languages = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Turkish": "tr",
    "Dutch": "nl",
    "Swedish": "sv",
    "Polish": "pl",
    "Indonesian": "id",
    "Greek": "el",
    "Norwegian": "no",
    "Finnish": "fi",
    "Danish": "da",
    "Czech": "cs",
    "Thai": "th",
    "Vietnamese": "vi",
    "Bengali": "bn",
    "Hebrew": "he",
    "Malay": "ms",
    "Filipino": "fil",
    "Hungarian": "hu",
    "Ukrainian": "uk",
    "Lithuanian": "lt",
    "Slovenian": "sl",
    "Slovak": "sk",
    "Latvian": "lv",
    "Estonian": "et",
    "Croatian": "hr",
    "Bulgarian": "bg",
    "Serbian": "sr",
    "Romanian": "ro",
    "Icelandic": "is",
    "Irish": "ga",
    "Macedonian": "mk",
    "Albanian": "sq",
    "Basque": "eu",
    "Galician": "gl",
    "Welsh": "cy",
    "Belarusian": "be",
    "Swahili": "sw",
    "Yiddish": "yi",
    "Frisian": "fy",
    "Luxembourgish": "lb",
    "Maltese": "mt",
    "Maori": "mi",
    "Samoan": "sm",
    "Tongan": "to",
    "Esperanto": "eo",
    "Corsican": "co",
    "Hawaiian": "haw"
}  # Add more languages as needed

selected_language = tk.StringVar()
language_label = ttk.Label(root, text="Select Language for Translation")
language_label.pack()
language_combobox = ttk.Combobox(root, values=list(languages.keys()), textvariable=selected_language)
language_combobox.set("English")  # Default selection
language_combobox.pack(pady=5)

# Run the main event loop
root.mainloop()
