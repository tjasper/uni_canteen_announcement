import requests 
from bs4 import BeautifulSoup 
from gtts import gTTS 
from datetime import datetime
import os 

numbers_to_string = {0:"null", 1:"eins", 2:"zwei", 3:"vier", 4:"vier"}

bellFile = "sounds/Hand-bell-short-ring2.mp3"
announcementFile = "sounds/Essensansgae.mp3"

def textFilter(inputText):
    text = str(inputText)[47:-5] # remove html stuff
    
    #remove html-tags from text
    doSearch = True # search more then one time if we find a tag
    while doSearch:
        doSearch = False
        indicators = [None, None]
        for i in range(len(text)):
            if indicators[0] is None and text[i] is '<':
                indicators[0] = i
            else:
                if text[i] is '>':
                    if indicators[1] is not None:
                        indicators[1] = i 
                        break
                    else:
                        indicators[1] = i
        if indicators[1] is not None:
            # remove identified tags
            text = text[:indicators[0]] + text[indicators[1]+1:]  
            doSearch = True # search one more time               
    text = text.replace("* * *", "mit")
    text = text.replace("&gt;", "& ")
    text = text.replace("&lt;", " ")
    text = text.replace("&amp;", "& ")
    return text

def getFoodText(index): 
    global numbers_to_string

    # the target we want to open     
    url='https://www.stw-bremen.de/de/mensa/uni-mensa'
      
    #open with GET method 
    resp=requests.get(url)

    if resp.status_code==200: 
        soup=BeautifulSoup(resp.text,'html.parser')
        results = soup.findAll("td", attrs={"class":"field field-name-field-description"})
        return "Ausgabe " + numbers_to_string[index+1] + ". " + textFilter(results[index]) + ".      "
    else:
        return "Ausgabe " + numbers_to_string[index+1] + ". keine Angaben.   " 

def createMP3(inputText, language = 'de'):
    global announcementFile
    audio = gTTS(text=inputText, lang=language, slow=False)
    audio.save(announcementFile) 

def playAudio(bell=False):
    global bellFile, announcementFile
    if bell:
        os.system("mpg123 " + bellFile)
    else:
        os.system("mpg123 " + announcementFile)

def saySingleFood(index):
    text = getFoodText(index)
    #print(text)
    createMP3(text)
    playAudio()

def getMensaStatus():
    now = datetime.now()
    if now.isoweekday() <= 5:
        opening_time = now.replace(hour=11, minute=30, second=0, microsecond=0)
        mid_time = now.replace(hour=13, minute=00, second=0, microsecond=0)
        closing_time = now.replace(hour=14, minute=00, second=0, microsecond=0)
        if now <= opening_time:
            return ("Die Mensa öffnet in " + str(int(abs(divmod((now - opening_time).total_seconds(), 60)[0]))) + " Minuten. ", True)
        elif now > mid_time and now < closing_time:
            return ("Die Mensa schließt in " + str(int(abs(divmod((now - closing_time).total_seconds(), 60)[0]))) + " Minuten. ", True)
        elif now <= mid_time and now > opening_time:
            return ("Die Mensa hat jetzt geöffnet. ", True)
        elif now > closing_time:
            return ("Die Mensa hat jetzt geschlossen. ", False)
    else:
        return ("Die Mensa hat heute geschlossen. ", False)

def sayFood1234():
    food_list = [0,1,2] # indices of parsed website
    text = getMensaStatus()[0]
    if getMensaStatus()[1]:
        for i in food_list:
            text += getFoodText(i)
    print(text)
    createMP3(text)
    playAudio(True)
    playAudio()

sayFood1234()

