import speech_recognition as sr
import pyttsx3
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import numpy as np
import sounddevice as sd
import threading
import subprocess
import backend


# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Initialize Tkinter window
window = tk.Tk()
window.title("AI Fitness Buddy")

# Set display dimensions
display_width, display_height = 800, 600

# Create canvas for drawing
canvas = tk.Canvas(window, width=display_width, height=display_height)
canvas.pack()

# Load the background image

background = Image.open("gym.jpg")
background = background.resize((display_width, display_height))
photo_image = ImageTk.PhotoImage(background)

# Visualizer settings
bar_width = 25
bar_spacing = 2
bar_height = 4
bar_count = 50
bars_x = (display_width - (bar_width + bar_spacing) * bar_count + bar_spacing) // 2
bars_y = display_height - 450
sensitivity = 30

# Create sounddevice stream
sample_rate = 44100
buffer_size = 1024
stream_sd = sd.InputStream(samplerate=sample_rate, channels=1)
stream_sd.start()

# Create a transparent frame for conversation text
frame = ttk.Frame(window, padding="10")
frame.place(x=(display_width - 400) // 2, y=display_height - 220)

# Conversation Text Widget
conversation = tk.Text(frame, wrap=tk.WORD, width=50, height=10, font=("TkDefaultFont", 12))
conversation.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))
conversation.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))


def execute_other_code(conversation):
    # Call the other file or function here and capture the output
    process = subprocess.Popen(["python", "backend.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode("utf-8")

    # Update the Conversation Text Widget with the output
    conversation.configure(state="normal")  # Enable editing the widget
    conversation.insert(tk.END, "AKI: " + output + "\n")
    conversation.configure(state="disabled")  # Disable editing the widget
    speak(output, conversation)

def speak(message, conversation):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 190)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    print("Aki:", message)
    conversation.insert(tk.END, "AKI: " + message + "\n", "bold")
    engine.say(message)
    engine.runAndWait()
    conversation.see(tk.END)

def listen_thread(conversation):
    while True:
        command = listen(conversation)
        if command:
            print("Listening...")
            conversation.insert(tk.END, "You: " + command + "\n", "bold")
            engine.runAndWait()

def listen(conversation):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=1000000000)
    try:
        command = r.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        conversation.insert(tk.END, "Aki is now listening ...\n")
        return None
    except sr.RequestError:
        conversation.insert(tk.END, "Aki is now listening ...\n")
        return None

def update_visualization(bar_positions_up, bar_positions_down):
    # Get the microphone input samples from sounddevice
    samples_sd, _ = stream_sd.read(buffer_size)

    # Perform the Fast Fourier Transform (FFT) on the samples from sounddevice
    spectrum_sd = np.fft.fft(samples_sd)
    frequencies_sd = np.abs(spectrum_sd[:len(spectrum_sd) // 2])

    # Clear the canvas
    canvas.delete("all")

    # Draw the background image
    canvas.create_image(0, 0, anchor="nw", image=photo_image)

    # Draw the visualizer bars using sounddevice frequencies
    for i in range(bar_count):
        bar_x = bars_x + (bar_width + bar_spacing) * i
        if i * 2 < len(frequencies_sd):
            value = frequencies_sd[i * 2]
            if np.isnan(value):
                value = 0.0
            # Adjust the sensitivity here to increase the responsiveness
            bar_height_sd = max(int(value * sensitivity * 10), bar_height)
            # Calculate the y-coordinate of the bar's top position
            bar_top_y = bars_y - bar_height_sd
            # Draw the rectangle from the top position downward
            canvas.create_rectangle(bar_x, bar_top_y, bar_x + bar_width, bars_y, fill="white")

    # Update bar positions based on sound intensity
    for i in range(bar_count):
        bar_height_up = max(int(frequencies_sd[(i + 10) * 2]) * sensitivity, bar_height)
        bar_positions_up[i] = max(bars_y - bar_height_up, 0)  # Update up bar position

        bar_height_down = max(int(frequencies_sd[(i + 20) * 2]) * sensitivity, bar_height)
        bar_positions_down[i] = min(bars_y + bar_height_down, display_height)  # Update down bar position

    # Draw the visualizer bars
    for i in range(bar_count):
        bar_x = bars_x + (bar_width + bar_spacing) * i
        canvas.create_rectangle(bar_x, bar_positions_up[i], bar_x + bar_width, bars_y, fill="white")  # Draw up bar

    # Update the Tkinter window
    window.after(10, update_visualization, bar_positions_up, bar_positions_down)

def check_gui_running():
    if tk._default_root is None:
        print("Aki is now not running...")
    else:
        print("Aki is now running...")
        execute_other_code(conversation)

# Start listening thread
listen_t = threading.Thread(target=listen_thread, args=(conversation,), daemon=True)
listen_t.start()

# Start visualization update
bar_positions_up = [bars_y] * bar_count  # Initialize up bar positions
bar_positions_down = [bars_y] * bar_count  # Initialize down bar positions
update_visualization(bar_positions_up, bar_positions_down)

# Start checking if the GUI is running
gui_thread = threading.Thread(target=check_gui_running, daemon=True)
gui_thread.start()

# Start Tkinter main loop
window.mainloop()

# Stop and close sounddevice stream
stream_sd.stop()
stream_sd.close()

