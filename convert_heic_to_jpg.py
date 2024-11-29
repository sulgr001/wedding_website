import os
from PIL import Image
import pillow_heif

# Folder containing .heic files
input_folder = r"C:\Users\sulgr\Downloads\Maddie & Sully-001\Maddie & Sully"  # Replace with your folder path
output_folder = r"C:\Users\sulgr\Downloads\Maddie & Sully-001\Maddie & Sully\output"  # Subfolder for .jpg images

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith('.heic'):  # Check for .heic files
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.jpg')
        
        try:
            # Open the HEIC image and save as JPEG
            heif_file = pillow_heif.open_heif(input_path)
            image = Image.frombytes(
                heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode
            )
            image.save(output_path, "JPEG")
            print(f"Converted: {file_name} -> {output_path}")
        except Exception as e:
            print(f"Failed to convert {file_name}: {e}")

print("Conversion complete!")
