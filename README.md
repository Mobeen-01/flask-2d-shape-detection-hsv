# flask-2d-shape-detection-hsv
A Flask web app for real-time 2D shape detection using OpenCV and HSV color space. Detects and classifies basic geometric shapes in images, with a focus on leveraging the power of computer vision and Python's OpenCV library.

# Live Video Shape and Color Detection

This project is a Flask-based web application that uses OpenCV for live video processing to detect shapes and identify their colors in real-time. It also includes a Tkinter GUI for adjusting HSV (Hue, Saturation, Value) ranges to fine-tune the detection.

---

## Features

- **Live Video Stream**: Displays a live video feed from your webcam.  
- **Shape Detection**: Detects and labels shapes such as circles, rectangles, squares, and triangles.  
- **Color Detection**: Identifies colors of detected shapes based on HSV values.  
- **Dynamic HSV Adjustment**: Modify HSV range values via a web-based interface or a Tkinter GUI for real-time fine-tuning.  
- **User-Friendly Design**: Intuitive UI with sliders and a live preview for seamless adjustments.

---

## Technologies Used

- **Flask**: Backend framework for routing and video streaming.  
- **OpenCV**: Real-time computer vision for shape and color detection.  
- **Tkinter**: GUI for HSV range adjustments.  
- **HTML/CSS**: Frontend design for a responsive user interface.

---

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/live-video-shape-color-detection.git
   cd live-video-shape-color-detection
   ```

2. Navigate to the `flask_app` folder in Visual Studio Code and open the terminal.

3. Install the required libraries:  
   ```bash
   pip install Flask opencv-python numpy
   ```

4. Run the `app.py` file:  
   ```bash
   python app.py
   ```

5. Open your browser and go to the address:  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Usage

1. **Start the Application**: Launch the Flask app by running `app.py` and access the web interface.  
2. **Adjust HSV Ranges**: Use the Tkinter GUI or the web-based sliders to adjust HSV values for better detection.  
3. **Live Preview**: View the processed video stream with detected shapes and their respective colors.


## Video Tutorial

A video tutorial demonstrating how to use the algorithm and adjust settings has been included for a better understanding of the application.

#Flask #OpenCV #ShapeDetection #2DShapeDetection #HSV #ComputerVision #Python #MachineLearning #AI #DeepLearning #ImageProcessing #FlaskApp #OpenCVPython #DataScience #TechProjects

