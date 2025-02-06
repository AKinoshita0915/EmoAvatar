"""
Backend service
"""

from funasr import AutoModel

import os
import re
import socket


#Load Model
model = AutoModel(model="./emotion2vec_plus_base", disable_update=True)
print("loaded")

# Function to send the emotion to the image window
def send_emotion_to_display(emotion, host="localhost", port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(emotion.encode("utf-8"))
            print(f"Sent emotion: {emotion}")
    except Exception as e:
        print("Error", str(e))

# Predict emotion
def predict_emotion(audio_file):
    try:
        res = model.generate("recorded_audio.wav", output_dir="./outputs", granularity="utterance", extract_embedding=False)
        # os.remove(audio_file) # clean up
        print(res)

        # Extract highest scoring emotion
        scores = res[0]["scores"]
        labels = res[0]["labels"]
        max_score_index = scores.index(max(scores))
        
        # Filter the predicted label to remove non-English characters
        predicted_emotion = re.sub(r'[^a-zA-Z]', '', labels[max_score_index])

        # Update the image in the existing window
        send_emotion_to_display(predicted_emotion)

        return {"emotion": predicted_emotion}
        
    except Exception as e:
        return {"error": str(e)}
print("defined")   
# Example usage
# audio_file = "..\..\Datasets\STUDIES\ITA\Emotion100-Angry\wav\ITA-Emotion100-Teacher-Angry-004.wav"
# predict_emotion(audio_file)
# print("predicted")