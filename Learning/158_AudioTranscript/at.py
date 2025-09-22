# at.py - AudioTranscript
#
# 2025-09-22    PV      First version from Gemini

# I have a series of mp3 audio files from a french radio podcast, an example is attached. I need a python program to
# transcribe spoken text, that takes the path of a .mp3 file, and would write the result of audio transcription in a
# .txt in a second provided path+file. I would be nice to have the choice between different audio transcription models
# so I can find the more efficient for my data.

# Of course! I can create a Python program that transcribes audio from an MP3 file and saves it to a text file. To give
# you the flexibility you asked for, the script will let you choose between three different transcription models:
# Whisper, Vosk, and the Google Web Speech API.
#
# I will provide you with three files:
#
#     transcribe.py: The main Python script to perform the transcription.
#
#     requirements.txt: A file listing the necessary Python libraries for you to install.
#
#     README.md: A guide explaining how to set up and use the script, including how to download the necessary model for Vosk.
#
# You're all set! Just follow the setup instructions in the README.md file to install the necessary libraries. After
# that, you can run the transcribe.py script from your terminal with the audio file you provided.
#
# Let me know if you have any questions or need further modifications!

# Dependencies (requiremlents.txt)
# pydub
# SpeechRecognition
# openai-whisper
# vosk

# (Vosk Only) Download the French Language Model
#
# If you plan to use the vosk model, you need to download the appropriate language model.
#     Go to the Vosk Models Page. (https://alphacephei.com/vosk/models)
#     Find a French model (e.g., vosk-model-fr-0.22) and download it.
#     Unzip the downloaded file. You will get a folder (e.g., vosk-model-fr-0.22).
#     Remember the path to this folder, as you will need it to run the script.
#     -> D:\Vosk\vosk-model-fr-0.6-linto-2.2.0

# Problem, whisper needs specifically numpy 2.2 and I have 2.3 on py machine...
# python -v venv venv
# venv\Scripts\activate    (or activate in VSCode)
# pip install -r requirements.txt

from datetime import datetime
import os
import time
import wave
import json
import sys
from pydub import AudioSegment
import speech_recognition as sr
from common_fs import folder_part, get_all_files, file_exists


# --- Model-specific transcription functions ---

def transcribe_with_whisper(wav_path: str, model_name: str):
    """
    Transcribes audio using OpenAI's Whisper model.
    This model runs locally and offers high accuracy.
    """
    try:
        import whisper
    except ImportError:
        print("Whisper not installed. Please run: pip install openai-whisper")
        sys.exit(1)

    # print("Loading Whisper model (this may take a moment)...")
    # You can choose other models like "base", "tiny", "small", "medium", "large"
    # "base" is a good starting point.
    whisper_model = whisper.load_model(model_name)
    print(f"Transcribing with Whisper {model_name}...")
    result = whisper_model.transcribe(wav_path, language="fr", fp16=False, patience=2, beam_size=5)
    return str(result["text"])

def transcribe_with_vosk(wav_path, model_path):
    """
    Transcribes audio using the Vosk offline model.
    Requires a language-specific model to be downloaded.
    """
    if not model_path or not os.path.exists(model_path):
        print(f"Vosk model path '{model_path}' not found.")
        print("Please download a French model from https://alphacephei.com/vosk/models and provide the path using --vosk_model_path")
        sys.exit(1)

    try:
        from vosk import Model, KaldiRecognizer
    except ImportError:
        print("Vosk not installed. Please run: pip install vosk")
        sys.exit(1)

    print("Loading Vosk model...")
    model = Model(model_path)
    wf = wave.open(wav_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    print("Transcribing with Vosk...")
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result.get("text", ""))

    part_result = json.loads(rec.FinalResult())
    results.append(part_result.get("text", ""))

    return " ".join(results)

