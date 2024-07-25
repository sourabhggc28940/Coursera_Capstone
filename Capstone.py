import os
import openpyxl
from openpyxl import Workbook

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

def save_folder_info_to_excel(folder_info, output_file):
    headers = ["Folder Name", "Total Files", "Total Size (bytes)", "File Name", "File Size (bytes)", "File Path"]
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Folder Info"
    
    # Write headers
    ws.append(headers)
    
    # Write data rows
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
            ws.append(row)
    
    # Auto-size columns
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width
    
    wb.save(output_file)

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    output_file = "folder_info.xlsx"
    folder_info = get_folder_info(directory)
    save_folder_info_to_excel(folder_info, output_file)
    print(f"Folder information saved to {output_file}")
