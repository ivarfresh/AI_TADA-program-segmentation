"""
Generates keyframes/i-frames for each shot video. For more info on i-frames, see:
- https://en.wikipedia.org/wiki/Video_compression_picture_types

Input:
    - MoviePY segmented shot videos.
    - Extension: .mp4

Output:
    - I-frame .jpg images 

Note:
    - there can be multiple images for one shot video. 
    
"""

import os
import subprocess


def process_videos(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through the video files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(input_folder, filename)
            output_path_pattern = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_iframe_%03d.jpg")
    
            # Use FFmpeg to extract I-frames
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vf", "select='eq(pict_type,PICT_TYPE_I)'",
                "-vsync", "vfr",
                output_path_pattern
            ]
    
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
            # if FFMPEG failed, print the error
            if process.returncode != 0:
                print(f"Error extracting I-frames for {filename}: {process.stderr.decode()}")
            else:
                print(f"I-frames extracted for {filename}.")
    
    print("I-frame extraction completed.")
    
    
def main():
    # Input and output folder containing video files; adjust as needed.
    
    video = "DS782_722374D-DGS00Z03UDY"
    input_folder = f"../../data/3_MoviePy_segmentation/{video}"
    output_folder = f"../../data/4_i_frames/{video}"
    
    process_videos(input_folder, output_folder)
    
if __name__== '__main__':
    main()
