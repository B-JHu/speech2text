# speech2text

A command-line tool to turn your speech into JSON notes.

## Description

Uses the 'SpeechRecognition'-library to

​	a) Record audio (hopefully a voice:) ) and save this recording at the user's demand

​	b) Transcribe what is being said in the recording and

​	c) Write the transcript into a .json-file, timestamped and indexed

The resulting .json-file will consist of an entry/multiple entries in the following format:

```json
{"index": int, timestamp: datetime, text: str}
```

with "notes" being the root element

----

I got the inspiration for this mini-"project" from Kalle Halden's YouTube-video ["I Built Your Strange Python Automation Ideas"](https://www.youtube.com/watch?v=_5pH_tr7uN0).

## Requirements

- **Python** 3.9+
- **PyAudio** 0.2.11+
- **PocketSphinx** (if you want to use the *default* 'pocketsphinx' option; [Link]())
  + additional language packages (if you want to another language than US English)

## Documentation/Options

```shell
usage: speech2text_terminal.py [-h] [-o OUTFILE] [-s SR_ENGINE] [-l LANGUAGE] [--save_audio]
```

arguments:

```shell
-o OUTFILE, --outfile OUTFILE
Specify the name of the file the transcribed text is written to (default: 'notes.json'). 
```

If the file does not exist, a new one will be created. If it does exist (from previous recordings), the speech data will be appended to the JSON file. If it does exist, but the file does not follow the specified format, the program will throw an error and exit.

----

```shell
-s SR_ENGINE, --sr_engine SR_ENGINE
Specify the speech recognition engine used to decode the speech. May either be 'pocketsphinx' (default) oder 'google'.
```

Keep in mind that option 'pocketsphinx' requires pocketsphinx to be installed on your system (and additional language packets, if you so desire), and 'google' requires an internet connection.

----

```shell
-l LANGUAGE, --language LANGUAGE
Specify the language you are dictating in (default: 'de-DE'). Must be specified as an RFC5646 language tag (e.g. 'en-GB', 'en-US', 'fr-FR').
```

----

```
--save_audio
If this flag is set, the recording of your voice will be saved to a .wav-file (default: False).
```

The .wav-file will have the current datetime as its filename, and will be saved into a folder called 'voice_recordings'.

## License

This code is licensed under the GNU General Public License v3.0.

This code makes use of the 'SpeechRecognition'-library from Anthony Zhang (Uberi). It is made available under the 3-clause BSD license. See [this link](https://github.com/Uberi/speech_recognition/blob/master/LICENSE.txt) for the license information.