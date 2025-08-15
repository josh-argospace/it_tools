import os
import glob

def generate_master_txt(folder="C:/Users/JoshGier/Desktop/TEMP/Passive_s_param/Kyocera_AVX_800r_horz"):
    # Change to the target folder (defaults to current directory)
    os.chdir(folder)
    
    # Find all files with a .S2P extension (case-sensitive)
    s2p_files = glob.glob("*.S2P")
    
    # Name of the output file
    output_filename = "Kyocera_800r_horz_sparams.txt"
    
    with open(output_filename, "w") as outfile:
        # Write the header lines
        outfile.write("BEGIN DSCRDATA\n")
        outfile.write("% INDEX filename\n")
        outfile.write("\n")
        
        # Write each file entry with an index and its full file path
        for index, s2p_file in enumerate(s2p_files, start=1):
            full_path = os.path.abspath(s2p_file)
            outfile.write(f"{index} {full_path}\n")
        
        outfile.write("\n")
        # Write the footer line
        outfile.write("END DSCRDATA\n")
    
    print(f"Generated {output_filename} with {len(s2p_files)} entries.")

if __name__ == "__main__":
    # If your .S2P files are in a different folder, provide its path here.
    generate_master_txt()

import os
import glob

def generate_master_txt(folder="."):
    # Change to the target folder (defaults to current directory)
    os.chdir(folder)
    
    # Find all files with a .S2P extension (case-sensitive)
    s2p_files = glob.glob("*.S2P")
    
    # Name of the output file
    output_filename = "filename.txt"
    
    with open(output_filename, "w") as outfile:
        # Write the header lines
        outfile.write("BEGIN DSCRDATA\n")
        outfile.write("% INDEX filename\n")
        outfile.write("\n")
        
        # Write each file entry with an index and its full file path
        for index, s2p_file in enumerate(s2p_files, start=1):
            full_path = os.path.abspath(s2p_file)
            outfile.write(f"{index} {full_path}\n")
        
        outfile.write("\n")
        # Write the footer line
        outfile.write("END DSCRDATA\n")
    
    print(f"Generated {output_filename} with {len(s2p_files)} entries.")

if __name__ == "__main__":
    # If your .S2P files are in a different folder, provide its path here.
    generate_master_txt()
