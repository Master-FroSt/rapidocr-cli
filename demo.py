from rapidocr import RapidOCR


# Process an image from URL
# Supports HTTP/HTTPS, local file paths, and numpy arrays
img_url = "ISI_DIRECTORY_MENUJU_GAMBAR"
if img_url == "ISI_DIRECTORY_MENUJU_GAMBAR":
    print("Isi url menuju gambar!")
else:
    # Initialize the OCR engine
    # This loads the default detection, classification, and recognition models
    engine = RapidOCR()
    # The engine call performs three steps:
    # 1. Text detection (finds text regions)
    # 2. Text direction classification (0°, 90°, 180°, 270°)
    # 3. Text recognition (converts images to strings)
    result = engine(img_url)

    # Result contains a list of (text, confidence, box) tuples
    # text: recognized string
    # confidence: float between 0-1
    # box: list of 4 corner coordinates
    print(result)

    # Expected output format:
    # [(['Hello', 'World'], 0.95, [[10,10], [100,10], [100,30], [10,30]]), ...]

    # Visualize results by drawing boxes and text on the image
    # Creates a new image file with annotations
    result.vis("vis_result.jpg")