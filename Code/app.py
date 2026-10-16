import cv2
import numpy as np
import streamlit as st
from attendance import AttendanceManager
from detector import FaceDetector
from recognizer import FaceAnalyzer

# Initialize components
st.set_page_config(
    page_title="Modular Smart Attendance", page_icon="🎯", layout="wide"
)
detector = FaceDetector()
analyzer = FaceAnalyzer()

st.title("🎯 Modular Face, Emotion & Attendance System")
st.write(
    "Take a picture via your webcam to run detection, recognition, emotion"
    " analysis, and log attendance."
)

col1, col2 = st.columns(2)

with col1:
  st.subheader("📷 Live Capture")
  camera_image = st.camera_input("Capture frame for attendance")

  if camera_image is not None:
    bytes_data = camera_image.getvalue()
    frame = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if frame is not None:
      with st.spinner("Processing face, identity, and emotion..."):
        # 1. Detect Face coordinates
        faces = detector.detect_faces(frame)

        # 2. Analyze Emotion & Identity
        emotion, region = analyzer.analyze_emotion(frame)
        name = analyzer.identify_person(frame)

        x, y, w, h = region["x"], region["y"], region["w"], region["h"]

        # 3. Draw visuals on image
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(
            frame,
            f"{name} ({emotion})",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )

        # Render image in Streamlit
        st.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            caption=f"Result: {name}",
            use_container_width=True,
        )

        # 4. Handle Attendance Logging
        if name != "Unknown":
          success, msg = AttendanceManager.log(name, emotion)
          if success:
            st.success(f"✅ Hello **{name}**! Emotion: **{emotion}**. {msg}")
          else:
            st.info(f"ℹ️ **{name}**: {msg}")
        else:
          st.warning(
              "⚠️ Face not recognized. Please add your photo to the"
              " `known_faces/` folder."
          )

with col2:
  st.subheader("📋 Attendance Records (Excel/CSV)")
  df_attendance = AttendanceManager.get_records()
  st.dataframe(df_attendance, use_container_width=True)

  if not df_attendance.empty:
    csv_data = df_attendance.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Attendance Sheet",
        data=csv_data,
        file_name="attendance.csv",
        mime="text/csv",
    )
