import cv2
import os
from datetime import datetime

# Function to crop a video
def crop_video(input_path, output_path):
    # Load the video file
    cap = cv2.VideoCapture(input_path)

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the crop dimensions (16:9 ratio)
    new_width = int((height / 16) * 9)
    new_height = height

    # Create a new video file for the output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    # Crop the video frame by frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop the frame to 16:9
        cropped_frame = frame[(height - new_height) // 2:(height + new_height) // 2,
                              (width - new_width) // 2:(width + new_width) // 2]

        # Write the cropped frame to the new video file
        out.write(cropped_frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Function to process all videos in a folder, sorted by date
def process_videos_in_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all video files in the folder
    files = [
        f for f in os.listdir(input_folder)
        if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))
    ]

    # Sort files by modification date (ascending)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(input_folder, x)))

    # Process each video in the sorted order
    for filename in files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        print(f"Processing {filename}...")
        # Crop the video
        crop_video(input_path, output_path)
        print(f"Finished {filename}.")

# Choose your input and output folders
input_folder = 'your/input/folder/path'  # Replace with the path to your folder with videos
output_folder = 'your/OUTPUT/folder/path'  # Replace with the folder where you want to save cropped videos

# Process all videos in the input folder
process_videos_in_folder(input_folder, output_folder)
