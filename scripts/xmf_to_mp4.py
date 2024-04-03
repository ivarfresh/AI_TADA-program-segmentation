import os
from moviepy.editor import VideoFileClip

def convert_mxf_to_mp4(mxf_file_path, output_folder):
    """
    Converts an MXF file to MP4 format and saves it to the specified output folder.
    Also outputs the sound of the input video.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the MXF file
    video_clip = VideoFileClip(mxf_file_path, audio=True)

    # Define the output file path
    base_name = os.path.basename(mxf_file_path)
    mp4_file_name = os.path.splitext(base_name)[0] + ".mp4"
    mp4_file_path = os.path.join(output_folder, mp4_file_name)

    # Write the video file in MP4 format
    video_clip.write_videofile(mp4_file_path, codec="libx264", audio_codec="aac")

def main():
    # Folder containing MXF files
    mxf_folder = "../data/21_08_2023"
    # Output folder for MP4 files
    output_folder = "../data/conversions"

    # Get a list of all files already converted to MP4 in the output folder
    already_converted = {file for file in os.listdir(output_folder) if file.endswith(".mp4")}

    # Process each MXF file in the folder
    for file in os.listdir(mxf_folder):
        if file.endswith(".mxf"):
            # Check if this MXF file's corresponding MP4 file already exists in the output folder
            mp4_file_name = os.path.splitext(file)[0] + ".mp4"
            if mp4_file_name in already_converted:
                print(f"Skipping {file} as it's already converted to MP4.")
                continue  # Skip the conversion for this file
            
            # If the MP4 file does not exist in the output folder, proceed with the conversion
            mxf_file_path = os.path.join(mxf_folder, file)
            convert_mxf_to_mp4(mxf_file_path, output_folder)
            print(f"Converted {file} to MP4.")

if __name__ == "__main__":
    main()
