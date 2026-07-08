#!/usr/bin/env python3
"""
RapidOCR ONNX CLI Tool
--------------------------
A lightweight command-line tool to extract text from images,
automatically copy it to your clipboard, and visualize the results.

Prerequisites:
    pip install rapidocr-onnxruntime pyperclip opencv-python numpy
"""

import argparse
import sys
from pathlib import Path

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError as e:
    RapidOCR = None  # Fixes IDE unbound warning
    print(f"[-] Detailed Import Error: {e}")
    print("[-] Error: rapidocr_onnxruntime is not installed or missing core dependencies.")
    print(
        "[!] Tip: If you already ran 'pip install', your IDE might be using a different Python interpreter/virtual environment than your terminal.")
    sys.exit(1)

try:
    import pyperclip
except ImportError:
    pyperclip = None  # Fixes IDE unbound warning
    print("[-] Error: pyperclip is not installed.")
    print("[!] Please install it using: pip install pyperclip")
    sys.exit(1)

try:
    import cv2
    import numpy as np

    HAS_CV2 = True
except ImportError:
    cv2 = None
    np = None
    HAS_CV2 = False


def visualize_result(image_path: str, result: list, output_path: str = "vis_result.jpg"):
    """
    Draws red bounding boxes around the detected text and saves the image.
    This replicates the `.vis()` behavior from the generic RapidOCR demo.
    """
    if not HAS_CV2:
        print("[-] Skipping visualization: 'opencv-python' is not installed.")
        return

    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"[-] Failed to load image for visualization: {image_path}")
        return

    # Draw a bounding box for each detected text region
    for item in result:
        # RapidOCR returns: [box, text, confidence]
        box = item[0]

        # Convert box coordinates to integer numpy array for OpenCV
        pts = np.array(box, np.int32)
        pts = pts.reshape((-1, 1, 2))

        # Draw the polygon (red box, 2px thickness)
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

    # Save the annotated image
    cv2.imwrite(output_path, img)
    print(f"[+] Visualization image saved to: {output_path}")


def extract_text(image_path: str, disable_copy: bool, visualize: bool) -> None:
    """
    Runs the ONNX OCR engine on the specified image and handles the output.
    """
    path = Path(image_path)
    if not path.is_file():
        print(f"Error: Could not find the image file at '{image_path}'")
        sys.exit(1)

    print(f"[*] Initializing RapidOCR (ONNX backend)...")
    # Initialize the engine
    engine = RapidOCR()

    print(f"[*] Processing '{path.name}'...")

    # Run inference.
    # result: list of [box_coordinates, text, confidence_score]
    # elapse: tuple of time taken for [det, cls, rec]
    result, elapse_list = engine(str(path))

    if result is None:
        print("\n[-] No text was detected in the image.")
        return

    # Format output text
    extracted_lines = [line[1] for line in result]
    full_text = "\n".join(extracted_lines)

    # Print results to terminal
    print("\n" + "=" * 40)
    print("📋 EXTRACTED TEXT:")
    print("=" * 40)
    print(full_text)
    print("=" * 40)

    # Calculate total time taken
    total_time = sum(elapse_list) if isinstance(elapse_list, list) else elapse_list
    print(f"[*] OCR completed in {total_time:.3f} seconds.")

    # Handle Clipboard
    if not disable_copy and pyperclip:
        try:
            pyperclip.copy(full_text)
            print("[+] Text automatically copied to your clipboard!")
        except Exception as e:
            print(f"[-] Failed to copy to clipboard: {e}")

    # Handle Visualization
    if visualize:
        out_name = f"vis_{path.name}"
        visualize_result(str(path), result, out_name)


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from an image using RapidOCR (ONNX)."
    )

    parser.add_argument(
        "image_path",
        type=str,
        help="Path to the screenshot or image file you want to read."
    )

    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Print the text to the terminal but DO NOT copy it to the clipboard."
    )

    parser.add_argument(
        "--vis",
        action="store_true",
        help="Generate an output image with red boxes drawn around detected text."
    )

    args = parser.parse_args()

    extract_text(args.image_path, args.no_copy, args.vis)


if __name__ == "__main__":
    main()