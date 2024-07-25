import os
import pandas as pd

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
        
        for f in files:
            file_path = os.path.join(root, f)
            file_size = os.path.getsize(file_path)
            folder_info.append({
                'folder_name': folder_name,
                'total_files': total_files,
                'total_size': total_size,
                'file_name': f,
                'file_size': file_size,
                'file_path': file_path
            })
    
    return folder_info

def save_folder_info_to_excel(folder_info, output_file):
    # Create a DataFrame from the folder info
    df = pd.DataFrame(folder_info)
    
    # Write the DataFrame to an Excel file
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    output_file = "folder_info.xlsx"
    folder_info = get_folder_info(directory)
    save_folder_info_to_excel(folder_info, output_file)
    print(f"Folder information saved to {output_file}")
