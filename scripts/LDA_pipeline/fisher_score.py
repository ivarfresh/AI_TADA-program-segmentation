"""
Calculates the fisher score for windows of frames by using a sliding window approach. 
For more info on the fisher score formula and the sliding window, see:

- fisher score intro: https://www.freecodecamp.org/news/an-illustrative-introduction-to-fishers-linear-discriminant-9484efee15ac/
- sliding window: https://www.geeksforgeeks.org/window-sliding-technique/


Input:
    - the color histograms of images (list)
    
Output:
   - plot of the Fisher score's and important frame numbers.
   - print values. 
"""

import re
import math
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
import color_hists
from scipy.signal import find_peaks

def calculate_program_boundary(group1_keys, group2_keys):
    """
    Calculates the potential program boundary frame number by averaging the last frame of a
    group of images before the boundary and the first frame of a group after the boundary,
    then rounding up to the nearest integer.

    Parameters:
    - group1_keys (list): A list of image filenames in the group before the program boundary.
    - group2_keys (list): A list of image filenames in the group after the program boundary.

    Returns:
    - int: The calculated program boundary frame number.
    """
    
    # Extract the frame number from the last element of Group 1
    last_frame_group1 = int(re.search(r'split_\d+_(\d+)_iframe_\d+\.jpg', group1_keys[-1]).group(1))
    # Extract the frame number from the first element of Group 2
    first_frame_group2 = int(re.search(r'split_(\d+)_\d+_iframe_\d+\.jpg', group2_keys[0]).group(1))
    
    # Calculate the average and round it upwards to the nearest integer
    program_boundary = math.ceil((last_frame_group1 + first_frame_group2) / 2)
    
    return program_boundary

def compute_fisher(histograms, keys, window_size=40):
    """
    Computes Fisher scores for each window of histograms to determine significant changes
    in image content, potentially indicating a program boundary.

    Parameters:
    - histograms (list): A list of histogram arrays for sequential images.
    - keys (list): A list of image filenames corresponding to the histograms.
    - window_size (int): The number of histograms to include in each comparison window.

    Returns:
    - list: A list of tuples containing the start frame, Fisher score, and the keys for
            images in the before and after groups for each window.
    """
    
    fisher_score = []
    
    # Sliding window implementation
    for start_index in range(len(histograms) - 2 * window_size + 1):
        group1_histograms = histograms[start_index:start_index + window_size]
        group2_histograms = histograms[start_index + window_size:start_index + 2 * window_size]
        
        # Fisher score calculation
        # 1.Calculate means (m1 and m2)
        m1 = np.mean(group1_histograms, axis=0)
        m2 = np.mean(group2_histograms, axis=0)
        
        # 2.Calculate variances (s1^2 and s2^2)
        s1_squared = np.var(group1_histograms, axis=0, ddof=1)  # ddof=1 for sample variance
        s2_squared = np.var(group2_histograms, axis=0, ddof=1)  # ddof=1 for sample variance
        
        # 3.Compute the score using the formula from the image
        score_array = ((m2 - m1) ** 2) / (s1_squared + s2_squared)
        
        # Summarize the score array into a single value (for example, by taking the mean)
        score = np.mean(score_array)  # This is one way to summarize the score array
        
        print(f'score: {score}')
        
        match = re.match(r'split_(\d+)_(\d+)_iframe_\d+\.jpg', keys[start_index])
        start_frame = match.group(1) if match else 'Unknown'

        fisher_score.append((start_frame, score, keys[start_index:start_index + window_size], keys[start_index + window_size:start_index + 2 * window_size]))
        
    return fisher_score

    
def print_low_fisher_scores(fisher_score, threshold=0.05):
    """
    Prints the start frames and LDA scores for cases where the LDA score is at or below
    a specified threshold, indicating potential areas of low differentiation.

    Parameters:
    - fisher_score (list): A list of tuples containing information about LDA scores and the
                           corresponding frame groups.
    - threshold (float): The LDA score threshold below which to highlight scores.
    """
    
    print(f"Start frames with LDA score of {threshold} or lower:")
    for start_frame, score, _, _ in fisher_score:
        if score <= threshold:
            print(f"Start frame: {start_frame}, LDA score: {score}")
            
def print_fisher_score_peaks(fisher_score):
    """
    Identifies and prints the peaks in LDA scores along with the calculated program boundaries for these peaks.

    Parameters:
    - fisher_score (list): A list of tuples containing information about LDA scores and the
                           corresponding frame groups.
    """
    
    lda_scores = [score for _, score, _, _ in fisher_score]

    # Find peaks in the LDA scores
    peaks, _ = find_peaks(lda_scores)
    peak_scores = [lda_scores[i] for i in peaks]

    # Calculate program boundaries for the peaks
    program_boundaries = [calculate_program_boundary(fisher_score[i][2], fisher_score[i][3]) for i in peaks]

    print("Peaks in LDA scores:")
    for i, peak in enumerate(peaks):
        print(f"Peak at index {peak} (Program Boundary: {program_boundaries[i]}), LDA score: {peak_scores[i]}")


