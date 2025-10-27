from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils.database import add_file
from ..utils.txt_converter import pdf2txt, xlsx2txt

import os

def process_file(file_path: str, ocr_dir: str):
    """
    Process a single PDF file for OCR.
    Args:
        file_name: The name of the PDF file.
        directory_path: The path to the directory containing the PDF file. If not provided, it will be inferred from the file name.
        ocr_file_path: The path to the directory where the OCR output will be saved. If not provided, it will be inferred from the directory path.
    """
    
    raw_file_name = file_path.split("/")[-1]
    welldone_file_path = ocr_dir + "/" + raw_file_name[:raw_file_name.rfind(".")] + ".txt"
    print(f"Processing {file_path} into {welldone_file_path}")

    if ".pdf" in raw_file_name:
        pdf2txt(file_path, welldone_file_path)
    elif ".txt" in raw_file_name:
        import shutil
        shutil.copy(file_path, welldone_file_path)
    elif ".xlsx" in raw_file_name:
        xlsx2txt(file_path, welldone_file_path)
    else:
        raise "Not supported file type"
    add_file(welldone_file_path)

    # user_data = str(os.listdir(USER_DATA_RAW)) + f"\nNew file: {raw_file_name}"

def process_files_parallel(directory_path, ocr_file_path, ocr_processor, max_workers):
    all_files = [filename for filename in os.listdir(directory_path) if filename.endswith(".pdf")]
    os.makedirs(ocr_file_path, exist_ok=True)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, file_name, directory_path, ocr_file_path, ocr_processor): file_name for file_name in all_files}
        for future in tqdm(as_completed(futures), total=len(all_files), desc="Processing files"):
            future.result()

def upload_file(file):
    import shutil, gradio as gr
    from ..scripts.DEFAULT import USER_DATA_RAW, USER_DATA_DIGESTABLE
    file_dir = USER_DATA_RAW
    os.makedirs(file_dir, exist_ok=True)
    shutil.copy(file, file_dir)
    if os.name == 'nt':
        file_path = file_dir + '/' + file.name[file.name.rfind("\\")+1:]
    elif os.name == 'posix':
        file_path = file_dir + '/' + file.name[file.name.rfind("/")+1:]
    process_file(file_path=file_path, ocr_dir=USER_DATA_DIGESTABLE)
    print("Success!")
    return gr.update(open=False)
