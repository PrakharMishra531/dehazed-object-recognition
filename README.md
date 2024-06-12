# Dehazed Object Recognition
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
## Project Description

### Enhancing Object Recognition Accuracy Through Image Dehazing Using Image Pyramid

In many real-world scenarios, images captured under adverse weather conditions such as haze, fog, or smoke suffer from reduced visibility and poor contrast. This degradation significantly hampers the performance of object recognition systems, which rely on clear and detailed images to accurately detect and identify objects. Hazy images introduce ambiguity and noise, leading to lower accuracy and increased false positives and negatives in object detection tasks.

This project aims to develop a comprehensive image enhancement solution to improve the clarity and detail of images captured under hazy conditions. By leveraging the image pyramid technique, Gaussian blurring, and dark channel prior methods, we can effectively reduce haze and enhance image quality. The enhanced images will be integrated with the YOLO (You Only Look Once) object detection framework to significantly improve object recognition accuracy.

Key features of this project include:
- **Development of a robust dehazing algorithm** using the image pyramid technique.
- **Integration with the YOLO framework** for improved object detection.
- **User-friendly GUI** for easy image processing and visualization.
- **Performance validation** to demonstrate the effectiveness of the dehazing algorithm in improving object recognition accuracy.


## Tech Stack

Our project utilizes the following technologies:

| Name                  | Icon                                                                                     |
|-----------------------|------------------------------------------------------------------------------------------|
| TTKBootstrap          | ![TTKBootstrap](https://img.shields.io/badge/-TTKBootstrap-blue)                         |
| OpenCV                | ![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white) |
| NumPy                 | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=NumPy&logoColor=white)    |
| scikit-image          | ![scikit-image](https://img.shields.io/badge/scikit--image-0091ea?style=for-the-badge&logo=scikit-image&logoColor=white) |
| SciPy                 | ![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=SciPy&logoColor=white)    |
| Ultralytics           | ![Ultralytics](https://img.shields.io/badge/Ultralytics-19A974?style=for-the-badge&logo=Ultralytics&logoColor=white) |
| Pillow                | ![Pillow](https://img.shields.io/badge/Pillow-9A9A9A?style=for-the-badge&logo=Pillow&logoColor=white) |


## Demo Images

### Image 1
![Demo Image 1](demo1.jpg)

### Image 2
![Demo Image 2](demo2.jpg)

## Installation Guide

To set up the project on your local machine, follow these steps:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/PrakharMishra531/dehazed-object-recognition
    cd yourproject
    ```

2. **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
