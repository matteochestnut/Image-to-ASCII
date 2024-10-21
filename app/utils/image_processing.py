# utils/image_processing.py

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

font_size = 8
ascii_chars = [' ', '.', ':', 'c', 'o', 'P', 'O', '?', '@', '■', '|', '-', '/', '\\']

def convert_to_ASCII(image_bytes):
    """Convert the uploaded image to ASCII image and return as a PNG image."""
    # Convert bytes to numpy array and read it using OpenCV
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.COLOR_BGR2RGB)

    height, width = get_image_dims(img)
    ascii_str, color_array = make_ascii_str(img, font_size, ascii_chars)
    ascii_img = render(ascii_str, font_size, height, width, color_array, True)

    # Convert to grayscale
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert the image to PNG format
    #pil_img = Image.fromarray(ascii_img)

    return ascii_img

def get_resize_image(image, scale = 8):
    height, width = image.shape[:2]
    new_size = (int(width / scale), int(height / scale))
    return cv2.resize(image, new_size)

def get_image_dims(image):
    return image.shape[:2]

def get_quantized_luminance(image):
    """
    Quantized luminance values:
    0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
    """
    luminance = ( 0.2126 * image[:, :, 0] + 0.7152 * image[:, :, 1] + 0.0722 * image[:, :, 2] ) / 255
    return np.floor(luminance * 10) / 10

def gaussian_blur(image):
    low_sigma = cv2.GaussianBlur(image,(3,3),0)
    high_sigma = cv2.GaussianBlur(image,(5,5),0)
    return low_sigma - high_sigma

def sobel_filter(image):
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    atan2 = (np.arctan2(grad_y, grad_x) / np.pi) * 0.5 + 0.5
    grad = np.sqrt(grad_x**2 + grad_y**2)
    return grad / np.max(grad), atan2

def get_resized_threshold_gradient(grad, scale):
    scaled_grad = grad * 255
    _, threshold_grad = cv2.threshold(scaled_grad, 20, 255, cv2.THRESH_BINARY)
    return (get_resize_image(threshold_grad, scale) / 255).astype(np.int32)

def get_resized_quantized_atan2(atan2, scale):
    resized_atan2 = get_resize_image(atan2, scale)
    oldMin = 0
    oldMax = 1
    newMin = 10
    newMax = 13
    quantized_atan2 =  (((resized_atan2 - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
    return (np.floor(quantized_atan2 * 10) / 10).astype(np.int32)

def make_ascii_str(image, scale, ascii_chars):
    color_array = []
    resized_image = get_resize_image(image, scale)
    quantized_luminance = get_quantized_luminance(resized_image)
    
    gaussian_image = gaussian_blur( get_quantized_luminance( image ) )
    grad, atan2 = sobel_filter(gaussian_image)
    threshold_grad = get_resized_threshold_gradient(grad, scale)
    #plt.imshow(threshold_grad, cmap = "gray")
    #plt.show()
    quantized_atan2 = get_resized_quantized_atan2(atan2, scale)
    directions = np.multiply(threshold_grad, quantized_atan2)
    
    # fare un mappa in cui le direzioni sono quantizzate a 10, 11, 12, 13
    # creare array direzioni con valori 0, 10, 11, 12, 13 usande il grad
    # prendere il massimo tra array luminanza e array direzioni
    # convertire in ascii nel ciclo for
    
    ascii_str = ''
    for y in range(quantized_luminance.shape[0]):
        for x in range(quantized_luminance.shape[1]):
            luminance = quantized_luminance[y, x]
            char_index = np.maximum( int(luminance.item() * 10), directions[y, x])
            ascii_str += ascii_chars[char_index]
            color_array.append( (resized_image[y][x][2], resized_image[y][x][1], resized_image[y][x][0], 255) )
        ascii_str += '\n'
        color_array.append( (0, 0, 0, 0) )
    return ascii_str, color_array
    

def render(ascii_str, font_size, render_height, render_width, color_array, color):
    if not color:
        color_array = [(255, 255, 255, 255)] * len(ascii_str)
    font = ImageFont.truetype('Arial.ttf', font_size)
    canvas = Image.new('RGB', (render_width, render_height), 'black')
    draw = ImageDraw.Draw(canvas)
    color_index = 0
    y_text = 0
    for line in ascii_str.splitlines():
        x_text = 0
        for char in line:
            if char != ' ':
                #draw.text((x_text, y_text), char, fill=color_array[color_index], font=font)
                draw.text((x_text, y_text), char, fill=(255, 255, 255, 255), font=font)
            x_text += font_size
            color_index += 1
        y_text += font_size
        color_index += 1
    
    return canvas
    
    #canvas.show()
    #canvas.save(save_name)
