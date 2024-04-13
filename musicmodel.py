import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

def GenerateAudio(Collision=False, n=10, duration=5, sampling_rate=44100, frequency=440):
    # Set parameters
    duration = duration  # Duration of the melody in seconds
    sampling_rate = sampling_rate  # Sampling rate (samples per second)
    frequency = frequency  # Frequency of the note (A4)

    # Generate time array
    t = np.linspace(0, duration, int(sampling_rate * duration))

    # Create a sine wave for the melody
    melody = np.sin(2 * np.pi * frequency * t)

    # Normalize the melody
    melody /= np.max(np.abs(melody))

    # Generate a collision sound
    if Collision:
        collision = np.random.rand(sampling_rate * duration)
        collision /= np.max(np.abs(collision))
        audio = melody + collision
    else:
        audio = melody
        
    return audio