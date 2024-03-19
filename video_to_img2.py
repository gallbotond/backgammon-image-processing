import cv2
import matplotlib.pyplot as plt
import datetime
import os
import cv2
import csv

import util

def run():
    file1 = "./vid/2024-03-16 15-47-55.mp4"
    name = "video_to_img2.py"

    frames = cv2.VideoCapture(file1)
    # save = False
    save = True
    show_img = False
    pause = False
    log = False

    frame_rate = util.getFPS(frames)
    number_of_frames = util.getNumberOfFrames(frames)
    frame_rate_new = 3  # number of frames to select every second
    selected_frame_index = int(frame_rate / frame_rate_new)  # pick every nth frame

    if log: print(
        "frame rate",
        frame_rate,
        "\nnumber of frames",
        number_of_frames,
        "\nselected frame index",
        selected_frame_index,
    )

    if save:
        # save files to a folder with the current time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        if not os.path.exists(current_time):
            os.makedirs(f'./data/{current_time}')

    selected_frames = []  # list of selected frames by reduced framerate
    difference_array = []  # array to store difference values
    selected_values = [] # array to store difference values 
    selected_frames_unique = []  # array to store unique frames

    # image_compare_displacement = 15  # the distance between the compared images by index
    image_compare_displacement = 5  # the distance between the compared images by index
    difference_threshold = 2.0  # pick frames where the difference is less than this
    unique_difference_threshold = 2.5  # to compare the last saved frame with the current selected frame
    selection_delay = 3  # delay for the selected frames to not pick the first selected frame

    if save:
        # save the parameters to a csv file
        with open(f'./data/{current_time}/parameters.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name','Frame Rate', 'Number of Frames', 'Selected Frame Index', 'Image Compare Displacement', 'Difference Threshold', 'Unique Difference Threshold'])
            writer.writerow([name, frame_rate, number_of_frames, selected_frame_index, image_compare_displacement, difference_threshold, unique_difference_threshold])

    # Set the DPI and size in pixels
    dpi = 100
    width_pixels = 2000
    height_pixels = 500

    # Calculate the size in inches
    width_inches = width_pixels / dpi
    height_inches = height_pixels / dpi

    # Create a new figure with the specified size and DPI
    # plt.figure()

    # Create an empty plot
    fig, ax = plt.subplots(figsize=(30, 5))
    plot_diff = []
    plot_unique_diff = []
    x = []
    line, = ax.plot(x, plot_diff)
    line_unique, = ax.plot(x, plot_unique_diff)
    # add labels to the plot
    plt.xlabel(f'Frame Index (x{selected_frame_index})')
    plt.ylabel('Difference')
    # set the plot window size
    # plt.axis([0, number_of_frames / selected_frame_index, 20, 0])
    # set the plot window position on screen
    plt.get_current_fig_manager().window.setGeometry(100, 600, 1800, 400)  # Set the window position to (100, 200) and size to 500x2000 pixels

    # add horizontal lines to the plot
    plt.axhline(y=difference_threshold, color='SkyBlue', linestyle='-', label=f'Difference Threshold ({difference_threshold})')
    # show label for the horizontal line
    plt.legend()

    # add line for unique difference threshold
    plt.axhline(y=unique_difference_threshold, color='PeachPuff', linestyle='-', label=f'Unique Difference Threshold ({unique_difference_threshold})')  
    # show label for the horizontal line
    plt.legend()

    # plotting arrays
    selected_plot_array = []
    selected_frame_array = []
    line_array = []

    counter = 0  # frame index
    selected_counter = 0  # selected frame index
    delay_counter = 0  # delay for the selected frames to not pick the first selected frame
    unique_found = False  # flag to check if the unique frame is found
    while counter < number_of_frames:
        _, frame = frames.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        if show_img: cv2.imshow('frame', frame)

        if counter % selected_frame_index == 0:  # append every nth frame
            selected_frames.append(frame)
            # print("added frame", counter)
            selected_counter += 1
            if show_img: cv2.imshow(f"{selected_frame_index}. frame", selected_frames[-1])

        if (len(selected_frames) > image_compare_displacement):  # if we have enough frames to compare
            im1 = selected_frames[len(selected_frames) - image_compare_displacement]
            im2 = selected_frames[-1]

            diff = cv2.mean(cv2.absdiff(im1, im2))[0]
            # print("difference", format(diff, ".2f")) # format the difference to 2 decimal places
            difference_array.append(diff)

            # print(selected_counter, diff)

            # Ensure that x and plot_diff have the same length before appending
            # if len(x) == len(plot_diff):
            #     x.append(selected_counter)
            #     plot_diff.append(diff)
            #     plot_unique_diff.append(plot_unique_diff[-1] if len(plot_unique_diff) > 0 else 0)
            # else:
            #     print("Error: x and plot_diff do not have the same length.")

            # only plot the last 100 values
            # line.set_xdata(x[-100:])
            # line.set_ydata(plot_diff[-100:])  # Update the y-data of the line artist
            # ax.relim()
            # ax.autoscale_view()

            # plt.draw()
            # plt.pause(.001)
            line_array.append({"x": selected_counter, "y": diff})

            if diff < difference_threshold:
                if show_img: cv2.imshow("selected frame", selected_frames[-1])
                selected_values.append({"x": len(difference_array), "y": diff})
                print("added frame", counter)
                cv2.waitKey(0)

                # draw a small light blue dot on the plot, but only the last 100 values
                # plt.plot(selected_counter, diff, 'bo')
                selected_plot_array.append({"x": selected_counter, "y": diff})

                if len(selected_frames_unique) == 0:
                    selected_frames_unique.append(selected_frames[-1])
                else:
                    difference_unique = cv2.mean(cv2.absdiff(selected_frames_unique[-1], selected_frames[-1]))[0]
                    if log: print("difference unique", format(difference_unique, ".2f"))

                    # plot the unique difference and show it
                    # plt.plot(selected_counter, difference_unique, 'ro')
                    # print(selected_counter, difference_unique, len(plot_unique_diff), len(x))
                    # if len(x) == len(plot_unique_diff):
                    
                    # plot_unique_diff[-1] = difference_unique
                    # line_unique.set_xdata(x)
                    # line_unique.set_ydata(plot_unique_diff)
                    # ax.relim()
                    # ax.autoscale_view()
                    # plt.draw()
                    # plt.pause(.001)

                    if log: print(difference_unique)

                    if difference_unique > unique_difference_threshold:
                        selected_frames_unique.append(selected_frames[-1])
                        if log: print("added unique frame", counter)
                        
                        # draw a vertical line on the plot with a height of 8.5
                        # plt.axvline(x=selected_counter, color='green', linestyle='-', label=f'frame{len(selected_frames_unique)}.jpg')
                        # show a text on the vertical line rotated 90 degrees with some offset from the top
                        # plt.text(selected_counter, 8.5, f'frame{len(selected_frames_unique)}.jpg', rotation=90, ha='center', va='bottom', color='white', fontsize=8, bbox=dict(facecolor='green', edgecolor='white', boxstyle='square,pad=0.3'))
                        selected_frame_array.append({"x": selected_counter, "name": f'frame{len(selected_frames_unique)}.jpg'})

                        if show_img: cv2.imshow("selected frame unique", selected_frames[-1]) # show the unique frame
                        if save:
                            # save the unique frame to a file
                            cv2.imwrite(f"./data/{current_time}/frame{len(selected_frames_unique)}.jpg", frame)
                            # cv2.waitKey(0)

        counter += 1

        # listen for keypresses in the plot window
        if pause: plt.pause(.001)
        # if plt.waitforbuttonpress(0.01):
        #     # if p is pressed, pause the video
        #     if cv2.waitKey(0) & 0xFF == ord('p'):
        #         cv2.waitKey(0)

    

    # plot the values of line_array as a line plot
    plt.plot([x["x"] for x in line_array], [x["y"] for x in line_array], 'b-')

    # plot the values of selected_plot_array as a scatter plot
    plt.scatter([x["x"] for x in selected_plot_array], [x["y"] for x in selected_plot_array], color='blue')

    # plot the values of frame_array as labeled vertical lines
    for frame in selected_frame_array:
        plt.axvline(x=frame["x"], color='green', linestyle='-', label=frame["name"])
        plt.text(frame["x"], 8.5, frame["name"], rotation=90, ha='center', va='bottom', color='white', fontsize=8, bbox=dict(facecolor='green', edgecolor='white', boxstyle='square,pad=0.3'))

    # wait for keypress to close the plot window
    # save the plot to a file
    if save: plt.savefig(f'./data/{current_time}/plot.png')

    plt.show()
    cv2.waitKey(0)
    # if save:
    #     # save the plot to a file
    #     plt.savefig(f'./data/{current_time}/plot.png')

    cv2.destroyAllWindows()
run()