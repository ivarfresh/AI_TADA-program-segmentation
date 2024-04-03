from moviepy.editor import VideoFileClip
import os

def split_video_by_frames(video_folder_path, video_name, scenes_txt, output_dir):
    """
    Splits a video into multiple segments based on start and end frames specified in a given file.

    Parameters:
    - video_folder_path: The path to the folder containing the video and frames file.
    - video_name: The name of the video file to be processed (including extension).
    - frames_file_name: The name of the text file containing the start and end frames for each segment.
    - output_dir: The directory where the output video segments will be saved.

    Each line in the frames file should contain a pair of numbers (start frame, end frame),
    separated by a space. This function will create a subdirectory in the output directory
    named after the video file (without its extension) where all the video segments will be saved.
    """
    video_path = os.path.join(video_folder_path, video_name)
    video = VideoFileClip(video_path)
    
    # Extract the video's base name (without extension) to use as the folder name
    video_name_without_ext = os.path.basename(video_path).split('.')[0]
    full_output_dir = os.path.join(output_dir, video_name_without_ext)
    
    print(f'video_path: {video_path}')
    print(f'scenes_txt: {scenes_txt}')
    print(f'video_name_without_ext: {video_name_without_ext}')
    print(f'full_output_dir: {full_output_dir}')
    
    # Ensure the output directory exists
    if not os.path.exists(full_output_dir):
        os.makedirs(full_output_dir)
    
    with open(scenes_txt, 'r') as file:
        for line in file:
            start_frame, end_frame = map(int, line.strip().split())
            output_path = os.path.join(full_output_dir, f"split_{start_frame}_{end_frame}.mp4")
            clip = video.subclip(start_frame / video.fps, end_frame / video.fps)
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def main():
    #adjust these paths based on which videos you want to process.
    video_folder_path = "../../data/0_videos/21_08_2023/mxf"
    video_name = "DS574_708549D-DGS00Z03UM8.mxf"
    scenes_txt = "../../data/1_TransNet_files/DS574_708549D-DGS00Z03UM8.mxf.scenes.txt"
    output_dir = "../../data/3_MoviePy_segmentation"
    
    split_video_by_frames(video_folder_path, video_name, scenes_txt, output_dir)

if __name__== '__main__':
    main()
