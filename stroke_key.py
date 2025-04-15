"""
Strikes binded keys to switch the emotion in VTuber app
"""

import tkinter as tk
from threading import Thread
import time
import socket
from pynput.keyboard import Key, Controller

# Key Controller
keyboard = Controller()
stop_flag = False

# Emotion to key mapping
emotion_key_map = {
    "happy": "j",
    "sad": "s",
    "angry": "a",
    "surprised": "x",
    "disgusted": "s",
    "fearful": "x",
    "neutral": "n",
}

current_emotion = None
new_emotion = None

def send_key_stroke():
    global current_emotion
    global new_emotion
    global stop_flag

    while not stop_flag:
        # Check if the emotion is supported
        if new_emotion == current_emotion:
            print("Emotion continued")
        elif new_emotion in emotion_key_map:
            # Update the current emotion
            current_emotion = new_emotion

            # Send the key stroke for the current emotion
            print(f"Sending key stroke for {current_emotion}")
            keyboard.press(emotion_key_map[current_emotion])
            time.sleep(0.01)
            keyboard.release(emotion_key_map[current_emotion])
        else:
            print(f"Emotion {current_emotion} not supported")

        # cool down 
        time.sleep(1)

def start_task():
    global stop_flag

    stop_flag = False
    Thread(target=send_key_stroke).start()

def stop_task():
    global stop_flag

    stop_flag = True

def socket_listener(host="localhost", port=5000):
    """
    Listens for emotion messages from the backend app
    """
    global new_emotion

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Listening on {host}:{port}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode("utf-8")
                print(f"Received: {data}")

                if data:
                    new_emotion = data
                else:
                    print("No data received")

def main():
    global stop_flag

    # Start the socket listener in sepparate thread
    socket_thread = Thread(target=socket_listener, args=("localhost", 5000), daemon=True)
    socket_thread.start()

    # Strat the background task to send key strokes
    print("Starting background task...")
    try:
        start_task()
    except KeyboardInterrupt or Exception as e:
        if e:
            print("Error:", str(e))
        print("\nShutting down...")
        stop_flag = True
        socket_thread.join()

if __name__ == "__main__":
    main()