import argparse
import tkinter as tk
from PIL import ImageGrab
import pytesseract
from pyttsx3 import init
from skimage.metrics import structural_similarity as compare_ssim
import numpy as np
import cv2
import time
import sys

# Set up argument parser
parser = argparse.ArgumentParser(description="Capture a portion of the screen, apply OCR, and read it aloud if it changes.")
parser.add_argument("--coords", nargs=4, type=int, default=[413, 1459, 1604, 1632], help="Coordinates for the screen capture, in the format: top_x top_y bottom_x bottom_y")
parser.add_argument("--contrast", type=int, default=200, help="Contrast threshold (0-255) for image processing")
parser.add_argument("--original", type=str, default="original.png", help="Filename for saving the original screenshot")
parser.add_argument("--processed", type=str, default="processed.png", help="Filename for saving the processed screenshot")
parser.add_argument("--verbose", action="store_true", help="Print debug statements to the console")

# Parse arguments
args = parser.parse_args()

# Check if no arguments were given and print help if true
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Initialize text-to-speech engine
engine = init()

# Constants
coords = args.coords
screenshot_interval = 500  # in milliseconds
last_image = None
text_has_been_read = False

# Debugging function to print messages with a timestamp
def debug_print(message):
    if args.verbose:
        print(f"[DEBUG {time.strftime('%X')}]: {message}")

# Function to capture and process the screen
def process_screen():
    global last_image, text_has_been_read
    debug_print("Capturing the screen area.")

    # Capture the screen
    screenshot = ImageGrab.grab(bbox=(coords[0], coords[1], coords[2], coords[3]))
    debug_print("Screen captured.")

    # Convert the image to grayscale and increase contrast
    gray_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    _, processed_image = cv2.threshold(gray_image, args.contrast, 255, cv2.THRESH_BINARY)
    debug_print("Image processed to monochrome and contrast increased.")

    # If this is the first capture, initialize the last_image
    if last_image is None:
        last_image = processed_image
        debug_print("Initialized last_image.")

    # Compare the new screenshot with the last image
    score, _ = compare_ssim(last_image, processed_image, full=True)
    debug_print(f"Image comparison score: {score}")

    # If there is a change, perform OCR and read out the text
    if score < 1.0 and not text_has_been_read:
        debug_print("Change detected, performing OCR and reading text.")
        # Save the original and processed images
        cv2.imwrite(args.original, np.array(screenshot))
        cv2.imwrite(args.processed, processed_image)

        # Perform OCR
        text = pytesseract.image_to_string(processed_image)
        if text:
            # Read out the text using pyttsx3
            engine.say(text)
            engine.runAndWait()
            text_has_been_read = True  # Set the flag to True after reading the text
            debug_print(f"Text read aloud: {text}")
        else:
            debug_print("No text found by OCR.")
    elif score == 1.0:
        text_has_been_read = False  # Reset the flag when the region is unchanged

    # Update the last_image
    last_image = processed_image

    # Schedule the next screen capture
    root.after(screenshot_interval, process_screen)

# Create a transparent overlay window with a red border
root = tk.Tk()
root.attributes('-topmost', True)  # Always stay on top
root.overrideredirect(1)  # Remove border and title bar

# Calculate the window size and position
window_width = coords[2] - coords[0]
window_height = coords[3] - coords[1]
window_position = f"{window_width}x{window_height}+{coords[0]}+{coords[1]}"

# Set up the window
root.geometry(window_position)
root.attributes('-alpha', 0.3)  # Make the window transparent but visible

# Create a frame for the red border
frame = tk.Frame(root, borderwidth=1, relief='solid')
frame.pack(fill='both', expand='yes')
frame.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
debug_print("Transparent window with red border created.")

# Start the screen processing function
root.after(screenshot_interval, process_screen)

# Run the application
root.mainloop()
