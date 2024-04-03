import re
import math
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
import color_hists

histogram_dict = color_hists.histograms
keys_sorted = sorted(list(histogram_dict.keys()), key=lambda x: int(re.match(r'split_(\d+)_\d+_iframe_\d+\.jpg', x).group(1)))
histograms_sorted = [np.concatenate((histogram_dict[key][0], histogram_dict[key][1], histogram_dict[key][2])) for key in keys_sorted]

def calculate_program_boundary(group1_keys, group2_keys):
    """
    Description
    ----------
    Calculates potentional program boundary frame number, by:
        1. taking the end frame of the last shot in the "before" group.
        2. taking the start frame of the first shot in the "after" group. 
    
    Parameters
    ----------
    group1_keys : list
        - the names of images belonging to the "before group" (group before program boundary)
    group2_keys : list
        - the names of images belonging to the "after group" (group after program boundary)

    Returns
    -------
    program_boundary : integer
        - potential program boundary frame number

    """
    # Extract the frame number from the last element of Group 1
    last_frame_group1 = int(re.search(r'split_\d+_(\d+)_iframe_\d+\.jpg', group1_keys[-1]).group(1))
    # Extract the frame number from the first element of Group 2
    first_frame_group2 = int(re.search(r'split_(\d+)_\d+_iframe_\d+\.jpg', group2_keys[0]).group(1))
    
    # Calculate the average and round it upwards to the nearest integer
    program_boundary = math.ceil((last_frame_group1 + first_frame_group2) / 2)
    
    return program_boundary

def compute_sliding_lda_scores_with_windows(histograms, keys, window_size=1000):
    lda_scores_with_windows = []
    for start_index in range(len(histograms) - 2 * window_size + 1):
        group1_histograms = histograms[start_index:start_index + window_size]
        group2_histograms = histograms[start_index + window_size:start_index + 2 * window_size]
        
        group1_labels = [0] * window_size
        group2_labels = [1] * window_size
        
        X = np.array(group1_histograms + group2_histograms)
        y = np.array(group1_labels + group2_labels)
        
        lda = LinearDiscriminantAnalysis()
        lda.fit(X, y)
        score = lda.score(X, y)
        
        match = re.match(r'split_(\d+)_(\d+)_iframe_\d+\.jpg', keys[start_index])
        start_frame = match.group(1) if match else 'Unknown'

        lda_scores_with_windows.append((start_frame, score, keys[start_index:start_index + window_size], keys[start_index + window_size:start_index + 2 * window_size]))
        
    return lda_scores_with_windows


