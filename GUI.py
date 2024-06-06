import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
from tkinter import PhotoImage, Label
import cv2
from image_enhancement import ImageEnhancement
import threading
import time
import queue
from PIL import Image, ImageTk
import sys

# Assuming you have the detect_objects and draw_detections functions from detection.py
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolov8n.pt')

def detect_objects(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    # Perform inference using the YOLO model
    results = model(image)[0]
    # Prepare the detections list
    detections = []
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        detections.append([int(x1), int(y1), int(x2), int(y2), round(score, 3), results.names[int(class_id)]])
    return image, detections

def draw_detections(image, detections):
    # Iterate through the detections and draw rectangles
    for detection in detections:
        x1, y1, x2, y2, score, class_name = detection
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f'{class_name}: {score}'
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

class ImageEnhancementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Enhancement")
        self.root.geometry("800x500")  # Set the window size to 800x500

        # Apply dark theme
        self.style = ttk.Style("darkly")

        # Adjust label size and padding
        self.label = ttk.Label(root, text="Select an image to process", bootstyle="white", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Adjust button sizes and padding
        self.select_button = ttk.Button(root, text="Select Image", bootstyle="primary", command=self.select_image, width=20)
        self.select_button.pack(pady=10)

        self.process_button = ttk.Button(root, text="Process Image", bootstyle="success", command=self.process_image, width=20)
        self.process_button.pack(pady=10)
        self.process_button["state"] = "disabled"

        self.image_path = ""

        # Adjust loading label size and padding
        self.loading_label = ttk.Label(root, text="", bootstyle="success", font=("Helvetica", 14))
        self.loading_label.pack(pady=10)
        self.loading_animation_running = False

        # Queue for communicating between threads
        self.queue = queue.Queue()

        # Check the queue periodically
        self.root.after(100, self.check_queue)

        # Image display label
        self.image_label = Label(root)
        self.image_label.pack(pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.label.config(text=f"Selected Image: {self.image_path.split('/')[-1]}")
            self.process_button["state"] = "normal"
            self.display_image(self.image_path)

    def display_image(self, path):
        img = Image.open(path)
        img = img.resize((400, 300), Image.ANTIALIAS)
        self.img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.img_tk)

    def process_image(self):
        if not self.image_path:
            Messagebox.show_error("Error", "No image selected")
            return

        img = cv2.imread(self.image_path)
        if img is None:
            Messagebox.show_error("Error", "Could not read image")
            return

        file_name = self.image_path.split("/")[-1].split(".")[0]
        enhancer = ImageEnhancement()

        # Start the loading animation in a separate thread
        self.loading_animation_running = True
        threading.Thread(target=self.loading_animation).start()

        # Process the image in a separate thread to keep the GUI responsive
        threading.Thread(target=self.process_image_thread, args=(enhancer, img, file_name)).start()

    def process_image_thread(self, enhancer, img, file_name):
        try:
            enhancer.image_enhancement(img, file_name)
            self.queue.put(("success", "Image processed successfully. Check the output directory."))
        except Exception as e:
            self.queue.put(("error", f"An error occurred: {str(e)}"))
        finally:
            self.queue.put(("stop_loading", None))

    def loading_animation(self):
        while self.loading_animation_running:
            for frame in "|/-\\":
                if not self.loading_animation_running:
                    break
                self.loading_label.config(text=f"Processing {frame}")
                time.sleep(0.1)
        self.loading_label.config(text="")

    def check_queue(self):
        try:
            while True:
                message_type, message = self.queue.get_nowait()
                if message_type == "success":
                    Messagebox.show_info("Success", message)
                    self.display_output_image()
                elif message_type == "error":
                    Messagebox.show_error("Error", message)
                elif message_type == "stop_loading":
                    self.loading_animation_running = False
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def display_output_image(self):
        output_path = os.path.join(os.path.dirname(__file__), "output/results/gaussian_blurred_image.png")
        if not os.path.exists(output_path):
            Messagebox.show_error("Error", "Output image not found")
            return

        new_window = ttk.Toplevel()
        new_window.title("Processed Images")
        new_window.geometry("1600x800")

        # Create a frame to hold the images and labels
        image_frame = ttk.Frame(new_window)
        image_frame.pack(pady=20)

        # Original Image
        original_img = Image.open(self.image_path)
        original_img = original_img.resize((400, 300), Image.ANTIALIAS)
        self.original_img_tk = ImageTk.PhotoImage(original_img)

        original_img_label = Label(image_frame, image=self.original_img_tk)
        original_img_label.grid(row=0, column=0, padx=10)

        original_img_text = ttk.Label(image_frame, text="Original Image", bootstyle="primary", font=("Helvetica", 14))
        original_img_text.grid(row=1, column=0, padx=10)

        # Dehazed Image
        dehazed_img = Image.open(output_path)
        dehazed_img = dehazed_img.resize((400, 300), Image.ANTIALIAS)
        self.dehazed_img_tk = ImageTk.PhotoImage(dehazed_img)

        dehazed_img_label = Label(image_frame, image=self.dehazed_img_tk)
        dehazed_img_label.grid(row=0, column=1, padx=10)
        dehazed_img_text = ttk.Label(image_frame, text="Dehazed Image", bootstyle="primary", font=("Helvetica", 14))
        dehazed_img_text.grid(row=1, column=1, padx=10)

        # Perform object detection using detection.py
        image, detections = detect_objects(output_path)

        # Print the detections
        for detection in detections:
            print(detection)

        # Draw detections on the image
        image_with_detections = draw_detections(image, detections)

        # Display the image with detections
        detection_img = Image.fromarray(cv2.cvtColor(image_with_detections, cv2.COLOR_BGR2RGB))
        detection_img = detection_img.resize((400, 300), Image.ANTIALIAS)
        self.detection_img_tk = ImageTk.PhotoImage(image=detection_img)

        detection_img_label = Label(image_frame, image=self.detection_img_tk)
        detection_img_label.grid(row=0, column=2, padx=10)

        detection_img_text = ttk.Label(image_frame, text="Object Detection", bootstyle="primary", font=("Helvetica", 14))
        detection_img_text.grid(row=1, column=2, padx=10)

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ImageEnhancementApp(root)
    root.mainloop()
