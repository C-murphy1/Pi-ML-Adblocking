
import numpy as np
from numpy import loadtxt
import re





text_file = open('RawData.txt', encoding='utf8') #opens txt file "RawData.txt"
url_list = text_file.read().split('\n') #reads txt file, createslist, each line is a new element
text_file.close()



# x and y indecies correspond
y = [] #block/forwardlist, 0=blocked, 1=forwarded
X = [] #array of url comonentlists


def split(word):
    return list(word)



def line_to_dataset(list): #Old Function for generating Training data from PiHole output data

    ignore = 0
    
    for item in list:
        newline = item.replace('gravity','',1) # removes "gravity"
        simplified = ''
        if (newline.find(' is ') != -1):
            head, sep, tail = newline.partition(' is ') #removes all text after "is"; used for blocked domains
            simplified = head
        else:
            head, sep, tail = newline.partition(' to ') #removes all text after "to"; used for forwarded domains
            simplified = head

        url_string_array = re.split(r'[ :/()_@?=.-]\s*', simplified) #splits into x cells 
        del url_string_array[0:4] # removes date from line, consistant on all lines 

        if (len(url_string_array) <= 0 ):
            break
            
        if (url_string_array[0] == "blocked"):      #0 = blocked, 1 = forwarded
            y.append('0\n')                                #add 0 tolist
        elif (url_string_array[0] == "forwarded"):
            y.append('1\n')                                #add 1 tolist
        
    
        del url_string_array[0] #removes block/forward from url components
        if(ignore == 0): # does not append ignored value to X list
            combined = ''
            new_char_array = []
            
            for word in url_string_array: #splits words into characters
                new_char_array.append(split(word))
            #print(new_char_array)

            

            for char_list in new_char_array:
                for char in char_list:
                
                    combined += (char + ' ')
            
            X.append(combined + "\n")  # adds list of url compoents to dataset list


        
        ignore = 0


line_to_dataset(url_list)            

text_file = open('TrainingDataX.txt', "r+",encoding='utf8')
text_file.writelines(X) # writes x training data to TrainingDataX.txt
text_file.close()

text_file = open('TrainingDataY.txt', "r+",encoding='utf8')
text_file.writelines(y) # writes y training data to TrainingDataY.txt
text_file.close()

print("Finished")
print(len(url_list))
print(len(X))
