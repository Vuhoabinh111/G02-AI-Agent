from langchain_core.tools import tool
from ..scripts.DEFAULT import USER_DATA_RAW

import os
import datetime

@tool
def list_uploaded_files() -> str:
    """
    Trả về danh sách các file mà người dùng đã upload lên hệ thống cùng với thời gian upload.
    """
    directory_path = USER_DATA_RAW
    results = []
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                info = entry.stat()
                mod_time = datetime.datetime.fromtimestamp(info.st_mtime)
                
                # Format the modification time into a string
                mod_time_str = mod_time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Create the final formatted string
                if entry.is_file():
                    line = f"File: {entry.name:<25} Last Modified: {mod_time_str}"
                    results.append(line)
                elif entry.is_dir():
                    line = f"Dir:  {entry.name:<25} Last Modified: {mod_time_str}"
                    results.append(line)
    except FileNotFoundError:
        results.append(f"Error: Directory not found at '{directory_path}'")
    except Exception as e:
        results.append(f"An error occurred: {e}")
        
    return str(results)