import cv2
import matplotlib.pyplot as plt
import os
import cv2
import csv

import util

from util.frame_selection import *
from util.helpers import *

def run():
    file1 = "./vid/2024-03-16 15-47-55.mp4"
    name = "video_to_img2_refactor.py"

    frames = cv2.VideoCapture(file1)

    # set up arguments
    save = True
    show_img = False
    pause = False
    log = False

    # set up the parameters
    frame_rate = getFPS(frames)
    number_of_frames = getNumberOfFrames(frames)
    frame_rate_new = 3  # number of frames to select every second
    selected_frame_index = int(frame_rate / frame_rate_new)  # pick every nth frame

    print_stats(log, frame_rate, number_of_frames, selected_frame_index)

    folder = create_data_folder(save)

    # arrays to store the frames and difference values
    selected_frames = []  # list of selected frames by reduced framerate
    difference_array = []  # array to store difference values
    selected_difference_array = [] # array to store difference values of selected frames
    selected_frames_unique = []  # array to store unique frames
    # plotting value arrays
    selected_plot_array = []
    selected_frame_array = []
    line_array = []

    # comparison parameters
    image_compare_displacement = 5  # the distance between the compared images by index
    difference_threshold = 1.5  # pick frames where the difference is less than this
    unique_difference_threshold = 2.5  # to compare the last saved frame with the current selected frame

    save_params_csv(save, folder, name, frame_rate, number_of_frames, selected_frame_index, image_compare_displacement, difference_threshold, unique_difference_threshold)

    # Set the DPI and size in pixels
    dpi = 100
    width_pixels = 2000
    height_pixels = 500

    # Create an empty plot
    plt.subplots(figsize=subplot_params(dpi, width_pixels, height_pixels), dpi=dpi)

    # add labels to the plot
    plt.xlabel(f'Frame Index (x{selected_frame_index})')
    plt.ylabel('Difference')

    # add line for difference threshold
    plt.axhline(y=difference_threshold, color='SkyBlue', linestyle='-', label=f'Difference Threshold ({difference_threshold})')
    # add line for unique difference threshold
    plt.axhline(y=unique_difference_threshold, color='PeachPuff', linestyle='-', label=f'Unique Difference Threshold ({unique_difference_threshold})') 
    plt.legend()

    counter = 0  # frame index
    selected_counter = 0  # selected frame index

    # loop through the video
    while counter < number_of_frames:
        _, frame = frames.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5) # rescale the frame to half the size
        if show_img: cv2.imshow('frame', frame)

        if counter % selected_frame_index == 0:  # append every nth frame
            selected_frames.append(frame)
            selected_counter += 1
            if show_img: cv2.imshow(f"{selected_frame_index}. frame", selected_frames[-1])

        if (len(selected_frames) > image_compare_displacement):  # if we have enough frames to compare
            im1 = selected_frames[len(selected_frames) - image_compare_displacement]
            im2 = selected_frames[-1]

            diff = cv2.mean(cv2.absdiff(im1, im2))[0]
            difference_array.append(diff)

            line_array.append({"x": selected_counter, "y": diff})

            if diff < difference_threshold: 
                if show_img: cv2.imshow("selected frame", selected_frames[-1])
                selected_difference_array.append({"x": len(difference_array), "y": diff})
                selected_plot_array.append({"x": selected_counter, "y": diff})

                if len(selected_frames_unique) == 0: # if the unique array is empty, add the first frame
                    selected_frames_unique.append(selected_frames[-1])
                else:
                    difference_unique = cv2.mean(cv2.absdiff(selected_frames_unique[-1], selected_frames[-1]))[0] # compare the last saved frame with the current selected frame
                    if log: print("difference unique", format(difference_unique, ".2f"))

                    if difference_unique > unique_difference_threshold:
                        selected_frames_unique.append(selected_frames[-1])
                        if log: print("added unique frame", counter)
                        
                        # add the unique frame position and name to the array
                        selected_frame_array.append({"x": selected_counter, "name": f'frame{counter}.jpg'})

                        if show_img: cv2.imshow("selected frame unique", selected_frames[-1]) 
                        save_frame(save, folder, selected_frames[-1], counter)

        counter += 1 # next frame

    # plot the values of line_array as a line plot
    plt.plot([x["x"] for x in line_array], [x["y"] for x in line_array], 'b-')

    # plot the values of selected_plot_array as a scatter plot
    plt.scatter([x["x"] for x in selected_plot_array], [x["y"] for x in selected_plot_array], color='blue')

    # plot the values of frame_array as labeled vertical lines
    for frame in selected_frame_array:
        plt.axvline(x=frame["x"], color='green', linestyle='-', label=frame["name"])
        plt.text(frame["x"], 8.5, frame["name"], rotation=90, ha='center', va='bottom', color='white', fontsize=8, bbox=dict(facecolor='green', edgecolor='white', boxstyle='square,pad=0.3'))

    # save the plot to a file
    if save: plt.savefig(f'{folder}/plot.png')

    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

run()