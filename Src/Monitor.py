"""
File Monitoring Script

This script monitors specific directories for new files being added. 
It periodically checks (every 10 seconds) for new files in the specified directories
and prints a message when any new file is detected.

Inputs:
- A list of directories to monitor, specified in the `MONITORED_DIRECTORIES` variable.

Outputs:
- Prints a message to the console whenever a new file is added to one of the monitored directories.

How it works:
1. The script initializes by taking a snapshot of the files currently in the monitored directories.
2. Every 10 seconds, it compares the current state of files in these directories with the previous snapshot.
3. If new files are detected (present in the current state but not in the previous snapshot), their names and paths are printed.
4. The script continues monitoring until stopped manually (e.g., using `Ctrl+C`).

Note:
- This script uses polling (checking every 10 seconds). For real-time monitoring, use libraries like `watchdog`.

Author: Riemann Derakhshan
"""

import os
import time

# Paths to monitor
MONITORED_DIRECTORIES = [
    "/Users/vahid/Desktop/AI Apps/LLMops/Data Source/Structured",
    "/Users/vahid/Desktop/AI Apps/LLMops/Data Source/Semi structured",
    "/Users/vahid/Desktop/AI Apps/LLMops/Data Source/Un structured",
]

# Dictionary to store the initial set of files in each directory
file_snapshots = {}

def initialize_snapshots(directories):
    """
    Initializes a snapshot of files in the specified directories.
    
    Parameters:
        directories (list): A list of directory paths to monitor.
    
    Returns:
        None: Updates the global file_snapshots dictionary with the initial state of files.
    """
    for directory in directories:
        # Check if the directory exists
        if os.path.exists(directory):
            # Store the initial list of files in the directory as a set
            file_snapshots[directory] = set(os.listdir(directory))
        else:
            # Handle non-existent directories gracefully
            print(f"Warning: Directory {directory} does not exist.")
            file_snapshots[directory] = set()

def check_for_new_files(directories):
    """
    Checks for new files in the monitored directories by comparing the current
    file list with the previously stored snapshot.
    
    Parameters:
        directories (list): A list of directory paths to monitor.
    
    Returns:
        None: Prints the names of newly detected files to the console.
    """
    for directory in directories:
        # Get the current list of files in the directory (if it exists)
        current_files = set(os.listdir(directory)) if os.path.exists(directory) else set()
        
        # Retrieve the previous snapshot of files
        previous_files = file_snapshots.get(directory, set())
        
        # Identify new files by finding the difference between the current and previous sets
        new_files = current_files - previous_files
        
        # Update the snapshot with the current state of files
        file_snapshots[directory] = current_files
        
        # Print a message for each newly detected file
        for new_file in new_files:
            print(f"New file uploaded: {os.path.join(directory, new_file)}")

if __name__ == "__main__":
    """
    Main execution block. Initializes the monitoring process and repeatedly
    checks for new files every 10 seconds until interrupted.
    """
    # Take an initial snapshot of the files in the directories
    initialize_snapshots(MONITORED_DIRECTORIES)
    
    print("Monitoring for new files. Press Ctrl+C to stop.")
    
    try:
        # Continuous monitoring loop
        while True:
            # Check for new files in the monitored directories
            check_for_new_files(MONITORED_DIRECTORIES)
            
            # Wait for 10 seconds before the next check
            time.sleep(10)
    except KeyboardInterrupt:
        # Graceful exit when the user interrupts the program
        print("Stopping the monitoring process.")
