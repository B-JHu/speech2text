import json
from datetime import datetime
import os
import sys
import argparse
import speech_recognition as sr

# =======================
# speech2text
# Version: 1.0 (Nov. 29, 2021)
# A command-line tool to turn your speech into JSON notes.
#
# -----------------------
# The 'SpeechRecognition'-library is made available under the 3-clause BSD license. For the license information, see https://github.com/Uberi/speech_recognition/blob/master/LICENSE.txt
# =======================
__version__ = "1.0.0"


# application defaults
OUTPUT_FILENAME = "notes.json"
SR_ENGINE = "pocketsphinx"      # If you change this, please change the 'help='-string in the 'parseCommandLineInputs()'-method!
LANGUAGE = "de-DE"
SAVE_AUDIO = False

# arbitrary stuff for the program; can't be bothered to make them command-line arguments...
SR_TIMEOUT = 5
JSON_INDENT = 3
# ------

def parseCommandLineInputs():
    parser = argparse.ArgumentParser(description=f"A command-line tool to turn your speech into JSON notes.")

    parser.add_argument("-o", "--outfile", default=OUTPUT_FILENAME, help=f"Specify the name of the file the transcribed text is written to (default: '{OUTPUT_FILENAME}').")
    parser.add_argument("-s", "--sr_engine", default=SR_ENGINE, help="Specify the speech recognition engine used to decode the speech. May either be 'pocketsphinx' (default) oder 'google'.")
    parser.add_argument("-l", "--language", default=LANGUAGE, help=f"Specify the language you are dictating in (default: {LANGUAGE}). Must be specified as an RFC5646 language tag (e.g. 'en-GB', 'en-US', 'fr-FR').")
    parser.add_argument("--save_audio", default=False, action="store_true", help=f"If this flag is set, the recording of your voice will be saved to a .wav-file (default: {SAVE_AUDIO}).")

    args = parser.parse_args()
    return args

# ------

def recordVoice(recog: sr.Recognizer, saveAudio: bool) -> sr.AudioData:
    audioData = None

    with sr.Microphone() as audioSource:
        audioData = recog.listen(audioSource, timeout=SR_TIMEOUT)

    if saveAudio:
        currentDateTimeStr = str(datetime.now())
        with open(currentDateTimeStr + ".wav", "wb") as audioOutputFile:
            audioOutputFile.write(audioData.get_wav_data())

    return audioData

def transcribeAudio(recog: sr.Recognizer, audio: sr.AudioData, sr_eng: str, lang: str) -> str:
    spokenText = ""
    
    if sr_eng == "pocketsphinx":
        spokenText = recog.recognize_sphinx(audio, language=lang)
    elif sr_eng == "google":
        spokenText = recog.recognize_google(audio, language=lang)
    else:
        print("Error: Speech recognition engine not supported! Exiting...")
        sys.exit(2)

    return spokenText

def writeDataToFile(fileName: str, text: str):
    previousData = None
    lastDataIndex = -1
    currentDateTimeStr = str(datetime.now())

    # if the file does not exist, create it. Only *then* try to read the JSON data from it.
    if not os.path.exists(fileName):
        with open(fileName, "w") as newFile:
            newFile.write("{\n  \"notes\": []\n}")
            newFile.close()

    with open(fileName, "r") as jsonFile:
        previousData = json.load(jsonFile)
        jsonFile.close()

    # automatically index the data correctly
    try:
        lastDataIndex = previousData["notes"][-1]["index"]
    except Exception:
        pass

    previousData["notes"].append({
        "index": (lastDataIndex + 1),
        "timestamp": currentDateTimeStr,
        "text": text
    })

    with open(fileName, "w") as outputFile:
        outputFile.write(json.dumps(previousData, indent=JSON_INDENT))
        outputFile.close()


# =======
# main
# =======
def main():
    args = parseCommandLineInputs()

    print("Initializing...")
    recog = sr.Recognizer()
    print("\tDone!")

    audio = recordVoice(recog, args.save_audio)
    text = transcribeAudio(recog, audio, args.sr_engine, args.language)

    writeDataToFile(args.outfile, text)

if __name__ == "__main__":
    main()