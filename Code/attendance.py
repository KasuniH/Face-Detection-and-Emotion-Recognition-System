from datetime import datetime
import os
import pandas as pd

ATTENDANCE_FILE = "attendance.csv"


class AttendanceManager:

  @staticmethod
  def log(name: str, emotion: str) -> tuple[bool, str]:
    """Logs attendance to a CSV file (compatible with Excel & Google Sheets)."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    if not os.path.exists(ATTENDANCE_FILE):
      df = pd.DataFrame(columns=["Name", "Date", "Time", "Emotion"])
      df.to_csv(ATTENDANCE_FILE, index=False)

    df = pd.read_csv(ATTENDANCE_FILE)

    # Check if already logged today
    already_logged = not df[
        (df["Name"] == name) & (df["Date"] == date_str)
    ].empty

    if not already_logged:
      new_row = pd.DataFrame([{
          "Name": name,
          "Date": date_str,
          "Time": time_str,
          "Emotion": emotion.capitalize(),
      }])
      df = pd.concat([df, new_row], ignore_index=True)
      df.to_csv(ATTENDANCE_FILE, index=False)
      return True, f"Successfully checked in at {time_str}!"
    else:
      return False, "Attendance already marked for today."

  @staticmethod
  def get_records() -> pd.DataFrame:
    if os.path.exists(ATTENDANCE_FILE):
      return pd.read_csv(ATTENDANCE_FILE)
    return pd.DataFrame(columns=["Name", "Date", "Time", "Emotion"])
