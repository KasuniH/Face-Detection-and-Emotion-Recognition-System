import cv2


class FaceDetector:

  def __init__(self, cascade_path="face_detector.xml"):
    # Fallback to OpenCV's built-in cascade if custom xml doesn't exist
    self.face_cascade = cv2.CascadeClassifier(cascade_path)
    if self.face_cascade.empty():
      self.face_cascade = cv2.CascadeClassifier(
          cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
      )

  def detect_faces(self, img):
    """Detects faces in an image and returns bounding boxes (x, y, w, h)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = self.face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=4
    )
    return faces
