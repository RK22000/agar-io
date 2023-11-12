# AGARIObot

## Setup

### Linux
Setup conda: `conda env create -f environment.yml`
 
Dependencies: `sudo apt-get install wmctrl scrot`

Download [eng.traineddata](https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata) to the root folder: `wget https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata`

## Run

Start the agar.io game in a browser window and enter the name. Then run the bot:
`python agario_bot.py`

You can start in bot control mode of manual control.
Bot control will attempt to find the star button and start the game.
Press escape to stop the recording.
Press shift to switch from bot to manual control.