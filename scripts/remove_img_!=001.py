"""
Removes all I-frames which do not have number 001. To ensure that we only have one keyframe/ video.

(this script is probably not necessary, was just to test) 
"""

import os

# Folder containing the images
folder = "../data/4_i_frames_FFMPEG_001"

# Iterate through the files in the folder
for filename in os.listdir(folder):
    if not filename.endswith(".jpg"):
        continue  # Skip files that are not JPEG images
    
    # Split the filename to extract the final number part
    name_parts = filename.split('_')
    final_number = name_parts[-1].split('.')[0]  # Remove the file extension and get the final number
    
    # Check if the final number is not '001'
    if final_number != "001":
        # Construct the full path to the file
        file_path = os.path.join(folder, filename)
        
        # Remove the file
        os.remove(file_path)
        print(f"Removed: {filename}")

print("Processing completed.")
