import os
import glob


def remove_files(directory):
    # Create patterns to match .csv and .db files
    csv_pattern = os.path.join(directory, "*.csv")
    db_pattern = os.path.join(directory, "*.db")

    # Find all .csv files
    csv_files = glob.glob(csv_pattern)
    # Find all .db files
    db_files = glob.glob(db_pattern)

    # Combine lists of files to remove
    files_to_remove = csv_files + db_files

    # Remove each file
    for file_path in files_to_remove:
        try:
            os.remove(file_path)
            print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")


if __name__ == "__main__":
    # Check if the directory exists
    if os.path.isdir(os.getcwd()):
        remove_files(os.getcwd())
    else:
        print("The specified directory does not exist.")
