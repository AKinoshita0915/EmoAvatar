"""
Main APP
"""

import tkinter as tk
from tkinter import messagebox
from record_audio import record_audio, is_audio_silent
from proto_emo_back import predict_emotion

import threading

""" Global """
mic_on = False
record_duration = 3
silent_threshold = 0.05

""" Functions """
# Toggle mic function
def toggle_mic():
    global mic_on
    mic_on = not mic_on # toggle

    if mic_on:
        record_btn.config(text="Listening: On", bg="lightgreen")
        start_loop()
    else:
        record_btn.config(text="Listening: Off", bg="red")

# Function to update the recording duration
def update_duration():
    global record_duration
    try:
        new_duration = int(duration_entry.get()) # Get value from entry field
        if new_duration <= 0:
            raise ValueError("Duration must be greater than 0.")
        record_duration = new_duration
        messagebox.showinfo("Success", f"Recording duration updated to {record_duration} seconds.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to update the silence threshold
def update_threshold():
    global silent_threshold
    try:
        new_threshold = float(threshold_entry.get()) # Convert value to float
        if not (0.0 <= new_threshold <= 1.0):
            raise ValueError("Threshold must be a value between 0.0 and 1.0.")
        silent_threshold = new_threshold
        messagebox.showinfo("Success", f"Silent threshold updated to {silent_threshold}.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to record and predict its emotion
def record_and_predict():
    try:
        global record_duration
        global silent_threshold

        # Record the audio
        output_path = "recorded_audio.wav"
        record_audio(output_path, duration=record_duration, sample_rate=16000)

        # Check if the audio is silent
        if is_audio_silent(output_path, silence_threshold=silent_threshold):
            print("Audio contains no speech.")
            return

        # Predict the emotion from recorded audio
        result = predict_emotion(output_path)

        # Display the result
        if "emotion" in result:
            print(f"Predicted Emotion: {result['emotion']}")
        elif "error" in result:
            print("Error", result["error"])
        else:
            print("Error", result.get("Unknown Error"))
    except Exception as e:
        print("Error", str(e))

# loop function for record and predict
def start_loop():
    def loop_record_and_predict():
        while mic_on:
            record_and_predict()
    # Run the loop in a separate thread to keep the UI responsive
    threading.Thread(target=loop_record_and_predict, daemon=True).start()

""" GUI """
# Initialize GUI
root = tk.Tk()
root.title("Speech Emotion Recognition")

# Add duration input field
duration_label = tk.Label(root, text="Recording Duration (seconds):", font=("Arial", 12))
duration_label.pack(pady=10)

duration_entry = tk.Entry(root, font=("Arial", 12))
duration_entry.insert(0, str(record_duration))
duration_entry.pack(pady=10)

update_duration_btn = tk.Button(root, text="Update Duration", command=update_duration, font=("Arial", 12))
update_duration_btn.pack(pady=10)

# Add threshold input field
threshold_label = tk.Label(root, text="Silence Threshold(0.0-1.0):", font=("Arial", 12))
threshold_label.pack(pady=10)

threshold_entry = tk.Entry(root, font=("Arial", 12))
threshold_entry.insert(0, str(silent_threshold))
threshold_entry.pack(pady=10)

update_threshold_btn = tk.Button(root, text="Update Threshold", command=update_threshold, font=("Arial", 12))
update_threshold_btn.pack(pady=10)

# Add button to record and predict
record_btn = tk.Button(root, text="Listening: Off", 
                       command=toggle_mic, 
                       font=("Arial", 14), bg="red", fg="black")
record_btn.pack(pady=20)

# Add instructions
instructions = tk.Label(root, text="Toggle the button to start/stop listening \nand predict the emotion.", 
                        font=("Arial", 12), fg="gray")
instructions.pack(pady=10)

# Run the Tkinter event loop
root.geometry("400x400")
root.mainloop()