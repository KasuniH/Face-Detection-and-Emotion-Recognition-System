from datetime import datetime, timedelta
import os
import cv2
import pandas as pd


class PrivacyManager:

  @staticmethod
  def blur_unrecognized_faces(img, bbox):
    """Blurs the facial area of unidentified or non-consented individuals."""
    x, y, w, h = bbox
    if w <= 0 or h <= 0:
      return img

    # Extract Region of Interest (ROI) and apply Gaussian Blur
    roi = img[y : y + h, x : x + w]
    blurred_roi = cv2.GaussianBlur(roi, (99, 99), 30)
    img[y : y + h, x : x + w] = blurred_roi
    return img

  @staticmethod
  def enforce_data_retention(
      csv_filepath: str, retention_days: int = 30
  ) -> int:
    """Purges attendance log entries older than the retention limit (GDPR compliance)."""
    if not os.path.exists(csv_filepath):
      return 0

    df = pd.read_csv(csv_filepath)
    if df.empty or "Date" not in df.columns:
      return 0

    cutoff_date = (datetime.now() - timedelta(days=retention_days)).strftime(
        "%Y-%m-%d"
    )
    initial_count = len(df)

    # Filter out records older than cutoff date
    df_filtered = df[df["Date"] >= cutoff_date]
    purged_count = initial_count - len(df_filtered)

    if purged_count > 0:
      df_filtered.to_csv(csv_filepath, index=False)

    return purged_count
