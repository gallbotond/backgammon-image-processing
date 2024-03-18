import os
import datetime
import csv
import cv2

# print stats if log is True
def print_stats(log, frame_rate, number_of_frames, selected_frame_index):
    if log: print(
        "frame rate",
        frame_rate,
        "\nnumber of frames",
        number_of_frames,
        "\nselected frame index",
        selected_frame_index,
    )
        
# create a data folder with the current time
def create_data_folder(save):
    if save:
        # save files to a folder with the current time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        folder = f'./data/{current_time}'
        if not os.path.exists(current_time):
            os.makedirs(folder)
        return folder
        
# save the parameters to a csv file
def save_params_csv(save, folder, name, frame_rate, number_of_frames, selected_frame_index, image_compare_displacement, difference_threshold, unique_difference_threshold):
    if save:
        # save the parameters to a csv file
        with open(f'{folder}/parameters.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name','Frame Rate', 'Number of Frames', 'Selected Frame Index', 'Image Compare Displacement', 'Difference Threshold', 'Unique Difference Threshold'])
            writer.writerow([name, frame_rate, number_of_frames, selected_frame_index, image_compare_displacement, difference_threshold, unique_difference_threshold])

def subplot_params(dpi, width_pixels, height_pixels):
    # Set the DPI and size in pixels
    dpi = 100
    width_pixels = 2000
    height_pixels = 500

    # Calculate the size in inches
    width_inches = width_pixels / dpi
    height_inches = height_pixels / dpi
    return width_inches, height_inches

def save_frame(save, folder, frame, counter):
    if save:
        # save the frame
        cv2.imwrite(f'{folder}/frame_{counter}.jpg', frame)