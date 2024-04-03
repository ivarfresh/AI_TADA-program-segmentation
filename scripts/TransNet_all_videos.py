"""
Script Description:
This script runs the TransNetV2 model on a folder with videos and determines all the shot boundaries 
for each video. 

Usage:
Ensure the 'video_directory' variable is set to the path where your video files are located, and 
'script_path' points to the location of the transnetv2.py script. Run this script in a Python environment 
where subprocess is available. The script will process all .mxf and .mp4 files in the specified directory 
that do not already have an associated .mxf.scenes.txt file.


Input:
    - Folder containing videos: .mxf or .mp4

Output: 
    - {movie_name}.scenes.txt:
            - each row represents a shot
            - the first number is the start frame of the shot, the second number is the end frame. 
    - {movie_name}.predictions.txt
            - each row represents a frame. 
            - For each frame, gives the prediction that the frame is a shot_start_frame (left number)
            and the prediction that it is a shot_end_frame (right number)
    
"""

import os
import subprocess

# Directory where your video files are stored
video_directory = "../data/0_videos/21_08_2023/mxf"

# Path to the Python script you want to run on each video
script_path = "../TransNet_model/inference/transnetv2.py"

# List all files in the video directory that end with .mxf or .mp4
video_files = [f for f in os.listdir(video_directory) if f.endswith('.mxf') or f.endswith('.mp4')]

# Iterate over each video file and run the script
for video_file in video_files:
    movie_name = os.path.splitext(video_file)[0]  # Extract the movie name without its extension
    
    # Check if {movie_name}.mxf.scenes.txt already exists
    scenes_file_path = os.path.join(video_directory, f"{movie_name}.mxf.scenes.txt")
    if os.path.exists(scenes_file_path):
        print(f"Skipping {video_file} as {scenes_file_path} already exists.")
        continue  # Skip this file and move to the next one in the loop

    # If the scenes file doesn't exist, proceed with processing
    video_path = os.path.join(video_directory, video_file)
    # Construct the command to run the script on the video
    command = f"python {script_path} {video_path}"
    # Execute the command
    subprocess.run(command, shell=True)
    print(f"Processed {video_file}")

print("All videos have been processed.")
