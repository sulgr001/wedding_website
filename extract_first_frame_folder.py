import cv2
import os

# Input folder containing .mp4 files
input_folder = r"C:\Users\sulgr\Downloads\Maddie & Sully-001\Maddie & Sully"  # Replace with your folder path
output_folder = r"C:\Users\sulgr\Downloads\Maddie & Sully-001\Maddie & Sully\output"    # Folder to save extracted frames

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith('.mp4'):  # Check for .mp4 files
        input_video_path = os.path.join(input_folder, file_name)
        output_image_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_frame1.jpg")
        
        # Open the video file
        video_capture = cv2.VideoCapture(input_video_path)

        # Check if the video was successfully opened
        if not video_capture.isOpened():
            print(f"Error: Unable to open video file: {file_name}")
            continue

        # Read the first frame
        success, frame = video_capture.read()
        if success:
            # Save the first frame as a JPEG image
            cv2.imwrite(output_image_path, frame)
            print(f"First frame saved for: {file_name} -> {output_image_path}")
        else:
            print(f"Error: Unable to read the first frame for: {file_name}")

        # Release the video capture object
        video_capture.release()

print("Processing complete!")
