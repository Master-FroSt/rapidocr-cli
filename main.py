#!/usr/bin/env python3
"""
RapidOCR CLI Tool (V6 Models Wrapper)
--------------------------
A lightweight command-line tool to extract text from images,
automatically copy it to your clipboard, and visualize the results.

Prerequisites:
    pip install rapidocr pyperclip
"""

import argparse
import sys
from pathlib import Path

try:
    from rapidocr import RapidOCR
except ImportError as e:
    RapidOCR = None  # Fixes IDE unbound warning
    print(f"[-] Detailed Import Error: {e}")
    print("[-] Error: 'rapidocr' wrapper is not installed.")
    print("[!] Please install it using: pip install rapidocr")
    sys.exit(1)

try:
    import pyperclip
except ImportError:
    pyperclip = None  # Fixes IDE unbound warning
    print("[-] Error: pyperclip is not installed.")
    print("[!] Please install it using: pip install pyperclip")
    sys.exit(1)


def extract_text(image_path: str, disable_copy: bool, visualize: bool) -> None:
    """
    Runs the RapidOCR wrapper (which auto-downloads V6 models) on the image.
    """
    path = Path(image_path)
    if not path.is_file():
        print(f"Error: Could not find the image file at '{image_path}'")
        sys.exit(1)

    print(f"[*] Initializing RapidOCR (V6 Wrapper)...")
    # Initialize the engine. It will use the downloaded v6 models automatically.
    engine = RapidOCR()

    print(f"[*] Processing '{path.name}'...")

    # Run inference
    raw_output = engine(str(path))

    # Handle different return signatures based on the wrapper version
    if isinstance(raw_output, tuple) and len(raw_output) == 2:
        result, _ = raw_output
    else:
        result = raw_output

    if not result:
        print("\n[-] No text was detected in the image.")
        return

    # Extract text robustly from RapidOCROutput dataclass or legacy lists
    extracted_lines = []

    # V6/3.x Wrapper returns a RapidOCROutput object with a 'txts' property
    if hasattr(result, 'txts') and result.txts:
        extracted_lines = list(result.txts)

    # Some experimental branches used 'texts'
    elif hasattr(result, 'texts') and result.texts:
        extracted_lines = list(result.texts)

    # Fallback if the underlying engine returns raw tuple/list data directly
    elif isinstance(result, (list, tuple)):
        for item in result:
            # Find the string element in the tuple (usually the text)
            text_part = next((x for x in item if isinstance(x, str)), None)
            if text_part is not None:
                extracted_lines.append(text_part)
            elif len(item) > 1:
                # Fallback if the tuple structure is slightly different
                extracted_lines.append(str(item[1]))

    full_text = "\n".join(extracted_lines)

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
        if hasattr(result, 'vis'):
            # The wrapper natively supports .vis() without needing OpenCV!
            result.vis(out_name)
            print(f"[+] Visualization image saved to: {out_name}")
        else:
            print("[-] Visualization (.vis) is not supported by your installed version of the wrapper.")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from an image using the RapidOCR Wrapper."
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
        help="Generate an output image with boxes drawn around detected text."
    )

    args = parser.parse_args()

    extract_text(args.image_path, args.no_copy, args.vis)


if __name__ == "__main__":
    main()