def transcribe_with_google(wav_path):
    """
    Transcribes audio using Google's Web Speech API.
    Requires an active internet connection.
    """
    print("Transcribing with Google Web Speech API...")
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        try:
            # recognize speech using Google Speech Recognition
            # Using French language for transcription
            text = r.recognize_google(audio_data, language="fr-FR")
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"


def my_log(msg: str, skip_line: bool = False):
    # Get the current time
    now = datetime.now()
    # Format the timestamp down to milliseconds
    # %f gives microseconds, so we slice the first 3 digits for milliseconds
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open("c:\\temp\\transcription.log", "a") as file:
        if skip_line:
            file.write("\n")
        file.write(timestamp + "\t" + msg + "\n")

def transcribe_audio(input_mp3: str):
    # Validate input file
    if not os.path.exists(input_mp3):
        print(f"Error: Input file not found at '{input_mp3}'")
        return
    print("\n\n\n---------------------------------------------------\nProcessing "+input_mp3)
    my_log("Processing " + input_mp3, True)

    # Convert MP3 to WAV
    tstart = time.time()
    print("Converting input to a temporary WAV file...")
    try:
        audio = AudioSegment.from_mp3(input_mp3)
        # Convert to mono and set a standard sample rate
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)  # 16kHz is standard for many speech models

        temp_wav_path = r"C:\temp\temp_transcription_audio.wav"
        # Export as WAV
        audio.export(temp_wav_path, format="wav")
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        print("Please ensure you have ffmpeg installed and accessible in your system's PATH.")
        return
    duration = time.time() - tstart
    msg = "WAV conversion completed in " + str(round(duration, 3)) + 's'
    print(msg)
    my_log(msg)

    # --- 3. Transcribe based on selected model
    print(input_mp3)
    # for model in ["whisper_base", "whisper_tiny", "whisper_small", "whisper_medium", "whisper_large", "vosk", "google"]:
    for model in ["whisper_small"]:
        print("- " + model)
        tstart = time.time()
        transcribed_text = ""
        if model.startswith("whisper"):
            model_name = model.split("_")[1]
            transcribed_text = transcribe_with_whisper(temp_wav_path, model_name)
        elif model == "vosk":
            transcribed_text = transcribe_with_vosk(temp_wav_path, vosk_model_path)
        elif model == "google":
            transcribed_text = transcribe_with_google(temp_wav_path)
        duration = time.time() - tstart
        msg = "Transcription with " + model + " completed in " + str(round(duration, 3)) + 's'
        print(msg)
        my_log(msg)

        # Save transcription to output file
        # output_txt = f"c:\\temp\\transcription_{model}.txt"
        output_txt = input_mp3.replace(".mp3", ".txt").replace(r"C:\MusicOD\Humour", r"C:\Temp")
        os.makedirs(folder_part(output_txt), exist_ok=True)
        try:
            with open(output_txt, 'w', encoding='utf-8') as f:
                f.write(transcribed_text)
            # print(f"\nTranscription successful!")
            # print(f"Result saved to '{args.output_txt}'")
        except IOError as e:
            print(f"Error writing to output file '{output_txt}': {e}")

    # --- 4. Clean up temporary WAV file ---
    os.remove(temp_wav_path)
    print("Temporary WAV file removed.")


vosk_model_path = r"D:\Vosk\vosk-model-fr-0.6-linto-2.2.0"

if __name__ == "__main__":
    #transcribe_audio(r"C:\MusicOD\Humour\Tanguy Pastureau\Tanguy Pastureau maltraite l'info 2023\2023-10\Tanguy Pastureau - 2023-10-11 - Les politiques aussi font du greenwashing.mp3")

    for filefp in get_all_files(r"C:\MusicOD\Humour\Tanguy Pastureau"):
        if filefp.endswith(".mp3") and "maltraite" in filefp:
            output_txt = filefp.replace(".mp3", ".txt").replace(r"C:\MusicOD\Humour", r"C:\Temp")
            if not file_exists(output_txt):
                transcribe_audio(filefp)
