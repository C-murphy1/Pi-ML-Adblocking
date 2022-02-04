import time
import tensorflow as tf
import tensorflow_datasets as tfds
import re
import numpy as np
import os



filePath = "/var/log/pihole.log" #Pihole log file location 


model = tf.keras.models.load_model("Training/Model/model.keras")

def split(word):
    return list(word)

def isolateURL(item): #Extracts URL from piHole log entry
    url = ''
    if (item.find("blocked") == -1): #Removes all parts of the string besides the URL
        index = item.find("forwarded")
        cut = item[index+10:]
        url = cut[:cut.find(' ')]
    else:
        index = item.find("blocked")
        cut = item[index+8:]
        url = cut[:cut.find(' ')]

    return url

def lineToInput(item): #converts pihole data log entry into a list of characters the make up the URL
        output = ''
        
        url = isolateURL(item)
       
        shortenedUrl = re.sub(r'[ :/()_@?=.-]\s*', '', url)#removes common url dividers such as ":", "/", "."
        shortenedUrl = shortenedUrl[:101] #Removes characters after 100 to keep consistant with model training
        charList = split(shortenedUrl) #splits each url into a list of characters
        output = charList

        print(output)
        return output #Returns a list of characters

encoder = tfds.deprecated.text.TokenTextEncoder.load_from_file("Training/Model/VocabList") #imports tokens file that was generated during the model training

def encode(text):#Returns a list of encoded characters, using the imported encoding scheme

    outputList = [''] * len(text)
    encodedList = [''] * len(text)

    i = 0
    while i < len(text):
        encodedList[i] = encoder.encode(text[i]) #Encoder creates 2d list, characters must be moved into a 1d list
        outputList[i] = encodedList[i][0]
        i += 1
   
    return outputList 

def pad_encoded_text(charList): #Adds 0's to the end of the list so that all inputs to the model are 100 elements in length
    outputList = charList
    length = len(charList)
    if (length < 100):
        for j in range(0, 100 - length):
            outputList.append(0)
    
    return outputList


        


lastLine = None

recentBlocks = [] #an array of strings to keep track of sites that have recently been blocked

while True:
    with open(filePath,'r') as f:
        lines = f.readlines()
    if(len(lines) < 1):
        pass
    elif lines[-1] != lastLine:
        lastLine = lines[-1]

        if (len(lastLine) > 30): #Checks if the link has been used by the model recently, to avoid some repitition in common URL's
            url = isolateURL(lastLine)
            recentLink = False
            for item in recentBlocks:
                if (url == item):
                    recentLink = True


            if (not recentLink):#Only runs a prediction if the link has not been seen recently
                formatted_input = pad_encoded_text(encode(lineToInput(lastLine))) 
                print(formatted_input)
                
                prediction = model.predict([formatted_input])
        
        

                if(np.argmax(prediction[0]) == 1): # if model decides url is ok
                
                    print(url)
                    print('Prediction: Good')
                    
                else: # if model decides url is bad

                    print(url)
                    print('Prediction: Bad')

                    blacklist_link = isolateURL(lastLine) #append to pi blacklist using get_url
                    os.system('pihole -b ' + blacklist_link)

            recentLink = False

            if (len(recentBlocks) >= 100): #Resets Recent blocks list after 100 entries
                recentBlocks = []
            
           
        
        print(lines[-1])
    time.sleep(.1)



















