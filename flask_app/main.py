import tkinter as tk
from tkinter import ttk
from utils import update_hsv, start_video_feed
import cv2
from PIL import Image, ImageTk

class VideoStreamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Video Stream with Shape Detection")
        self.root.geometry("1000x700")
        
        self.hsv_ranges = {
            "lh": 0, "ls": 0, "lv": 0,
            "uh": 179, "us": 255, "uv": 255
        }
        
        self.video_label = ttk.Label(self.root)
        self.video_label.pack(padx=10, pady=10)

        self.controls_frame = ttk.Frame(self.root)
        self.controls_frame.pack(pady=10)

        self.create_controls()

        self.cap = cv2.VideoCapture(0)
        self.update_video_stream()

    def create_controls(self):
        self.hsv_frame = ttk.LabelFrame(self.controls_frame, text="Adjust HSV Values", padding="10")
        self.hsv_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create sliders for each HSV value
        self.sliders = {}
        for idx, (label, range_value) in enumerate(self.hsv_ranges.items()):
            slider = ttk.Scale(self.hsv_frame, from_=0, to=255 if "s" in label or "v" in label else 179,
                               orient="horizontal", command=self.update_hsv)
            slider.set(range_value)
            slider.grid(row=idx, column=0, pady=5, padx=10)
            self.sliders[label] = slider

            lbl = ttk.Label(self.hsv_frame, text=label.upper(), width=5)
            lbl.grid(row=idx, column=1, pady=5, padx=10)

        # Button to reset sliders
        self.reset_button = ttk.Button(self.controls_frame, text="Reset All", command=self.reset_sliders)
        self.reset_button.pack(pady=10)

    def update_hsv(self, event=None):
        # Update HSV ranges based on sliders
        self.hsv_ranges = {
            "lh": int(self.sliders["lh"].get()),
            "ls": int(self.sliders["ls"].get()),
            "lv": int(self.sliders["lv"].get()),
            "uh": int(self.sliders["uh"].get()),
            "us": int(self.sliders["us"].get()),
            "uv": int(self.sliders["uv"].get())
        }
        update_hsv(self.hsv_ranges)

    def reset_sliders(self):
        # Reset all sliders to default values
        for slider in self.sliders.values():
            slider.set(0 if "h" in slider.get() else 179)

    def update_video_stream(self):
        success, frame = self.cap.read()
        if success:
            frame = start_video_feed(frame, self.hsv_ranges)  # Process the frame with HSV ranges
            img = Image.fromarray(frame)
            img = img.resize((640, 480))  # Resize the image for display
            img = ImageTk.PhotoImage(img)

            self.video_label.configure(image=img)
            self.video_label.image = img

        self.root.after(10, self.update_video_stream)  # Update the frame every 10ms


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoStreamApp(root)
    root.mainloop()
