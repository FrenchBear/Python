# sw.py
# Sound wave generation
#
# 2025-08-28    PV      Code written by Gemini

# I'd like a Python program on Windows to generate a sound 
# wave at 44100 Hz, from a function named amplitude taking sample number as input
# (int), returning an amplitude level between -1.0 and 1.0 (float). The duration (number
# of samples) is a constant defined in the program.
# 
# Here is an example of amplitude function I could use:
# 
# import math
# SAMPLING_FREQUENCY=44100 # Frequency in Hz
# def amplitude(sample: int) -> float:
#     SOUND_FREQUENCY = 440  # Frequency in Hz (A4)
#     return 0.75 * math.sin(2 * math.pi * sample/SAMPLING_FREQUENCY*SOUND_FREQUENCY) # Amplitude between -1 and +1
# 
# I'd like the option to hear the sound wave generated, and to save it in a standard .wav file for Windows.
# 
#  
# 
# Of course. Here is a Python program that generates a sound wave from a custom function, with options to play it or save it as a .wav file on Windows.
# 
# This script uses the NumPy, SoundDevice, and SciPy libraries. You'll need to install them first. Open your Windows command prompt or PowerShell and run this command:
# pip install numpy sounddevice scipy
# 
# How It Works
# 
# 1. Constants and the amplitude Function
# 
# The script starts by defining key constants like the SAMPLING_FREQUENCY (44100 Hz is standard for CD-quality audio) and the DURATION_SECONDS. The amplitude function is the core of the sound synthesis. The example provided generates a sine wave, which produces a pure tone. The mathematical formula used is:
# 
# A(t)=A_max.sin(2π.f.t)
# 
# where:
#     A(t) is the amplitude at time t.
#     A_max is the maximum amplitude (set to 0.75 to avoid clipping).
#     f is the SOUND_FREQUENCY (440 Hz for the musical note A4).
#     t is the time in seconds, calculated as sample_index / SAMPLING_FREQUENCY.
# 
# You can modify the logic inside the amplitude function to create any sound you want—for example, by combining multiple sine waves (additive synthesis), creating square or triangle waves, or generating noise.
# 
# 2. Generating the Wave Data
# 
# Instead of calling the amplitude function in a slow Python loop, we use NumPy for high performance:
#     np.arange(NUM_SAMPLES) creates an array of all sample numbers we need to calculate.
#     np.vectorize(amplitude) creates a version of your function that can operate on the entire NumPy array at once.
#     The result, wave_data, is a NumPy array containing the amplitude for every sample in your sound.
# 
# 3. Playing the Sound
# 
# The SoundDevice library makes playback simple. The command sd.play(wave_data, SAMPLING_FREQUENCY) sends your generated wave data directly to your computer's default audio output device. sd.wait() pauses the script until playback is complete.
# 
# 4. Saving the .wav File
# 
# The SciPy library provides an easy way to write .wav files.
#     Standard .wav files store audio as 16-bit integers, not as floating-point numbers.
#     We convert our wave_data array (with values from -1.0 to 1.0) to an integer array with values from -32767 to 32767.
#     write(filename, SAMPLING_FREQUENCY, int_wave_data) saves the data in the correct format.

import math
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

# --- Constants ---
SAMPLING_FREQUENCY = 44100  # Samples per second (Hz)
DURATION_SECONDS = 3        # Duration of the sound in seconds
NUM_SAMPLES = int(SAMPLING_FREQUENCY * DURATION_SECONDS)

# --- Amplitude Function ---
# This function defines the shape of the sound wave.
# It takes an integer sample number and returns a float between -1.0 and 1.0.
# You can replace the logic inside with any function you want.

def amplitude(sample_index: int) -> float:
    """
    Generates the amplitude for a given sample index.

    Args:
        sample_index: The index of the sample (e.g., from 0 to NUM_SAMPLES-1).

    Returns:
        A float value between -1.0 and 1.0.
    """
    sound_frequency = 440  # Frequency of the sound to generate in Hz (A4 note)

    # Formula for a sine wave: A * sin(2 * pi * f * t)
    # Here, t = sample_index / SAMPLING_FREQUENCY
    return 0.75 * math.sin(2 * math.pi * sound_frequency * sample_index / SAMPLING_FREQUENCY)


def main():
    """
    Main function to generate, play, and save the sound wave.
    """
    print("Generating sound wave... 🔊")

    # Create an array of sample indices, from 0 to NUM_SAMPLES-1
    sample_indices = np.arange(NUM_SAMPLES)

    # Use np.vectorize to apply the Python function to the entire NumPy array efficiently.
    # This is much faster than a standard Python for-loop.
    vectorized_amplitude = np.vectorize(amplitude)

    # Generate the wave data as a NumPy array of 32-bit floats
    wave_data = vectorized_amplitude(sample_indices).astype(np.float32)

    print("Generation complete.")

    # --- User Menu ---
    while True:
        choice = input("\nChoose an option: [P]lay, [S]ave, or [Q]uit: ").upper()

        if choice == 'P':
            # --- Play the sound ---
            print("Playing sound...")
            sd.play(wave_data, SAMPLING_FREQUENCY)
            sd.wait()  # Wait for the playback to finish
            print("Playback finished.")

        elif choice == 'S':
            # --- Save the sound to a .wav file ---
            filename = input("Enter filename (e.g., 'output.wav'): ")
            if not filename.lower().endswith('.wav'):
                filename += '.wav'

            # Convert the float wave data (-1.0 to 1.0) to 16-bit integers (-32768 to 32767)
            # This is the standard format for WAV files.
            int_wave_data = (wave_data * 32767).astype(np.int16)

            # Write the data to a .wav file
            write(filename, SAMPLING_FREQUENCY, int_wave_data)
            print(f"Sound saved to '{filename}' successfully. ✅")

        elif choice == 'Q':
            print("Exiting.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
