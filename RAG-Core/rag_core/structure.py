import os

def get_directory_structure(root_dir, prefix=''):
    structure = []
    
    # Get a list of files and directories in the root directory
    entries = os.listdir(root_dir)
    entries.sort()  # Sort to ensure consistent order

    # Iterate over the entries
    for i, entry in enumerate(entries):
        # Build the full path of the entry
        entry_path = os.path.join(root_dir, entry)
        
        # Determine the connector based on the position of the entry in the list
        if i == len(entries) - 1:
            connector = '┗'
            new_prefix = prefix + ' '
        else:
            connector = '┣'
            new_prefix = prefix + '┃ '

        # Add the entry to the structure list
        structure.append(f"{prefix}{connector} {entry}")
        
        # If the entry is a directory, recursively get its structure
        if os.path.isdir(entry_path):
            structure.extend(get_directory_structure(entry_path, new_prefix))

    return structure

def print_directory_structure(directory):
    structure = get_directory_structure(directory)
    directory_name = os.path.basename(directory)
    print(directory_name + '/')
    for line in structure:
        print(line)

# Directory to be listed
directory = '.'

# Print the structure of the directory
print_directory_structure(directory)
