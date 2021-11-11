import numpy as np 
from tensorflow import keras
from PIL import Image 

# Build the lookup table of symbols 

labels_id = {}
rev_label_lookup = {}
with open("labels.txt", "r") as file:
    for line in file:
        name, index = line.split()
        index = int(index)
        labels_id[name] = index
        rev_label_lookup[index] = name 

# Load model 
model = keras.models.load_model("model")

# Load image + do a little bit of image processing
test_image = np.array(Image.open("Sample Pictures/subset.png").convert("L").resize((40,40)))
processed = (256 - test_image.astype("float32")) / 256

# Ideally this shouldn't be needed as soon as we start tweaking the image processing
for _ in range(5):
    background = min(min([j for j in i if j > 0] or [0]) for i in processed)
    for i in range(40):
        for j in range(40):
            processed[i][j] = max(0, processed[i][j] - background)
processed = np.expand_dims(processed, 0)

# Returns the K symbols that are most likely to be the one in the picture 
# Every entry is in the form (certainty, name)
def identify(picture, K = 15):
    output = model.predict(picture)[0]
    candidates = sorted([
        (certainty, rev_label_lookup[ind]) for ind, certainty in enumerate(output)
    ], reverse = True)
    return candidates[:K]

print("Most likely symbols:")
for certainty, name in identify(processed):
    print("[%.5f] %s" % (certainty, name))
