"""
Use this file instead of the "color_hists.py".
Use this if you want to create color histograms for all frames in the shot videos, 
instead of only the I-frames/keyframes. 

Input:
    - Folder containing segmented shot videos.
    
Output:
    - Color histograms saved in numpy array file (color_histograms.npy)

"""


import os
import cv2
import numpy as np
import json
import matplotlib.pyplot as plt

# Function to calculate the histogram of an image
def calculate_histogram(image):
    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Calculate the histogram for each color channel
    red_hist = np.histogram(image[:, :, 0], bins=256, range=(0, 256))[0]
    green_hist = np.histogram(image[:, :, 1], bins=256, range=(0, 256))[0]
    blue_hist = np.histogram(image[:, :, 2], bins=256, range=(0, 256))[0]
    
    return red_hist.tolist(), green_hist.tolist(), blue_hist.tolist()

# Function to extract frames from video, calculate histograms, and save them
def process_video(video_path, histograms, video_name):
    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # No more frames to read
            
        # Calculate the histogram for the frame
        histograms[f"{video_name}_frame_{frame_num}.jpg"] = calculate_histogram(frame)
        frame_num += 1
        print(f"Processed frame {frame_num}/{total_frames} of {video_name}")
        
    cap.release()

# Save histograms to a file using NumPy's binary format
def save_histograms_np(histograms, filepath):
    # Convert the histograms dictionary to a list of tuples and then to a NumPy array
    histograms_array = np.array(list(histograms.items()), dtype=object)
    # Save the NumPy array to a binary .npy file
    np.save(filepath, histograms_array)


# Folder containing the videos
folder = "../data/3_MoviePy_segmentation/DS782_722374D-DGS00Z03UDY"

# Dictionary to hold histograms for each frame in each video
histograms = {}

# Iterate through the files in the folder
for filename in os.listdir(folder):
    if filename.endswith(".mp4"):  # Assuming the videos are in mp4 format
        # Construct the full path to the file
        video_path = os.path.join(folder, filename)
        print(f'Processing video: {filename}')
        
        # Process the video
        process_video(video_path, histograms, os.path.splitext(filename)[0])

# Save the histograms to a file
histograms_filepath = os.path.join(folder, "color_histograms.npy") #Change this path!
save_histograms_np(histograms, histograms_filepath)

print(f"Calculated histograms for {len(histograms)} frames.")
print(f"Histograms saved to {histograms_filepath}.")

