"""
Calculates color histogram for a folder with (i-frame) images. 

input:
    - folder with i-frame images. Extension: .jpg
    
Output:
    - "histograms"
        - type: dictionary
        - keys: image names
        - value: color histogram 
"""


import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# Function to calculate the histogram of an image
def calculate_histogram(image_path):
    """
    Calculate and return the color histogram of the image.
    
    Args:
    - image_path: The path to the image file.
    
    Returns:
    - A tuple of histograms for each color channel (red, green, blue).
    """
    with Image.open(image_path) as img:
        # Convert the image to RGB if it's not
        img = img.convert('RGB')
        
        # Calculate the histogram for each color channel
        red_hist = np.array(img.histogram()[0:256])
        green_hist = np.array(img.histogram()[256:512])
        blue_hist = np.array(img.histogram()[512:768])
        
        return red_hist, green_hist, blue_hist
    
def plot_histogram(image_path):
    """
    Calculate and plot the color histogram of the image.
    
    Args:
    - image_path: The path to the image file.
    """
    with Image.open(image_path) as img:
        # Convert the image to RGB
        img = img.convert('RGB')
        
        # Calculate the histogram for each color channel
        red_hist = np.array(img.histogram()[0:256])
        green_hist = np.array(img.histogram()[256:512])
        blue_hist = np.array(img.histogram()[512:768])
        
        # Setting up the histogram plot
        plt.figure(figsize=(10, 4))
        plt.plot(red_hist, color='red')
        plt.plot(green_hist, color='green')
        plt.plot(blue_hist, color='blue')
        plt.title('Color Histogram')
        plt.xlabel('Bin')
        plt.ylabel('Frequency')
        plt.show()

# Dictionary to hold histograms for each image
histograms = {}

# Folder containing the i-frame images for a video.
video = "DS782_722374D-DGS00Z03UDY" 
folder = f"../../data/4_i_frames/{video}"

# Iterate through the files in the folder
for filename in os.listdir(folder):
    if filename.endswith(".jpg"):
        # Construct the full path to the file
        file_path = os.path.join(folder, filename)
        
        # Calculate the histogram
        histograms[filename] = calculate_histogram(file_path)

#print(histograms['split_0_41_iframe_001.jpg'])

# At this point, `histograms` contains the color histograms for each image
print(f"Calculated histograms for {len(histograms)} images.")


