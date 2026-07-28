# services/qr_service.py

import cv2
import numpy as np


def decode_qr_image(uploaded_file):

    try:

        # Read uploaded file bytes
        file_bytes = np.asarray(
            bytearray(uploaded_file.read()),
            dtype=np.uint8
        )

        # Convert bytes into image
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
        qr_detector = cv2.QRCodeDetector()

        # Decode QR code
        data, points, _ = qr_detector.detectAndDecode(image)

        if not data:

            return {
                "success": False,
                "data": None,
                "message": "No QR code was detected in the image."
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