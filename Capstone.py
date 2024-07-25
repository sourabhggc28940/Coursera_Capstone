import os

def get_folder_info(directory):
    folder_info = []
    
    for root, dirs, files in os.walk(directory):
        # Get the folder name (if root is the directory itself, use the directory name)
        if root == directory:
            folder_name = os.path.basename(root) or root
        else:
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
    headers = ["Folder Name", "Total Files", "Total Size (bytes)", "File Name", "File Size (bytes)", "File Path"]
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    
    for folder in folder_info:
        for file in folder['files']:
            col_widths[0] = max(col_widths[0], len(folder['folder_name']))
            col_widths[1] = max(col_widths[1], len(str(folder['total_files'])))
            col_widths[2] = max(col_widths[2], len(str(folder['total_size'])))
            col_widths[3] = max(col_widths[3], len(file['file_name']))
            col_widths[4] = max(col_widths[4], len(str(file['file_size'])))
            col_widths[5] = max(col_widths[5], len(file['file_path']))

    def format_row(row):
        return " | ".join(f"{str(val).ljust(col_widths[i])}" for i, val in enumerate(row))
    
    # Print header
    print(format_row(headers))
    print("-+-".join('-' * width for width in col_widths))
    
    # Print rows
    for folder in folder_info:
        for file in folder['files']:
            row = [
                folder['folder_name'],
                folder['total_files'],
                folder['total_size'],
                file['file_name'],
                file['file_size'],
                file['file_path']
            ]
            print(format_row(row))

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    folder_info = get_folder_info(directory)
    print_folder_info(folder_info)
    
