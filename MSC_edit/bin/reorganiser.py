import os
import shutil
import sys

# Retrieve the directory containing files to be organized from command-line arguments
root_dir = sys.argv[1]

# List of target directory names for file organization
target_dirs = ["centrifuge", "kraken", "braken"]

# Loop through the files in the specified directory
for filename in os.listdir(root_dir):
    # Skip processing if it's a directory
    if os.path.isdir(os.path.join(root_dir, filename)):
        continue
    
    # Check if the current file should be moved to one of the target directories
    for target_dir in target_dirs:
        if target_dir in filename:
            # Ensure the target directory exists; create it if not
            os.makedirs(os.path.join(root_dir, target_dir), exist_ok=True)
            
            # Move the matched file to its corresponding target directory
            shutil.move(os.path.join(root_dir, filename), 
                        os.path.join(root_dir, target_dir, filename))
            break
