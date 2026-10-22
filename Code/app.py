import cv2
import numpy as np
import streamlit as st
from attendance import AttendanceManager
from audit import AuditLogger
from auth import AuthManager
from detector import FaceDetector
from privacy import PrivacyManager
from recognizer import FaceAnalyzer
from security import SecurityManager

# Initialize Security & Privacy Managers
sec_mgr = SecurityManager()
detector = FaceDetector()
analyzer = FaceAnalyzer()

st.set_page_config(
    page_title="Secure Attendance & Emotion System",
    page_icon="🛡️",
    layout="wide",
)

# 1. Sidebar Authentication & Governance Controls
AuthManager.render_login_form()

st.sidebar.markdown("---")
st.sidebar.subheader("⚖️ Privacy & Compliance")
consent_given = st.sidebar.checkbox(
    "I consent to biometric identification and emotion analysis", value=True
)

if st.sidebar.button("🧹 Enforce Data Retention (Purge >30 days)"):
  purged = PrivacyManager.enforce_data_retention("attendance.csv", 30)
  st.sidebar.success(f"Purged {purged} expired log records.")
  AuditLogger.log_event("DATA_PURGE", f"Purged {purged} old records.")

st.title("🛡️ Secure Smart Attendance & Emotion Tracker")

col1, col2 = st.columns(2)

with col1:
  st.subheader("📷 Live Capture")

  if not consent_given:
    st.warning("⚠️ Biometric consent is required to process video feed.")
  else:
    camera_image = st.camera_input("Capture frame")

    if camera_image is not None:
      frame = cv2.imdecode(
          np.frombuffer(camera_image.getvalue(), np.uint8), cv2.IMREAD_COLOR
      )

      if frame is not None:
        emotion, region = analyzer.analyze_emotion(frame)
        name = analyzer.identify_person(frame)
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]

        # Privacy Protection: Blur face if unknown or unrecognised
        if name == "Unknown":
          frame = PrivacyManager.blur_unrecognized_faces(frame, (x, y, w, h))
          st.warning("⚠️ Unknown face detected and anonymized for privacy.")
          AuditLogger.log_event(
              "UNKNOWN_FACE", "Unidentified face detected and blurred."
          )
        else:
          cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
          cv2.putText(
              frame,
              f"{name} ({emotion})",
              (x, max(y - 10, 20)),
              cv2.FONT_HERSHEY_SIMPLEX,
              0.6,
              (0, 255, 0),
              2,
          )

          # Log attendance
          success, msg = AttendanceManager.log(name, emotion)
          if success:
            st.success(f"✅ Hello {name}! {msg}")
            AuditLogger.log_event(
                "ATTENDANCE_LOGGED", f"Logged {name} with emotion {emotion}"
            )

        st.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True
        )

with col2:
  st.subheader("📋 Protected Attendance Records")

  # Enforce Access Control: Only authenticated users can view/export data
  if st.session_state.get("authenticated", False):
    df_attendance = AttendanceManager.get_records()
    st.dataframe(df_attendance, use_container_width=True)

    csv_data = df_attendance.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Export CSV Sheet",
        data=csv_data,
        file_name="secure_attendance.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.subheader("📜 Security Audit Log")
    st.text_area(
        "Audit Log Stream",
        AuditLogger.get_recent_audit_logs(),
        height=180,
    )
  else:
    st.info(
        "🔒 Attendance records and security logs are locked. Please log in"
        " via the sidebar to view sensitive data."
    )
