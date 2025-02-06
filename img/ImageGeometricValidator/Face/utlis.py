import cv2
from PIL import Image

# Function to detect faces using OpenCV's Haar cascade
def detect_faces(image_path):
    """
    Detect faces in an image using OpenCV's Haar Cascade Classifier.

    :param image_path: Path to the image file.
    :return: A list of detected faces as (x, y, w, h) tuples.
    """
    # Load the pre-trained Haar cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Return the list of faces (x, y, w, h)
    return faces

# Validate the aspect ratio of the image
def validate_aspect_ratio(image_path, target_aspect_ratio=1.0, tolerance=0.1):
    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = width / height

    if abs(aspect_ratio - target_aspect_ratio) > tolerance:
        print(f"Aspect ratio {aspect_ratio} is too different from target {target_aspect_ratio}.")
        return False
    return True

# Validate the scaling and cropping of faces
def validate_scaling_cropping(image_path, detected_faces, min_face_area=0.1, max_face_area=0.8):
    image = Image.open(image_path)
    width, height = image.size

    if len(detected_faces) == 0:
        print("No faces detected in the image.")
        return False
    
    # Check each face's area as a fraction of the image's total area.
    for (x, y, w, h) in detected_faces:
        face_area = (w * h) / (width * height)
        if face_area < min_face_area or face_area > max_face_area:
            print(f"Face area {face_area*100:.2f}% is outside the allowed range ({min_face_area*100:.2f}% to {max_face_area*100:.2f}%).")
            return False
    return True

# Validate the alignment of faces within the image
def validate_alignment(image_path, detected_faces, alignment_margin=0.2):
    image = Image.open(image_path)
    width, height = image.size

    if len(detected_faces) == 0:
        print("No faces detected in the image.")
        return False
    
    for (x, y, w, h) in detected_faces:
        face_center_x = x + w / 2
        face_center_y = y + h / 2
        
        if not (width * alignment_margin < face_center_x < width * (1 - alignment_margin) and
                height * alignment_margin < face_center_y < height * (1 - alignment_margin)):
            print(f"Face center ({face_center_x}, {face_center_y}) is out of the allowed alignment range.")
            return False
    return True

# Validate the number of faces detected
def validate_face_count(detected_faces, min_faces=1, max_faces=5):
    num_faces = len(detected_faces)
    if num_faces < min_faces or num_faces > max_faces:
        print(f"Number of faces detected ({num_faces}) is out of the allowed range ({min_faces}-{max_faces}).")
        return False
    return True

# Validate face overlap
def validate_face_overlap(detected_faces, max_overlap_ratio=0.2):
    for i in range(len(detected_faces)):
        for j in range(i + 1, len(detected_faces)):
            (x1, y1, w1, h1) = detected_faces[i]
            (x2, y2, w2, h2) = detected_faces[j]
            
            # Calculate intersection area
            x_overlap = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
            y_overlap = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
            overlap_area = x_overlap * y_overlap

            # Calculate face areas
            face_area1 = w1 * h1
            face_area2 = w2 * h2
            total_area = face_area1 + face_area2 - overlap_area

            # If the overlap ratio is too high, return False
            if overlap_area / total_area > max_overlap_ratio:
                print(f"Excessive overlap between faces {i} and {j}. Overlap ratio: {overlap_area / total_area:.2f}.")
                return False
    
    return True

# Validate face size proportion
def validate_face_size_proportion(image_path, detected_faces, min_face_width_ratio=0.05, max_face_width_ratio=0.5):
    image = Image.open(image_path)
    width, height = image.size

    for (x, y, w, h) in detected_faces:
        face_width_ratio = w / width
        if face_width_ratio < min_face_width_ratio or face_width_ratio > max_face_width_ratio:
            print(f"Face width ratio {face_width_ratio*100:.2f}% is out of the allowed range ({min_face_width_ratio*100:.2f}% to {max_face_width_ratio*100:.2f}%).")
            return False

    return True

