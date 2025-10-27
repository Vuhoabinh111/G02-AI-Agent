import os
from mistralai import Mistral

class Mistral_OCR:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("API key must be provided either as an argument or in the environment variable MISTRAL_API_KEY")
        self.client = Mistral(api_key=api_key)

    def upload(self, file_path):
        uploaded_file = self.client.files.upload(
            file={
                "file_name": file_path,
                "content": open(file_path, "rb"),
            },
            purpose="ocr"
        )
        return uploaded_file

    def get_ocr(self, file_id):
        signed_url = self.client.files.get_signed_url(file_id=file_id)
        ocr_response = self.client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url.url,
            },
            include_image_base64=True
        )
        return ocr_response

    def view_uploaded(self, file_id):
        retrieved_file = self.client.files.retrieve(file_id=file_id)
        return retrieved_file