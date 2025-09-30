# transcribe.py - Audio transcripts of podcasts
#
# 2025-09-22    PV      First version with Gemini help
# 2025-09-23    PV      After detailed tests, use whisper_small with language="fr", fp16=False, patience=2, beam_size=5
# 2025-09-23    PV      Result moved from C:\Temp to D:\AudioDups
# 2025-09-28    PV      Simplified version for DCL
# 2025-09-30    PV      Parametered version

from datetime import datetime
import os
import time
import sys
from pydub import AudioSegment
from common_fs import folder_part, file_exists
from myglob import MyGlobBuilder

group = "DCL-O"

match group:
    case "DCL-O":
        source = r"C:\MusicOD\Humour\David Castello-Lopes\David Castello-Lopes - Europe 1 - Les origines 2020-2023\*\*.mp3"
        search_path = r"C:\MusicOD\Humour"
        replace_path = r"D:\AudioDups\DCL-O"

    case "TP-M":
        source = r"C:\MusicOD\Humour\Tanguy Pastureau\Tanguy Pastureau maltraite l'info *\*\*.mp3"
        search_path = r"C:\MusicOD\Humour"
        replace_path = r"D:\AudioDups\TP-M"
        pass

    case _:
        breakpoint()

# Test MyGlob
# gs = MyGlobBuilder(source).compile()
# for ma in gs.explore():
#     if ma.is_file:
#         print(str(ma.path))
# os._exit(0)

translation_log = os.path.join(search_path, "transcription.log")
temp_wav_path = fr"c:\Temp\temp_transcription_audio_{group}.wav"


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

def my_log(msg: str, skip_line: bool = False):
    # Get the current time
    now = datetime.now()
    # Format the timestamp down to milliseconds
    # %f gives microseconds, so we slice the first 3 digits for milliseconds
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open(translation_log, "a") as file:
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
    try:
        audio = AudioSegment.from_mp3(input_mp3)
        # Convert to mono and set a standard sample rate
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)  # 16kHz is standard for many speech models
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
    print("Start transcription with Whisper small...")
    tstart = time.time()
    transcribed_text = transcribe_with_whisper(temp_wav_path, "small")
    duration = time.time() - tstart
    msg = "Transcription completed in " + str(round(duration, 3)) + 's'
    print(msg)
    my_log(msg)

    # Save transcription to output file
    output_txt = input_mp3.replace(".mp3", ".txt").replace(search_path, replace_path)
    os.makedirs(folder_part(output_txt), exist_ok=True)
    try:
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(transcribed_text)
        # print(f"\nTranscription successful!")
        # print(f"Result saved to '{args.output_txt}'")
    except IOError as e:
        print(f"Error writing to output file '{output_txt}': {e}")

    # --- 4. Clean up temporary WAV file ---
    if file_exists(temp_wav_path):      # Just in case temp file was already deleted in windows explorer, to avoid a crash
        os.remove(temp_wav_path)
    # print("Temporary WAV file removed.")


if __name__ == "__main__":
    gs = MyGlobBuilder(source).compile()
    for ma in gs.explore():
        if ma.is_file:
            filefp = str(ma.path)
            output_txt = filefp.replace(".mp3", ".txt").replace(search_path, replace_path)
            if not file_exists(output_txt):
                # print(output_txt)
                # print(file_part(output_txt))
                # os._exit(0)
                transcribe_audio(filefp)
