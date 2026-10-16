import cv2
from deepface import DeepFace
import numpy as np
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Face Detection & Emotion Recognition",
    page_icon="😊",
    layout="centered",
)

st.title("😊 Face Detection & Emotion Recognition App")
st.write(
    "Use your webcam to snap a photo, and the app will detect your face and analyze your emotion in real-time!"
)

# Webcam input widget
camera_image = st.camera_input("Take a picture")

if camera_image is not None:
  # Convert the uploaded image buffer to an OpenCV-readable numpy array
  bytes_data = camera_image.getvalue()
  cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

  if cv2_img is not None:
    try:
      with st.spinner("Analyzing face and emotions... Please wait."):
        # Perform emotion analysis and face detection using DeepFace
        analysis = DeepFace.analyze(
            cv2_img, actions=["emotion"], enforce_detection=False
        )

        # Ensure analysis result is iterable
        if not isinstance(analysis, list):
          analysis = [analysis]

        # Draw bounding boxes and dominant emotions on the image
        for face in analysis:
          region = face["region"]
          x, y, w, h = region["x"], region["y"], region["w"], region["h"]
          dominant_emotion = face["dominant_emotion"]

          # Draw a green rectangle around the face
          cv2.rectangle(cv2_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

          # Put text for the emotion above the rectangle
          cv2.putText(
              cv2_img,
              dominant_emotion.capitalize(),
              (x, max(y - 10, 20)),
              cv2.FONT_HERSHEY_SIMPLEX,
              0.8,
              (0, 255, 0),
              2,
          )

        # Convert OpenCV BGR image to RGB for Streamlit display
        cv2_img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

        st.success("Analysis Complete!")
        st.image(
            cv2_img_rgb,
            caption="Detected Face & Emotion",
            use_container_width=True,
        )

        # Show detailed emotion breakdown
        st.subheader("Detailed Emotion Probabilities:")
        emotions = analysis[0]["emotion"]
        for emotion, score in emotions.items():
          st.progress(
              int(score), text=f"{emotion.capitalize()}: {score:.2f}%"
          )

    except Exception as e:
      st.error(
          f"Could not detect a face or process the image. Error details: {e}"
      )
