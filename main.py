#!/usr/bin/env python3
"""
RapidOCR Interactive CLI
--------------------------
A drag-and-drop enabled, in-memory OCR loop with Quick Actions.

Prerequisites:
    pip install rapidocr pyperclip
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from rapidocr import RapidOCR
except ImportError as e:
    RapidOCR = None
    print(f"[-] Import Error: {e}")
    print("[-] Please install the wrapper: pip install rapidocr")
    sys.exit(1)

try:
    import pyperclip
except ImportError:
    pyperclip = None
    print("[-] Warning: pyperclip is not installed. Clipboard copying is disabled.")


def clear_screen():
    """Clears the terminal screen for a clean UI."""
    os.system('cls' if os.name == 'nt' else 'clear')


def sanitize_path(raw_path: str) -> str:
    """Cleans up terminal drag-and-drop paths."""
    p = raw_path.strip()

    # PowerShell sometimes prefixes drag-and-drop with '& '
    if p.startswith("& "):
        p = p[2:]

    # Remove surrounding quotes (common in Windows drag-and-drop)
    if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
        p = p[1:-1]

    return p.strip()


def generate_filenames(original_path: Path, out_dir: Path):
    """Generates smart timestamped filenames."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = original_path.stem

    txt_name = f"{base_name}_OCR_{timestamp}.txt"
    img_name = f"{base_name}_OCR_{timestamp}.jpg"

    return out_dir / txt_name, out_dir / img_name


def main():
    parser = argparse.ArgumentParser(description="Interactive RapidOCR CLI.")
    parser.add_argument("--quiet", action="store_true", help="Start with verbose logging disabled.")
    args = parser.parse_args()

    is_quiet = args.quiet
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)  # Ensure /out directory exists

    clear_screen()
    print("[*] WARM-UP PHASE: Loading RapidOCR engine into memory...")
    print("[*] (This takes a few seconds, but subsequent runs will be instant)")

    # Initialize engine ONCE outside the loop
    engine = RapidOCR()

    print("[+] Engine loaded successfully!\n")

    # The next input to process. Pre-populated if passed via quick-action menu.
    next_image_path = None

    while True:
        if not next_image_path:
            raw_input = input("\n[>] Drag your image here and press Enter (or type 'q' to quit, 't' to toggle quiet): ")
        else:
            raw_input = next_image_path
            next_image_path = None  # Reset for next iteration

        # Handle UI toggles
        if raw_input.lower() == 'q':
            break
        elif raw_input.lower() == 't':
            is_quiet = not is_quiet
            print(f"[*] Quiet mode is now {'ON' if is_quiet else 'OFF'}.")
            continue
        elif not raw_input.strip():
            continue

        # 1. Path Cleansing
        clean_p = sanitize_path(raw_input)
        img_path = Path(clean_p)

        if not img_path.is_file():
            print(f"[-] Error: Could not find file at '{clean_p}'")
            continue

        # 2. OCR Processing
        if not is_quiet:
            print(f"[*] Processing '{img_path.name}'...")

        raw_output = engine(str(img_path))
        result = raw_output[0] if (isinstance(raw_output, tuple) and len(raw_output) == 2) else raw_output

        if not result:
            print("[-] No text was detected in the image.")
            continue

        # Extract Text
        extracted_lines = []
        if hasattr(result, 'txts') and result.txts:
            extracted_lines = list(result.txts)
        elif hasattr(result, 'texts') and result.texts:
            extracted_lines = list(result.texts)
        elif isinstance(result, (list, tuple)):
            for item in result:
                text_part = next((x for x in item if isinstance(x, str)), None)
                if text_part is not None:
                    extracted_lines.append(text_part)
                elif len(item) > 1:
                    extracted_lines.append(str(item[1]))

        full_text = "\n".join(extracted_lines)

        # 3. Output Generation (Smart Filenames)
        txt_out_path, img_out_path = generate_filenames(img_path, out_dir)

        # Write TXT
        with open(txt_out_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        # Write Vis Image
        vis_supported = hasattr(result, 'vis')
        if vis_supported:
            result.vis(str(img_out_path))

        if not is_quiet:
            print("\n" + "=" * 40)
            print(full_text)
            print("=" * 40)
            print(f"[+] Saved text to: {txt_out_path}")
            if vis_supported:
                print(f"[+] Saved image to: {img_out_path}")

        # Clipboard default behavior
        if pyperclip:
            try:
                pyperclip.copy(full_text)
                print("[+] Text copied to clipboard!")
            except Exception as e:
                print(f"[-] Clipboard error: {e}")

        # 4. Quick Action Menu Loop
        while True:
            action = input(
                "\n[Action] Press 'I' (Img), 'N' (Notepad), 'C' (Clear), 'q' (Quit), or Drag NEW image here: ").strip()

            if action.lower() == 'i':
                if vis_supported:
                    os.startfile(str(img_out_path))
                else:
                    print("[-] Visualization not supported by this engine version.")

            elif action.lower() == 'n':
                os.startfile(str(txt_out_path))

            elif action.lower() == 'c':
                clear_screen()

            elif action.lower() == 'q':
                sys.exit(0)

            elif action:
                # If they pasted a new path instead of a command, break out and process it!
                next_image_path = action
                break


if __name__ == "__main__":
    main()