def plot_fisher_score_peaks(fisher_score):
    """
    Plots the Fisher (LDA) scores over a sequence of images and highlights the peaks, which
    may indicate significant content changes or transitions.
    
    Parameters:
    - fisher_score (list): A list of tuples containing information about LDA scores and the
                           corresponding frame groups.
    """
    
    lda_scores = [score for _, score, _, _ in fisher_score]
    indices = range(len(lda_scores))

    # Find peaks in the LDA scores
    peaks, _ = find_peaks(lda_scores, height=0.3)
    peak_scores = [lda_scores[i] for i in peaks]

    # Calculate program boundaries for the peaks
    program_boundaries = [calculate_program_boundary(fisher_score[i][2], fisher_score[i][3]) for i in peaks]

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot all the LDA scores
    ax.plot(indices, lda_scores, marker='o', linestyle='-', color='b', label='LDA Score')

    # Highlight the peaks
    ax.scatter(peaks, peak_scores, color='r', s=50, zorder=5, label='Peaks')

    # Setting the x-axis ticks to the program boundaries of the peaks
    ax.set_xticks(peaks)
    ax.set_xticklabels(program_boundaries, rotation=45, ha='right')

    # Adding labels and title
    ax.set_title('Fisher Scores with Peaks Highlighted')
    ax.set_xlabel('Frame numbers (of potential program boundaries)')
    ax.set_ylabel('Fisher Score')
    ax.legend()
    ax.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_threshold_fisher_scores(fisher_score, threshold, score_type='high'):
    """
    Plots LDA scores, highlighting scores above or below a certain threshold.
    
    Parameters:
    - fisher_score (list): A list of tuples containing information about LDA scores and the corresponding frame groups.
    - threshold (float): The threshold above or below which to highlight LDA scores.
    - score_type (str): Determines whether to highlight scores above ('high') or below ('low')
                        the threshold.
    """
    # Extract LDA scores
    lda_scores = [score for _, score, _, _ in fisher_score]

    # Determine indices of scores and their program boundaries based on the threshold and score type
    if score_type == 'high':
        indices_of_threshold_scores = [i for i, score in enumerate(lda_scores) if score > threshold]
        extreme_label = 'Above'
    elif score_type == 'low':
        indices_of_threshold_scores = [i for i, score in enumerate(lda_scores) if score <= threshold]
        extreme_label = 'Below'
    else:
        raise ValueError("score_type must be 'high' or 'low'")

    threshold_scores = [lda_scores[i] for i in indices_of_threshold_scores]
    program_boundaries = [calculate_program_boundary(fisher_score[i][2], fisher_score[i][3]) for i in indices_of_threshold_scores]

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot all the LDA scores
    ax.plot(range(len(lda_scores)), lda_scores, marker='o', linestyle='-', color='b', label='LDA Score')
    
    # Highlight the scores based on the threshold
    ax.scatter(indices_of_threshold_scores, threshold_scores, color='r', s=50, zorder=5, label=f'Scores {extreme_label} Threshold')

    # Setting the x-axis ticks to the program boundaries of the scores based on the threshold
    ax.set_xticks(indices_of_threshold_scores)
    ax.set_xticklabels(program_boundaries, rotation=45, ha='right')

    # Adding labels and title
    ax.set_title(f'LDA Scores {extreme_label} Threshold of {threshold}')
    ax.set_xlabel('Potential Program Boundary frame numbers.')
    ax.set_ylabel('LDA Score')
    ax.axhline(threshold, color='r', linestyle='--', label=f'Threshold ({threshold})')
    ax.legend()
    ax.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

#main
# Loading histograms and preparing data
histogram_dict = color_hists.histograms
keys_sorted = sorted(list(histogram_dict.keys()), key=lambda x: int(re.match(r'split_(\d+)_\d+_iframe_\d+\.jpg', x).group(1)))
histograms_sorted = [np.concatenate((histogram_dict[key][0], histogram_dict[key][1], histogram_dict[key][2])) for key in keys_sorted]


#Print score in range
# for start_frame, score, window_keys_group1, window_keys_group2 in fisher_score[300:320]:
#     print(80*'-')
#     print(f"Comparison starting at frame {start_frame}: LDA score = {score}")
#     print(f"\nGroup 1 contains: {', '.join(window_keys_group1)}")
#     print(f"\nGroup 2 contains: {', '.join(window_keys_group2)}")
    
#     # Calculate and print the program boundary
#     program_boundary = calculate_program_boundary(window_keys_group1, window_keys_group2)
#     print(f"\nProgram Boundary: {program_boundary}")
#     print(80*'-')


#Example usage and plotting
threshold = 0.4
fisher_score = compute_fisher(histograms_sorted, keys_sorted)
print_low_fisher_scores(fisher_score, threshold = threshold)
plot_threshold_fisher_scores(fisher_score, threshold = threshold, score_type='high') #adjust "score_type" if you want to plot the lowest points instead of the highest.
print_fisher_score_peaks(fisher_score)
# plot_fisher_score_peaks(fisher_score)




#FULL FRAMES of shot videos
# Currently, the code works calculates Fisher score between color histograms of 
# of I-frames/keyframes for each shot video. However, if you want it to calculate the Fisher score for
# color histograms of all frames of the shot videos, you could try using the code below. 
# You should then the color histograms saved in a .npy file. 

# def load_histograms_np(filepath):
#     histograms_array = np.load(filepath, allow_pickle=True)
#     return dict(histograms_array)
    
# histograms_filepath = "../../data/color_histograms.npy"
# loaded_histograms = load_histograms_np(histograms_filepath)
# print(type(loaded_histograms))



