# AGARIObot

## Setup

### Linux
Setup conda: `conda env create -f environment.yml`
 
Dependencies: `sudo apt-get install scrot`

Download [eng.traineddata](https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata) to the root folder: `wget https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata`

## Run

Start the agar.io game in a browser window and enter the name. Then run the bot:
`python agario_bot.py`

You can start in bot control mode of manual control.
Bot control will attempt to find the star button and start the game.
Press escape to stop the recording.
Press shift to switch from bot to manual control.

## Todos

- [x] Convert agario into a gym environmnet
- [x] Train a sb3 RL agent
- [ ] Train offline
- [ ] Use a programmatic browser interface instead of OCR
- [x] Capture the correct window rectangle
- [x] Speedup the screenshot capture
- [x] Fix death detection
- [x] Automatic episode restart
- [ ] Add reward on score change
- [ ] Reliable end of game reward parsing
- [ ] Learn by crashing implementation
- [ ] Imitation learning baselines
- [ ] Handle game crashes