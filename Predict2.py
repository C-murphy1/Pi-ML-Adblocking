import time
import tensorflow as tf
import tensorflow_datasets as tfds
import re
import numpy as np
import os


#filePath = 'T:\CodingStuffs\Python\ReadTest.txt' #for laptop testing
filePath = '/var/log/pihole.log' #for use in pihole


#formatted_input = []
recent_blocks = ''

#/home/pi/Blocker/predict.keras for use in pihole
#T:\CodingStuffs\Python\predict.keras for laptop testing
model = tf.keras.models.load_model("/home/pi/Blocker/predict.keras")

def split(word):
    return list(word)


def line_to_dataset(item):

    
        newline = item.replace('gravity','',1) # removes "gravity"
        simplified = ''
        if (newline.find(' is ') != -1):
            head, sep, tail = newline.partition(' is ') #removes all text after "is"; used for blocked domains
            simplified = head
        elif(newline.find(' to ') != -1):
            head, sep, tail = newline.partition(' to ') #removes all text after "to"; used for forwarded domains
            simplified = head
        else:
            head, sep, tail = newline.partition(' from ') #removes all text after "from"; used for reply domains
            simplified = head

        #print("Value of simplified is ")
        #print(simplified)


        url_string_array = re.split(r'[ :/.-]\s*', simplified) #splits into x cells 
        del url_string_array[0:6] # removes date from line, consistant on all lines


        #print("Value of url_string_array is ")
        #print(url_string_array)

        if (len(url_string_array) <= 0 ):
           pass

        else:
            del url_string_array[0]
            output = []
            new_char_array = []
            
            for word in url_string_array: #splits words into characters
                new_char_array.append(split(word))
            print(new_char_array)

            

            for char_list in new_char_array:
                for char in char_list:
                    output.append(char)
            
            #print(url_string_array)
            print(output)
            return output

#T:\CodingStuffs\Python\VocabList for laptop testing
#/home/pi/Blocker/VocabList
encoder = tfds.features.text.TokenTextEncoder.load_from_file("/home/pi/Blocker/VocabList")

def encode(text):
    #print("Value of Text array is ")
    #print(text)
    temp_array = []
    output_array = []
    
    if(len(text) <=0):
        pass
    else:

        for x in range(0,len(text)): # text is an array of strings

            if(text[x] != ''):
                encoded_text = encoder.encode(text[x]) #appended encoded_text number are in 1 cell arrays?, remove from inner array with loop if issue
                if(encoded_text != ''):
                    temp_array.append(encoded_text)
        for x in range(0,len(temp_array)):
            if (len(temp_array[x]) != 0):
                output_array.append(temp_array[x][0])

    #print(output_array)
    return output_array

def pad_encoded_text(text_array):
    temp_array = text_array
    output_array = []
    text_length = len(temp_array)
    if ( text_length < 100):
        for j in range(0, 100 - text_length):
            temp_array.append(0)
    #output_array.append(temp_array)
    return temp_array

        

def get_url(line):
    shortened = ''
    head, sep, tail = line.partition(': ')
    shortened = tail

    if (shortened.find(' is ') != -1):
        head, sep, tail = shortened.partition(' is ') #removes all text after "is"; used for blocked domains
        shortened = head
    elif(shortened.find(' to ') != -1):
        head, sep, tail = shortened.partition(' to ') #removes all text after "to"; used for forwarded domains
        shortened = head
    else:
        head, sep, tail = shortened.partition(' from ') #removes all text after "from"; used for reply domains
        shortened = head
    
    shortened = shortened.replace('gravity ','',1)
    shortened = shortened.replace('blocked ','',1)
    shortened = shortened.replace('query[A] ','',1)
    shortened = shortened.replace('query[AAAA] ','',1)
    shortened = shortened.replace('reply ','',1)
    shortened = shortened.replace('forwarded ','',1)
    shortened = shortened.replace('cached ','',1)
    shortened = shortened.replace('exactly ','',1)
    shortened = shortened.replace('blacklisted ','',1)


    print('The Value of shortened is: ')
    print(shortened)
    return shortened











lastLine = None

while True:
    with open(filePath,'r') as f:
        lines = f.readlines()
    if(len(lines) < 1):
        pass
    elif lines[-1] != lastLine:
        lastLine = lines[-1]

        
        formatted_input = pad_encoded_text(encode(line_to_dataset(lastLine))) 
        #print(formatted_input)
        #
        prediction = model.predict([formatted_input])
        
        #print(np.argmax(prediction[0]))

        if(np.argmax(prediction[0]) == 1): # if model decides url is ok
            if(recent_blocks.find(lastLine) == -1):

                print('Prediction: Good')
               

                #append to pi whitelist using get_url
                #whitelist_link = get_url(lastLine)
                #os.system('pihole -w ' + whitelist_link)

                recent_blocks += lastLine
        else: # if model decides url is bad
            if(recent_blocks.find(lastLine) == -1):

                print('Prediction: Bad')

                #append to pi blacklist using get_url
                blacklist_link = get_url(lastLine)
                os.system('pihole -b ' + blacklist_link)


                recent_blocks += lastLine
            

        #print('The vlaue of recent_blocks is: ')
        #print(recent_blocks)   
        
        print(lines[-1])
    time.sleep(.1)



















