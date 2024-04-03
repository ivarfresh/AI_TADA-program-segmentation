"""
This script processes video annotations for a specific video file using ELAN (Eudico Linguistic Annotator) format.
It performs the following tasks:
1. Loads a video file and its corresponding ELAN (.eaf) annotation file.
2. Extracts shot vectors (scenes) from the scenes.txt file.
3. Adds annotations for each shot (scene boundary) in the video.
4. Saves the modified annotations back into an ELAN file and links the video file to these annotations.

Dependencies:
- pympi: For handling ELAN files.
- moviepy: For video processing.
- A custom module 'read_elan_file_shots' for extracting shot vectors from the ELAN file.

Usage:
Adjust the base directory, video date folder, and video file name as per your project requirements.
Run the script to process the annotations and link them with the corresponding video file.

Note: 
    - If you run it multiple times on an existing ELAN file, it will add the same annotations multiple times.
    - After running this script, you still have to manually connect the videos to the .eaf files in ELAN.

"""

import os
from os.path import exists
from pympi.Elan import Eaf
from moviepy.editor import VideoFileClip
from read_elan_file_shots import get_shot_vector

# Function to add shot annotations to the EAF file
def add_annotations(eaf, shot_vector, frame_rate):
    tier_id = "Scene Boundaries"
    if tier_id not in eaf.get_tier_names():
        eaf.add_tier(tier_id)

    # Iterate through shot vectors and add annotations to the EAF file
    for start_frame, end_frame, _ in shot_vector:
        start_time = int(start_frame / frame_rate * 1000)
        end_time = int(end_frame / frame_rate * 1000)
        eaf.add_annotation(tier_id, start_time, end_time, value="Inter-program")
    
# Function to process a single video file
def process_video(base_dir, video_file_name, video_date_folder, transnet_folder, annotation_files_folder):
    video_file_path = os.path.join(base_dir, video_date_folder, f"{video_file_name}.mxf")
    new_folder_path = os.path.join(base_dir, annotation_files_folder, video_file_name)

    # Create a new folder for each video file
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Created new folder: {new_folder_path}")

    # Path for the new EAF file inside the new folder
    eaf_file_path = os.path.join(new_folder_path, f"{video_file_name}.eaf")

    # Create a new EAF file if it does not exist
    if not os.path.exists(eaf_file_path):
        eaf = Eaf()
        eaf.to_file(eaf_file_path)
        print(f"Created new EAF file: {eaf_file_path}")
    else:
        eaf = Eaf(eaf_file_path)

    # Load the video file and get its frame rate
    video = VideoFileClip(video_file_path)
    frame_rate = video.fps

    # Load or create the shot vector
    shot_vector_file_path = os.path.join(base_dir, transnet_folder, f"{video_file_name}.mxf.scenes.txt")
    shot_vector = get_shot_vector(eaf_file_path, shot_vector_file_path)

    # Add shot annotations to the EAF file
    add_annotations(eaf, shot_vector, frame_rate)

    # Save the updated EAF file
    output_path = os.path.join(new_folder_path, f"{video_file_name}.eaf")
    eaf.to_file(output_path)
    print(f'Saved updated EAF file to: {output_path}')

    # Add the video file as a linked file to the EAF
    eaf.add_linked_file(video_file_path, relpath=None, mimetype="video/mxf", time_origin=0)
    print(f'Linked video file {video_file_path} to EAF file.')

# Main function
def main(video_ext):
    base_dir = "/Users/ivar/Desktop/studieAI/AI_TADA3/coding/data"
    video_date_folder = f"0_videos/21_08_2023/{video_ext}"
    transnet_folder = "1_TransNet_files"
    annotation_files_folder = "2_annotation_files2/SBD"

    # Iterate over each file in the video date folder
    for file in os.listdir(os.path.join(base_dir, video_date_folder)):
        if file.endswith(f".{video_ext}"):
            video_file_name = file[:-4]  # Remove the file extension
            process_video(base_dir, video_file_name, video_date_folder, transnet_folder, 
                          annotation_files_folder)

# Entry point for the script
if __name__ == "__main__":
    main('mxf')



