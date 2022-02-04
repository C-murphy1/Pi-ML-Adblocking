# Pi-ML-Adblocking
The goal of this project is to have a machine learning model to work alongside the popular Ad-blocking system PiHole to allow it to detect new advertisement URL's and add them to its blacklist. This is a Python based project that uses Tensorflow's Keras api to handle the training and predictions of the models.

## Training a Model

Training a Model requires that you have Python, Tensorflow, Tensorflow Datasets, and NumPy installed.
It is also not recommended to train the model on a RaspberryPi due to its slower speed compared to an average desktop computer.

The "URLformat.py" and "ModelTrain.py" files are used to train a new model based on a given dataset. It is recommended to create a new dataset for modern website URL's, however, there is a pretrained verion of the model. If you wish to use the pretrained model simply copy the files from the "ModelPreTrained" folder into the "Model folder", and skip to the section about deploying the code on a RaspberryPi.

The process of training the model is fairly straightforward. The first step is to create a dataset of URL's that should be blocked and URL's that should be allowed. There are numerous sources of data online with lists that contain this information. As more websites are created these URL databases will also change, so it is recommended to find an up-to-date source for collecting lists of website URL's to make the model as effective as possible.

The dataset should be copied into the Training/RawData.txt file, and follow the rules below:

~~~~
# Formatting in the program follows these Rules/Assumptions
#   1.) Dataset is already randomized
#   2.) Each Url is preceeded by a "1 " or "0 " to create the list
#           ex:
#               "1 google.com" (indicates that google.com is a website that should not be blocked)
#               "0 google.com" (indicates that google.com is a website that should be blocked)
#   3.) Url's over 100 characters will be truncated
~~~~

Typically the easiest way to create the dataset is to import seperate "blocked" and "allowed" lists into a tool such as Microsoft Excel and merge 1/0 to the beginning of the text for each line, Then combine the two lists and randomize the order afterwards.

Once the dataset has been pasted into "RawData.txt" run the "URLFormat.py" file using python. This will generate two lists in "TrainingDataX.txt", and "TrainingDataY.txt" that are formatted for use by the model in the next step.

Once the "URLFormat.py" script is finished, you can run "ModelTrain.py" which will take the data and begin to train the model. If you have experience with Tensorflow/Keras, feel free to tweak the default model settings as you see fit before running the script, otherwise the default setup should work fine for this application.

The model will be saved in the "Model" folder, as "model.keras" and will also include a "VocabList" tokens file that keeps track of the text encoding. The tokens file is necesary for running the trained model.

## Running The Code on a RaspberryPi

Running the code on a RaspberryPi requires that you have PiHole, Tensorflow, Tensorflow Datasets, and NumPy installed on the RaspberryPi.

The Easiest way to get the model running on the Pi is to clone the repository onto the Pi, then transfer the files from the "Training/Model" folder on your PC, to the same foler on the Pi.

In order for the code to function properly PiHole needs to be configured to have the log file enabled. Some privacy settings may prevent PiHole from using the log file, which is the way that the current version of this program interfaces with PiHole.

After the setup is done, you can run the "Run.py" script and the model should begin to filter through URL requests. Any links the the model determines are adverisments will be added to be PiHole blacklist.

To run the program in the background, I will typically install "Screen" on the RaspberryPi and enter a Screen session before running the code, Otherwise the Pi could also be configured to run the program at startup.





