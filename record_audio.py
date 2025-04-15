"""
Record audio for specified duration
Parameters: output file path, duration in second, sample rate
"""

import sounddevice as sd
import soundfile as sf
import numpy as np

# sd.default.device = [3,6]
print('input device used:', sd.query_devices(sd.default.device[0]))

# Record audio
def record_audio(output_path, duration=5, sample_rate=16000):
    print("Listening...")
    audio = sd.rec(int(duration*sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait() # wait until recording finishes
    
    # Preprocess the audio (normalize and handle channels)
    # TODO(Noise cancelling)
    # audio = noise_cancelling(audio)
    audio = audio / np.max(np.abs(audio))  # Normalize
    if audio.ndim > 1:  # If stereo, take the first channel
        audio = audio[:, 0]
    # Convert audio to tensor Float (32-bit float)
    audio = audio.astype(np.float32)
    
    sf.write(output_path, audio, sample_rate)
    print(f"Recording saved to {output_path}")

def is_audio_silent(file_path, silence_threshold=-40):
    """
    Check if the audio file is silent
    """
    try:
        audio, sample_rate = sf.read(file_path)
        print(max(audio))
        return max(audio) < silence_threshold
    except Exception as e:
        print("Error", str(e))
        return True
    
def noise_cancelling(audio):
    """
    Noise cancelling
    """
    try:
        # print("TODO")
        return audio
    except Exception as e:
        print("Error", str(e))

# Example usage
# record_audio("recorded_audio.wav", duration=5)
    