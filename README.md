# NeuralWaifu (Temporarily - Jarvis) v1.0.4 (very early)
Voice Assistant created using Python and neural networks.
The main project challenges we try to achieve is:
 - 100% offline (no cloud)
 - Open source (full transparency)
 - No data collection (we respect your privacy)

## Neural Networks
Used neural networks:
 - Speech to text (STT):
   - Vosk Speech Recognition Toolkit via Vosk-rs
 - Chat:
   - ChatGPT
 - Text to speech (TTS):
   - Silero TTS

## To run the program(Windows)
For start, you need Git & Python >=3.10.

```
git clone https://github.com/Gleb-a-p/NeuralWaifu.git       // clone repo
cd NeuralWaifu                                              // mv into cloned repo
python -m venv .venv                                        // create .venv
.venv/Scripts/activate.bat                                  // activate .venv
pip install -r requirements.txt                             // install requirements
python main.py                                              // run program
```

## Supported Languages
Currently, only Russian language is supported.

## Author
Popov Gleb

## Newest version
The last commit you can find at this link: https://github.com/Gleb-a-p/NeuralWaifu.
Also, you can see all commit tree and choose any version.

## License
Shield: [![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg

See LICENSE.txt file for more details.
