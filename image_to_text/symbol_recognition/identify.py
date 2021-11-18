import numpy as np 
from tensorflow import keras
from PIL import Image 
import os 

# Build the lookup table of symbols 
relative_path = os.path.join(os.path.dirname(__file__), "labels.txt")

labels_id = {}
rev_label_lookup = {}
with open(relative_path, "r") as file:
    for line in file:
        name, index = line.split()
        index = int(index)
        labels_id[name] = index
        rev_label_lookup[index] = name 

# Load model 
model = keras.models.load_model(os.path.join(os.path.dirname(__file__), "model.h5"))

# Utility function to add a white border around a given picture
def add_margin(img, top, right, bottom, left):
    # Get dimension of picture and calculate new picture size
    width, height = img.size
    new_width = width + right + left
    new_height = height + top + bottom
    # (255, 255, 255) --> White
    padded = Image.new(img.mode, (new_width, new_height), (255, 255, 255))
    padded.paste(img, (left, top))
    return padded

#  Uses the pre-trained model to predict and process the image of a latex symbol
#  [Input]: 
#    img - A 2d numpy array with RGB values from [0, 255]
#    K - The K most certain latex symbols (default is 15)
#  [Output]:
#    A tuple containing the following:
#       A 2d numpy array after processing
#       A list of items each with (certainty, name) denoting the latex symbol and how certain the model is

def identify(img, K = 15):
    img = Image.fromarray(img)
    img = add_margin(img, 10, 10, 10, 10).convert("L")
    
    # Load image + do a little bit of image processing
    test_image = np.array(img.resize((40,40)))
    processed = (255 - test_image.astype("float32")) / 255

    # Ideally this shouldn't be needed as soon as we start tweaking the image processing
    for _ in range(20):
        background = min(min([j for j in i if j > 0] or [1e8]) for i in processed)
        for i in range(40):
            for j in range(40):
                processed[i][j] = max(0, processed[i][j] - background)
    processed = np.expand_dims(processed, 0)
    
    # Returns the K symbols that are most likely to be the one in the picture 
    # Every entry is in the form (certainty, name)
    def identify(picture, K):
        output = model.predict(picture)[0]
        candidates = sorted([
            (certainty, rev_label_lookup[ind]) for ind, certainty in enumerate(output)
        ], reverse = True)
        return candidates[:K]
    
    #print("Most likely symbols:")
    #for certainty, name in result:
    #    print("[%.5f] %s" % (certainty, name))
    
    # Return the processed picture (for debugging purposes) along with the K=15 most likely symbols
    return processed[0], identify(processed, K)