def xlsx2txt(input_excel_file, output_text_file):
    """
    Reads an XLSX file and converts its content to a tab-separated TXT file.

    Args:
        input_excel_file (str): The path to the input .xlsx file.
        output_text_file (str): The path for the output .txt file.
    """
    import pandas as pd
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(input_excel_file)

        df.to_csv(output_text_file, sep='\t', index=False)

        print(f"Successfully converted '{input_excel_file}' to '{output_text_file}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_excel_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def pdf2txt(input_pdf_file:str, output_text_file:str, ocr_processor:any):
    """
    Reads a PDF file and converts its content to a text file.
    """
    from .mistral_ocr import Mistral_OCR
    ocr_processor = Mistral_OCR()
    uploaded_file = ocr_processor.upload(input_pdf_file)
    ocr_response = ocr_processor.get_ocr(uploaded_file.id)
    # print(ocr_response)
    with open(output_text_file, "w", encoding="utf-8") as f:
        for i,page in enumerate(ocr_response.pages):
            f.write(page.markdown +'\n')