import os
import datetime

class Logger:
    def __init__(self):
        self.log_folder = "logs"
        self.filename = ""

    def create_log_file(self, filename):
        # Create the logs folder if it doesn't exist
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        # Combine the log folder path and the filename
        log_path = os.path.join(self.log_folder, filename)

        # Create a new log file
        with open(log_path, "w") as file:
            file.write("")

        print(f"Log file '{filename}' created.")
        self.filename = filename

    def log(self, message):
        if self.filename == "":
            print("No log file specified.")
            return
        # Combine the log folder path and the filename
        log_path = os.path.join(self.log_folder, self.filename)

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the log message with a timestamp to the log file
        with open(log_path, "a") as file:
            file.write(f"{timestamp}: {message}\n")

        print(f"Logged message to '{self.filename}': {message}")