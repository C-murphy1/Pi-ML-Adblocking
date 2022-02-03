import tensorflow as tf
import tensorflow_datasets as tfds
import os
import numpy as np



optimizer = tf.keras.optimizers.Adamax(0.001)
optimizer.learning_rate.assign(0.05) 

text_file = open("TrainingDataY.txt") 
txt_listy = text_file.readlines() #Reads formatted Training data from "TrainingDataY.txt" into a list
text_file.close()

listy = []

for i in range(0,len(txt_listy)): # Removes newline characters
    txt_listy[i] = txt_listy[i].replace('\n','')

for i in range(0,len(txt_listy)): #converts txt_listy into a list of integers
    if (txt_listy[i] == '0'):
        listy.append(0)
    else:
        listy.append(1)




text_file = open("TrainingDataX.txt",encoding='utf8')
listx = text_file.readlines() #Reads formatted Training data from "TrainingDatax.txt" into a list
text_file.close()

for x in range(0,len(listx)): #Removes newline characters
    listx[x] = listx[x].replace('\n','')


#NEED NEW METHOD OF TOKENIZING
tokenizer = tfds.deprecated.text.Tokenizer() 
#tokenizer = tfds.features.text.Tokenizer() #Creates tokenizer object to assign numeric values to all characters in the training data
vocab_size = 0


vocabulary_set = set()
for text in listx:
  tokens = tokenizer.tokenize(text)
  vocabulary_set.update(tokens)

vocab_size = len(vocabulary_set) + 2 #Adds 1 to account for any characters missing from training set. This removes a crash caused when a trained model encounters a character missing from its training data

encoder = tfds.deprecated.text.TokenTextEncoder(vocabulary_set) 
#encoder = tfds.features.text.TokenTextEncoder(vocabulary_set)

def encode(text):
  encoded_text = encoder.encode(text)
  return encoded_text

for x in range(0, len(listx)):
    item_value = encode(listx[x]) #Uses encoding pattern created by the tokenizer to replace all characters in the dataset with numbers
    item_length = len(item_value)
    
                              #Max length of an individual datapoint is 100 characters.
    if (item_length < 100):   #Adds 0's to the end of each entry to make each datapoint the same length for training.
        for j in range(0, 100 - item_length):
            item_value.append(0)
    listx[x] = item_value

encoder.save_to_file('Model\VocabList') 

X = np.array(listx)
y = np.array(listy)



#Code below defines the model, optimizer, and layers used to categorize the dataset
#
#The model is trained on half of the dataset, while the other half is used to test the model during training
#These model settings can be cmodified to improve accuracy, but larger models may cause issues when transferred to a RaspberryPi
#

model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(vocab_size, 32))

model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(16)))

model.add(tf.keras.layers.Dense(16,activation='relu'))

model.add(tf.keras.layers.Dense(2,activation='softmax'))

model.compile(optimizer=optimizer,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                metrics=['accuracy'])

model.fit(X,y,epochs=5,batch_size=64,validation_split=0.5)


model.save("Model\model.keras")






















