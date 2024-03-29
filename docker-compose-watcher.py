#!/usr/bin/env python3
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    """Handles the file change events."""
    def on_any_event(self, event):
        print(f"Event detected: {event.src_path}, {event.event_type}")
        rebuild_and_restart_services()

def rebuild_and_restart_services():
    """Rebuild and restart Docker Compose services."""
    print("Building Docker Compose services...")
    try:
        # Set the current working directory to the script's directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # Build the Docker images
        subprocess.run(["docker-compose", "build"], check=True)
        print("Docker Compose services built successfully.")
        
        print("Restarting Docker Compose services...")
        # Stop, remove containers and their volumes
        subprocess.run(["docker-compose", "down", "-v"], check=True)
        # Start the containers in detached mode
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("Docker Compose services restarted successfully.")
        
        print("Fetching Docker Compose logs...")
        command = "docker-compose logs"
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while building or restarting Docker Compose services or fetching logs: {e}")

def main():
    path = os.path.dirname(os.path.abspath(__file__))  # Watch the script's directory
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    # Perform Docker Compose tasks immediately before starting to watch for file changes
    rebuild_and_restart_services()
    
    observer.start()
    print(f">>>Watching for changes in: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()