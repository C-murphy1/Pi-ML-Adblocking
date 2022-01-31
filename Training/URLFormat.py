
import numpy as np
from numpy import loadtxt
import re




# Formatting in the program follows these Rules/Assumptions
#   1.) Dataset is already randomized
#   2.) Each Url is preceeded by a "1" "0" to create the corresponding list
#           ex:
#               "1 google.com" (indicates that google.com is a website that should not be blocked)
#               "0 google.com" (indicates that google.com is a website that should be blocked)
#   3.) Url's over 100 characters will be truncated



text_file = open('RawData.txt', encoding='utf8') 
url_list = text_file.read().split('\n') #Reads "RawData.txt" into a list.
text_file.close()



# x and y list indecies refer to the same url
y = [] #block/forward list, 0=block link, 1=forward link
x = [] #array of url's with spaces between each character 

def split(word): #splits a word into a list of characters
    return list(word)



def lineToDatasets(list): #Takes data from txt file and formats it to prepare for training

    for url in list:
        if (len(url) >=  5): #skips URL lines that are shorter than 5 characters
            shortenedUrl = url[:101] #removes trailing spaces, and limits size to 100 characters
            shortenedUrl = re.sub(r'[ :/()_@?=.-]\s*', '', shortenedUrl)#removes common url dividers such as ":", "/", "."

            charList = split(shortenedUrl) #splits each url into a list of characters

            y.append(charList[0] + "\n") #adds the block/forward value to the y dataset list
            del charList[0] #remoces block/ofrward value from the x dataset line

            line = ""
            for char in charList: #combines list of characters back into one string and appends to the x list
                line += (char + ' ')
            x.append(line + "\n")
    

lineToDatasets(url_list)            

text_file = open('TrainingDataX.txt', "r+",encoding='utf8')
text_file.writelines(x) # writes x training data to TrainingDataX.txt
text_file.close()

text_file = open('TrainingDataY.txt', "r+",encoding='utf8')
text_file.writelines(y) # writes y training data to TrainingDataY.txt
text_file.close()

print("Finished")
print("Training Set Contains: " + str(len(x)) + " Entries")

