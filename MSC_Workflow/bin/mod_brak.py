import sys
#Modify braken to use Krakens read length as braken take the report from kraken
def modify_tsv(file_path, output_path):
    # Read the TSV file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extract the value from the second row, second column
    value_to_copy = lines[1].split()[-1]  

    # Modify the first row to the desired format
    lines[0] = "Braken_Percentage   " + value_to_copy + "\n"

    # Write the modified lines to the output file
    with open(output_path, "w") as file:
        file.writelines(lines)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    modify_tsv(input_file, output_file)
    print("File has been modified successfully.")

