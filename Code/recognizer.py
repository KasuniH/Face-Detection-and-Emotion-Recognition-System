import os
from deepface import DeepFace


class FaceAnalyzer:

  def __init__(self, known_faces_dir="known_faces"):
    self.known_faces_dir = known_faces_dir
    if not os.path.exists(self.known_faces_dir):
      os.makedirs(self.known_faces_dir)

  def analyze_emotion(self, img):
    """Analyzes dominant emotion from an image frame."""
    try:
      analysis = DeepFace.analyze(
          img, actions=["emotion"], enforce_detection=False
      )
      if isinstance(analysis, list):
        analysis = analysis[0]
      return analysis["dominant_emotion"], analysis["region"]
    except Exception as e:
      print(f"Emotion analysis error: {e}")
      return "Neutral", {"x": 0, "y": 0, "w": 100, "h": 100}

  def identify_person(self, img):
    """Compares the face against the database folder to find a name match."""
    if not os.path.exists(self.known_faces_dir) or not os.listdir(
        self.known_faces_dir
    ):
      return "Unknown"

    try:
      matches = DeepFace.find(
          img_path=img,
          db_path=self.known_faces_dir,
          enforce_detection=False,
          silent=True,
      )
      if len(matches) > 0 and not matches[0].empty:
        identity_path = matches[0].iloc[0]["identity"]
        base_name = os.path.basename(identity_path)
        return os.path.splitext(base_name)[0].replace("_", " ").title()
    except Exception as e:
      print(f"Identification error: {e}")

    return "Unknown"