def plot_low_lda_scores(lda_scores_with_windows, threshold):
    # Extract LDA scores
    lda_scores = [score for _, score, _, _ in lda_scores_with_windows]
    
    # Find the indices and program boundaries of scores below the threshold
    indices_below_threshold = [i for i, score in enumerate(lda_scores) if score <= threshold]
    boundaries_below_threshold = [calculate_program_boundary(lda_scores_with_windows[i][2], lda_scores_with_windows[i][3]) for i in indices_below_threshold]
    scores_below_threshold = [lda_scores[i] for i in indices_below_threshold]

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot all the LDA scores
    ax.plot(range(len(lda_scores)), lda_scores, marker='o', linestyle='-', color='b', label='LDA Score')

    # Highlight the points below the threshold
    ax.scatter(indices_below_threshold, scores_below_threshold, color='r', s=50, zorder=5, label=f'Scores ≤ {threshold}')
    
    # Setting the x-axis ticks to the program boundaries of scores below threshold
    ax.set_xticks(indices_below_threshold)
    ax.set_xticklabels(boundaries_below_threshold, rotation=45, ha='right', fontsize=8)

    # Adding labels and title
    ax.set_title(f'LDA Scores Below {threshold}')
    ax.set_xlabel('Potential Program Boundary frame numbers')
    ax.set_ylabel('LDA Score')
    ax.axhline(threshold, color='r', linestyle='--', label='Threshold LDA Score')
    ax.legend()
    ax.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_high_lda_scores(lda_scores_with_windows, threshold):
    """
    Plots the LDA scores that are above the specified threshold, highlighting these points on the graph.

    Parameters:
    - lda_scores_with_windows: A list of tuples containing information about LDA scores and the corresponding frame groups.
    - threshold: The threshold above which LDA scores will be plotted.
    """
    # Extract LDA scores
    lda_scores = [score for _, score, _, _ in lda_scores_with_windows]

    # Find the indices and program boundaries of scores above the threshold
    indices_above_threshold = [i for i, score in enumerate(lda_scores) if score > threshold]
    scores_above_threshold = [lda_scores[i] for i in indices_above_threshold]
    program_boundaries = [calculate_program_boundary(lda_scores_with_windows[i][2], lda_scores_with_windows[i][3]) for i in indices_above_threshold]

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot all the LDA scores
    ax.plot(range(len(lda_scores)), lda_scores, marker='o', linestyle='-', color='b', label='LDA Score')
    
    # Highlight the points above the threshold
    ax.scatter(indices_above_threshold, scores_above_threshold, color='r', s=50, zorder=5, label=f'Scores > {threshold}')

    # Setting the x-axis ticks to the program boundaries of the scores above threshold
    ax.set_xticks(indices_above_threshold)
    ax.set_xticklabels(program_boundaries, rotation=45, ha='right')

    # Adding labels and title
    ax.set_title(f'LDA Scores Above {threshold}')
    ax.set_xlabel('Potential Program Boundary frame numbers.')
    ax.set_ylabel('LDA Score')
    ax.axhline(threshold, color='r', linestyle='--', label='Threshold LDA Score')
    ax.legend()
    ax.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

    
def print_low_lda_scores(lda_scores_with_windows, threshold):
    print(f"Program boundaries with LDA score of {threshold} or lower:")
    for window, score, start_frame, end_frame in lda_scores_with_windows:
        if score <= threshold:
            # Here we call the calculate_program_boundary function
            # and handle the case where a match might not be found
            try:
                program_boundary = calculate_program_boundary(start_frame, end_frame)
                print(f"Program boundary: {program_boundary}, LDA score: {score}")
            except AttributeError as e:
                print(f"Error processing frame range: {start_frame}-{end_frame}, with score: {score}")
                print(str(e))
                
def print_high_lda_scores(lda_scores_with_windows, threshold):
    """
    Prints program boundaries and LDA scores for all instances where the LDA score is above the threshold.

    Parameters:
    - lda_scores_with_windows: A list of tuples containing information about LDA scores and the corresponding frame groups.
    - threshold: The threshold above which to print the LDA scores and their program boundaries.
    """
    print(f"Program boundaries with LDA score above {threshold}:")
    for window, score, start_frame, end_frame in lda_scores_with_windows:
        if score > threshold:
            try:
                program_boundary = calculate_program_boundary(start_frame, end_frame)
                print(f"Program boundary: {program_boundary}, LDA score: {score}")
            except AttributeError as e:
                print(f"Error processing frame range: {start_frame}-{end_frame}, with score: {score}")
                print(str(e))

lda_scores_with_windows = compute_sliding_lda_scores_with_windows(histograms_sorted, keys_sorted, window_size=40)

for start_frame, score, window_keys_group1, window_keys_group2 in lda_scores_with_windows[300:320]:
    print(80*'-')
    print(f"Comparison starting at frame {start_frame}: LDA score = {score}")
    print(f"\nGroup 1 contains: {', '.join(window_keys_group1)}")
    print(f"\nGroup 2 contains: {', '.join(window_keys_group2)}")
    
    # Calculate and print the program boundary
    program_boundary = calculate_program_boundary(window_keys_group1, window_keys_group2)
    print(f"\nProgram Boundary: {program_boundary}")
    print(80*'-')

plot_low_lda_scores(lda_scores_with_windows, threshold =0.89)
print_low_lda_scores(lda_scores_with_windows,threshold =0.89)

plot_high_lda_scores(lda_scores_with_windows, threshold =0.98)
print_high_lda_scores(lda_scores_with_windows,threshold =0.98)

# plot_five_highest_lda_scores(lda_scores_with_windows)



