# uni_canteen_announcement
Short python script which finds the canteen meal information from https://www.stw-bremen.de/en/food-and-drink/uni-mensa , convert them into a .mp3 file and play it.

tested on ubuntu 18.04

## How to use:

### required packages
```zsh
pip3 install requests
pip3 install beautifulsoup4
pip3 install DateTime
pip3 install gtts
sudo apt-get update
sudo apt-get install mpg123
```

### run

```zsh
python3 ./mensaVoice.py
```


