import os
import cv2

def convert_to_black_and_white(file_path, filename, output_folder):
    """
    Convert an image to black and white using OpenCV.
    
    Args:
        file_path (str): Path to the input image file.
        filename (str): Original filename of the image.
        output_folder (str): Path to the folder where the processed image will be saved.

    Returns:
        str: Filename of the processed image.
    """
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_filename = f'bw_{filename.rsplit(".", 1)[0]}.png'
    processed_path = os.path.join(output_folder, processed_filename)
    cv2.imwrite(processed_path, gray)
    return processed_filename
