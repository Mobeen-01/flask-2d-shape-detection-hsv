import numpy as np
import cv2

# The global hsv_ranges will be passed as a parameter, no need to declare it as global here
def update_hsv(hsv_ranges):
    """
    This function updates the HSV ranges (called from Tkinter GUI).
    """
    # No need for global here, just use the passed parameter
    return hsv_ranges  # You can modify the hsv_ranges if needed

def start_video_feed(frame, hsv_ranges):
    """
    This function processes each frame from the video capture.
    It applies the HSV filtering and shape detection.
    """
    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV range from sliders
    lower_bound = np.array([hsv_ranges["lh"], hsv_ranges["ls"], hsv_ranges["lv"]])
    upper_bound = np.array([hsv_ranges["uh"], hsv_ranges["us"], hsv_ranges["uv"]])

    # Create mask based on HSV range
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Perform morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 400:
            continue

        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        # Draw contours
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)

        # Identify shape
        vertices = len(approx)
        if vertices == 3:
            shape_name = "Triangle"
        elif vertices == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            shape_name = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        elif vertices > 6:
            shape_name = "Circle"
        else:
            shape_name = "Unknown"

        # Display shape and color
        cv2.putText(frame, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    return frame
