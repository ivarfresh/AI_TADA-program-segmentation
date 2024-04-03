"""
Based on the annotation file, calculates a segmentation vector.

- input: 
    - annotation file
    
-output:
    - list of tuples, where each tuple corresponds to one annotation
    - tuple format: (start_frame, end_frame, label)
    
- label description:
    - 1 if program
    - 0 else
    
- example:
    - tuple (0, 15702, 1) gives the first program in the movie.
"""

import xml.etree.ElementTree as ET

def read_eaf(file_path, frame_rate=25):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Create a dictionary for time slot references
    time_slots = {}
    for time_slot in root.findall(".//TIME_ORDER/TIME_SLOT"):
        time_slot_id = time_slot.attrib.get("TIME_SLOT_ID")
        time_value = time_slot.attrib.get("TIME_VALUE")
        time_slots[time_slot_id] = time_value

    # Initialize the segmentation vector
    segmentation_vector = []

    # Process each tier
    for tier in root.findall(".//TIER"):
        tier_id = tier.attrib.get("TIER_ID")
        print(f"Tier: {tier_id}")

        for annotation in tier.findall(".//ALIGNABLE_ANNOTATION"):
            annotation_id = annotation.attrib.get("ANNOTATION_ID")
            start_time_ref = annotation.attrib.get("TIME_SLOT_REF1")
            end_time_ref = annotation.attrib.get("TIME_SLOT_REF2")

            # Convert time to frame numbers
            start_frame = int((int(time_slots[start_time_ref]) / 1000) * frame_rate)
            end_frame = int((int(time_slots[end_time_ref]) / 1000) * frame_rate)

            annotation_value = annotation.find(".//ANNOTATION_VALUE").text

            # Check if the annotation value is a program
            segment_value = 1 if annotation_value.startswith("program ") else 0

            # Add to segmentation vector
            segmentation_vector.append((start_frame, end_frame, segment_value))

            print(f"  Annotation ID: {annotation_id}")
            print(f"  Start Frame: {start_frame}")
            print(f"  End Frame: {end_frame}")
            print(f"  Annotation Value: {annotation_value}")
            print("")
    
    # Sort the segmentation vector based on start frame
    segmentation_vector.sort(key=lambda x: x[0])
    
    print(f'\nSegmentation_vector:\n\n{segmentation_vector}')
    return segmentation_vector


if __name__ == "__main__":
    file_path = "../data/2_annotation_files/caspian/DS782_722374D-DGS00Z03UDY/DS782_722374D-DGS00Z03UDY.eaf"
    read_eaf(file_path)
