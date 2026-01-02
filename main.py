import time
import os
import json
from getpass import getuser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.hashing import calculate_hash
from utils.logger import setup_logger
from utils.alerts import generate_alert

# ------------------ Load Config ------------------
CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    default_config = {
        "sensitive_paths": ["/Users/Shared/SensitiveDocs"],
        "allowed_users": [getuser()],
        "alert_on_usb": True
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(default_config, f, indent=4)

with open(CONFIG_FILE) as f:
    config = json.load(f)

# ------------------ Event Handler ------------------
class MonitorHandler(FileSystemEventHandler):
    def process(self, event):
        file_path = event.src_path
        user = getuser()
        event_type = event.event_type

        # Check if file is in sensitive path
        sensitive = any(file_path.startswith(path) for path in config["sensitive_paths"])

        # Calculate hash
        file_hash = calculate_hash(file_path)

        log_message = f"{event_type.upper()} | User: {user} | Path: {file_path} | Hash: {file_hash}"
        logger.info(log_message)

        # Generate alert if unauthorized
        if sensitive and user not in config["allowed_users"]:
            generate_alert(f"Unauthorized access by {user} on sensitive file: {file_path}", logger)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

# ------------------ Main Monitoring ------------------
if __name__ == "__main__":
    log_file = "logs/file_events.log"
    logger = setup_logger(log_file)

    path_to_monitor = "."  # Current folder
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_monitor, recursive=True)

    print(f"Monitoring started on: {os.path.abspath(path_to_monitor)}")
    print(f"Logs saved to: {log_file}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

