import os
import csv

# Set the folder path and file extension
folder_path = r"C:\Users\Public\Documents\Altium\Navigator System Controller"  # Use raw string
extension = ".SchDoc"  # Change this to the desired file extension

# Output file (writes to the same directory as the schematic files)
output_file = os.path.join(folder_path, "sch_name_list.csv")

def list_files_with_extension(folder, ext):
    """Returns a list of files in the folder that end with the given extension."""
    try:
        return [f for f in os.listdir(folder) if f.endswith(ext)]
    except FileNotFoundError:
        print(f"Error: Folder '{folder}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for folder '{folder}'.")
        return []

def write_file_list(folder, ext, output):
    """Writes the list of files with the given extension to a CSV file with additional empty columns."""
    files = list_files_with_extension(folder, ext)
    
    if not files:
        print("No matching files found.")
        return
    
    try:
        with open(output, "w", newline="") as f:
            writer = csv.writer(f)
            # Write the header with the requested columns
            writer.writerow(["Filename", "Sheet Name", "Entry Status", "Review Status", "Notes"])
            
            for file in files:
                sheet_name = os.path.splitext(file)[0]  # Remove extension
                writer.writerow([file, sheet_name, "", "", ""])  # Empty columns for Entry Status, Review Status, and Notes
        
        print(f"File list written to: {output}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Run the function
write_file_list(folder_path, extension, output_file)
