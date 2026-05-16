import logging
import os
from datetime import datetime

LOG_FILE = "audit.log"

# Wer hat wann welche Daten verarbeitet?

# Every ingestion event is timestamped to ensure traceability 
# and auditability,which is critical in regulated environments.


class AuditLogger:
    @staticmethod
    def log(event: str):
        """Append an audit event with timestamp to log file."""
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now().isoformat()} - {event}\n")
        # Also log to console
        logging.info(f"AUDIT: {event}")
    
    @staticmethod
    def get_last_n(n: int = 10):
        """Return last n lines of audit log."""
        if not os.path.exists(LOG_FILE):
            return []
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        return [line.strip() for line in lines[-n:]]

        timestamp = datetime.now()

        print(
            f"[{timestamp}] {message}"
        )