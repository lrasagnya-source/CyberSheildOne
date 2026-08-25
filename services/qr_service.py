import cv2
import numpy as np


def decode_qr_image(uploaded_file):
    """
    Decode a QR code from an uploaded image.

    Returns:
        dict containing success, data, and message.
    """

    try:
        # Read uploaded file
        file_bytes = np.asarray(
            bytearray(uploaded_file.read()),
            dtype=np.uint8
        )

        # Convert bytes to OpenCV image
        image = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

        if image is None:
            return {
                "success": False,
                "data": None,
                "message": "Unable to read the uploaded image."
            }

        # Create QR detector
        detector = cv2.QRCodeDetector()

        # Detect and decode QR
        data, points, _ = detector.detectAndDecode(image)

        # Check result
        if not data:
            return {
                "success": False,
                "data": None,
                "message": "No valid QR code was detected."
            }

        return {
            "success": True,
            "data": data,
            "message": "QR code successfully decoded."
        }

    except Exception as error:
        return {
            "success": False,
            "data": None,
            "message": f"Unable to decode QR code: {error}"
        }