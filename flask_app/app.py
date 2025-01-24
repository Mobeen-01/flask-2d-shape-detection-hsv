from flask import Flask, render_template, Response, request
import cv2
import numpy as np

app = Flask(__name__)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Default HSV range values
hsv_ranges = {
    "lh": 0, "ls": 0, "lv": 0,
    "uh": 179, "us": 255, "uv": 255
}


def get_color_name(h, s, v):
    """
    Map HSV values to a color name.
    """
    if v < 50:
        return "Black"
    elif s < 50:
        return "Gray" if v < 200 else "White"
    elif h < 15 or h > 165:
        return "Red"
    elif 15 <= h < 35:
        return "Yellow"
    elif 35 <= h < 85:
        return "Green"
    elif 85 <= h < 125:
        return "Blue"
    elif 125 <= h < 165:
        return "Purple"
    else:
        return "Unknown"


@app.route('/set_hsv', methods=['POST'])
def set_hsv():
    """
    Update HSV range based on the values from the sliders.
    """
    global hsv_ranges
    hsv_ranges = {
        "lh": int(request.form.get("lh", 0)),
        "ls": int(request.form.get("ls", 0)),
        "lv": int(request.form.get("lv", 0)),
        "uh": int(request.form.get("uh", 179)),
        "us": int(request.form.get("us", 255)),
        "uv": int(request.form.get("uv", 255)),
    }
    return '', 204


def generate_frames():
    """
    Video feed generation with shape and color detection.
    """
    global hsv_ranges

    while True:
        success, frame = cap.read()
        if not success:
            break

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
            # cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
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

            # Create mask for the detected shape
            shape_mask = np.zeros(mask.shape, np.uint8)
            cv2.drawContours(shape_mask, [approx], 0, 255, -1)

            # Compute mean HSV
            mean_val = cv2.mean(hsv, mask=shape_mask)
            h, s, v = mean_val[0], mean_val[1], mean_val[2]

            # Get color name
            if s < 50 and v > 200:
                color_name = "White"
            else:
                color_name = get_color_name(h, s, v)

            # Display shape and color
            cv2.putText(frame, f"{shape_name} - {color_name}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        # Combine frame and mask
        combined = cv2.hconcat([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])

        # Encode the frame
        _, buffer = cv2.imencode('.jpg', combined)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    """
    Render the HTML page.
    """
    return render_template('index.html')


 bbdef video_feed():
    """
    Route for the video stream.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
