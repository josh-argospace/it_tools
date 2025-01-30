import os

# Set the folder path and file extension
folder_path = "path/to/your/folder"  # Change this to your target folder
extension = ".txt"  # Change this to the desired file extension

# Output file
output_file = "file_list.txt"

def list_files_with_extension(folder, ext):
    """Returns a list of files in the folder that end with the given extension."""
    return [f for f in os.listdir(folder) if f.endswith(ext)]

def write_file_list(folder, ext, output):
    """Writes the list of files with the given extension to an output file."""
    files = list_files_with_extension(folder, ext)
    
    with open(output, "w") as f:
        for file in files:
            f.write(file + "\n")
    
    print(f"File list written to {output}")

# Run the function
write_file_list(folder_path, extension, output_file)
