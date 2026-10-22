from datetime import datetime
import logging
import os

AUDIT_LOG_FILE = "security_audit.log"

logging.basicConfig(
    filename=AUDIT_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class AuditLogger:

  @staticmethod
  def log_event(event_type: str, details: str, user: str = "System"):
    """Logs a security audit event with timestamp and user details."""
    message = f"User: '{user}' | Event: '{event_type}' | Details: {details}"
    logging.info(message)

  @staticmethod
  def get_recent_audit_logs(lines: int = 50) -> str:
    """Retrieves recent audit entries for security review."""
    if not os.path.exists(AUDIT_LOG_FILE):
      return "No audit logs available."
    with open(AUDIT_LOG_FILE, "r") as f:
      return "".join(f.readlines()[-lines:])
