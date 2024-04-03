# AI_TADA-program-segmentation
## Introduction
This repository entails the work for the program segmentation part of the project "AI-TADA: Automated indexing of historical television data". A collaboration of Utrecht University and Beeld and Geluid institute (https://www.uu.nl/en/research/ai-labs/ai-media-lab/projects/ai-tada-automated-indexing-of-historical-television-data).

This repo is about the program segmentation. Specifically, it is aimed at segmenting programs from an input video stream.

The general flow of the project is:
1. Generate shot boundary detections (SBDs) from a video stream.
2. Segment the input video into shot videos, based on the SBD files.
3. Extract keyframes for each shot video.  (optional)
4. Calculate features of each (key)frame.
5. Use LDA/fisher score to maximize between-class variance as to distinguish program boundaries.

The project also includes scripts for data annotation: converting shot boundaries to annotations and vice versa.

## Installation
1. Create anaconda environment with Python 3.11.5:
```
conda create --name AI_TADA python=3.11.5
```
2. Activate environment:
```
conda activate AI_TADA
```
3. Clone AI-TADA directory:
```
git clone https://github.com/ivarfresh/AI_TADA-program-segmentation.git
```
4. Go to directory:
```
cd {root_directory}/AI_TADA-program-segmentation
```
5. Install requirements.txt  (does not include packages required for TransNetV2):
```
pip install -r requirements.txt
```
6. Install the TransNetV2 model for SBD. Follow these steps: 
```
https://github.com/soCzech/TransNetV2/tree/master/inference
```
After installation, your root folder should look like this:
[root tree](https://github.com/ivarfresh/AI_TADA-program-segmentation/blob/main/tree%20images/root%20tree.png)

7. You will not have the video data yet. Ask your supervisors about this. Make sure your data folder has the following tree strucutre:
[data tree](https://github.com/ivarfresh/AI_TADA-program-segmentation/blob/main/tree%20images/data%20folder%20tree.png)

## Usage
### General project
1. If you work on Mac or linux, run "xmf_to_mp4.py". This converts all videos to ".mp4". If you work Windows, you can use ".xmf". 

2. Run "TransNet_all_videos.py" in order to run the TransNetV2 model on all videos in a folder. See [TransnetV2 run instructions](https://github.com/ivarfresh/AI_TADA-program-segmentation/blob/main/run%20instructions/Transnet%20run%20intstructions.txt), to run the model via terminal. 

5. Run "LDA_pipeline/MoviePy_segmentation.py" (segment the video into shot videos)

6. Run "LDA_pipeline/keyframe_FFMPEG.py" (generate keyframes)

7. Run "LDA_pipeline/color_hists.py" (calculate color histograms)

8. Run "LDA_pipeline/fisher_score.py" (calculate fisher score with sliding window) or "LDA_pipeline/LDA_hist.py" (calculate sklearn LDA with sliding window).

###Shots to annotations
1. If you want to turn shots into annotations, run "shots_to_annotations.py"
2. If you want to turn programs annotations into program segmentation vector, run "read_elan_file.py"
3. If you want to turn programs annotations into shot segmentation vector, run "read_elan_file_shots.py"
