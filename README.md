import os

def get_folder_info(directory):
    folder_info = []
    
    for root, dirs, files in os.walk(directory):
        # Skip the root directory itself, we only want subdirectories
        if root == directory:
            continue
        
        folder_name = os.path.basename(root)
        total_files = len(files)
        total_size = sum(os.path.getsize(os.path.join(root, f)) for f in files)
        
        file_details = []
        for f in files:
            file_path = os.path.join(root, f)
            file_size = os.path.getsize(file_path)
            file_details.append({'file_name': f, 'file_size': file_size, 'file_path': file_path})
        
        folder_info.append({
            'folder_name': folder_name,
            'total_files': total_files,
            'total_size': total_size,
            'files': file_details
        })
    
    return folder_info

def print_folder_info(folder_info):
    for folder in folder_info:
        print(f"Folder Name: {folder['folder_name']}")
        print(f"Total Files: {folder['total_files']}")
        print(f"Total Size: {folder['total_size']} bytes")
        print("Files:")
        for file in folder['files']:
            print(f"  File Name: {file['file_name']}")
            print(f"  File Size: {file['file_size']} bytes")
            print(f"  File Path: {file['file_path']}")
        print()

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    folder_info = get_folder_info(directory)
    print_folder_info(folder_info)
