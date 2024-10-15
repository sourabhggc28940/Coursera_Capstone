
import os
import csv
import stat
import hashlib

def get_file_permissions(file_path):
    """Get file permissions as a string encapsulated within single quotes."""
    try:
        # Check if the file is a symbolic link
        if os.path.islink(file_path):
            # Handle broken symlinks
            if not os.path.exists(file_path):
                return "'broken_symlink'"
            else:
                # Get permissions of the symlink target
                mode = os.lstat(file_path).st_mode
        else:
            # Get permissions of a regular file
            mode = os.stat(file_path).st_mode
        
        permissions = stat.filemode(mode)
        return f"'{permissions}'"  # Enclose permissions in single quotes
    except Exception as e:
        return f"Error: {e}"

def get_file_checksum(file_path):
    md5_hash = hashlib.md5()
    try:
        if os.path.islink(file_path) and not os.path.exists(file_path):
            return "broken_symlink"
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def get_folder_info(directory, folders_to_skip=None):
    folder_info = []

    # Convert folders_to_skip to a list if it's provided, otherwise, use an empty list
    folders_to_skip = folders_to_skip or []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        # Skip folders that match any path in the folders_to_skip list
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in folders_to_skip]

        folder_name = os.path.basename(root) or root
        total_files = len(files)
        total_size = sum(os.path.getsize(os.path.join(root, f)) for f in files if os.path.exists(os.path.join(root, f)))

        # If there are no files, add the folder information with zero files and size
        if total_files == 0:
            folder_info.append({
                'folder_name': folder_name,
                'total_files': total_files,
                'total_size': total_size,
                'file_name': None,
                'file_size': None,
                'file_path': None,
                'file_permissions': None,
                'file_checksum': None
            })
        else:
            for f in files:
                file_path = os.path.join(root, f)
                if os.path.exists(file_path) or os.path.islink(file_path):
                    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'
                    file_permissions = get_file_permissions(file_path)
                    file_checksum = get_file_checksum(file_path)
                    folder_info.append({
                        'folder_name': folder_name,
                        'total_files': total_files,
                        'total_size': total_size,
                        'file_name': f,
                        'file_size': file_size,
                        'file_path': file_path,
                        'file_permissions': file_permissions,
                        'file_checksum': file_checksum
                    })

    return folder_info

def save_folder_info_to_csv(folder_info, output_file):
    # Define CSV headers
    headers = ['folder_name', 'total_files', 'total_size', 'file_name', 'file_size', 'file_path', 'file_permissions', 'file_checksum']
    
    # Open the CSV file for writing
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the headers
        writer.writeheader()
        
        # Write the rows
        for info in folder_info:
            writer.writerow(info)

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    
    # Input multiple folder paths to skip, comma-separated, or leave blank to skip none
    folders_to_skip_input = input("Enter folder paths to skip (comma-separated, or leave blank to skip none): ")
    
    # Convert input string to a list of folder paths if provided
    folders_to_skip = [folder.strip() for folder in folders_to_skip_input.split(',')] if folders_to_skip_input else None
    
    output_file = "folder_info.csv"
    folder_info = get_folder_info(directory, folders_to_skip)
    save_folder_info_to_csv(folder_info, output_file)
    print(f"Folder information saved to {output_file}")
