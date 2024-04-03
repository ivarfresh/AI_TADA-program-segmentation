"""
This code takes in an annotation file and a shot.txt file and determines the label for each shot, 
based on the annotation file.

- input: 
    - annotation file
    - scenes.txt file
    
- output: 
    - list of tuples
    - tuples have format: (start_frame, end_frame, label)

- label description:
    - 1 if program
    - 0 else
"""

import os
import xml.etree.ElementTree as ET

# Function to read shot file and return a list of shots
def read_shot_file(file_path):
    with open(file_path, 'r') as file:
        shots = [tuple(map(int, line.strip().split())) for line in file]
    return shots

# Function to read EAF file and extract segmentation information
def read_eaf(file_path, frame_rate=25):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract time slot information
    time_slots = {time_slot.attrib.get("TIME_SLOT_ID"): time_slot.attrib.get("TIME_VALUE") for time_slot in root.findall(".//TIME_ORDER/TIME_SLOT")}
    
    segmentation_vector = []

    # Extract annotation information
    for tier in root.findall(".//TIER"):
        for annotation in tier.findall(".//ALIGNABLE_ANNOTATION"):
            start_time_ref = annotation.attrib.get("TIME_SLOT_REF1")
            end_time_ref = annotation.attrib.get("TIME_SLOT_REF2")
            start_frame = int((int(time_slots[start_time_ref]) / 1000) * frame_rate)
            end_frame = int((int(time_slots[end_time_ref]) / 1000) * frame_rate)
            annotation_value = annotation.find(".//ANNOTATION_VALUE").text
            segment_value = 1 if annotation_value.startswith("program ") else 0
            segmentation_vector.append((start_frame, end_frame, segment_value))

    segmentation_vector.sort(key=lambda x: x[0])
    return segmentation_vector

# Function to divide segmentation vector into shots using shot information
def divide_into_shots(segmentation_vector, shots):
    shot_vector = []
    for shot_start, shot_end in shots:
        shot_label = 0
        for segment_start, segment_end, label in segmentation_vector:
            if segment_start <= shot_end and segment_end >= shot_start:
                shot_label = label
                break
        shot_vector.append((shot_start, shot_end, shot_label))
    return shot_vector

# Function to get shot vector from EAF and shot file
def get_shot_vector(eaf_file_path, shot_file_path, frame_rate=25):
    segmentation_vector = read_eaf(eaf_file_path, frame_rate)
    shots = read_shot_file(shot_file_path)
    shot_vector = divide_into_shots(segmentation_vector, shots)
    return shot_vector

# Main function
def main():    
    # Print the current working directory: make sure directory is set to: AI_TADA/coding/scripts
    print("Current Working Directory:", os.getcwd())
    
    eaf_file_path = "../data/2_annotation_files/caspian/DS782_722374D-DGS00Z03UDY/DS782_722374D-DGS00Z03UDY.eaf"
    shot_file_path = "../data/1_TransNet_files/DS782_722374D-DGS00Z03UDY.mp4.scenes.txt"
    frame_rate = 25
    # Get the shot vector
    shot_vector = get_shot_vector(eaf_file_path, shot_file_path, frame_rate)
    print(shot_vector)
     # Print the first 20 shot information
    # for shot in shot_vector:
    #     print(shot)
        
    # print("Total number of shots:", len(shot_vector))

# Entry point for the script
if __name__ == "__main__":
    main()
    

