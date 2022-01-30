# PaZaR

An SE 101 project to convert math notes into LaTeX.

Here's our demo video:

https://user-images.githubusercontent.com/65367548/151722346-62a1cae5-3a36-4291-a7d1-dfa2f2a1bae0.mp4

## Hardware

The hardware component of the project included connecting a Raspberry Pi with a Pi Camera to a breadboard with control buttons and LEDs for feedback.
Once the picture was taken, it would be sent to the API to handle the symbol recognition and OCR to get the LaTeX code back.

## Running the symbol recognition script

Will be further documented as we move on but here are the general instructions (make sure you have Python 3.7 or newer installed):
```
python3 -m venv ./env
. ./env/bin/activate
pip3 install -r requirements.txt
cd symbol_recognition
python3 identify.py
```
