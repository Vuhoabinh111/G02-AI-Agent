# Ghi chú

## Tính năng đẩy file

File dạng: txt, pdf
Các bước:
- Module OCR (nếu file có dạng pdf)
- Lưu trữ file
- Xử lý và lưu vào FAISS (lưu ý cần bao gồm metadata và có id cho mỗi file)
    - Document(metadata={"id": file_id, "name": file_name, "type": file_type}, content=<file_content>)
- Tính năng xoá file: Duyệt và xoá file khỏi hệ thống (sử dụng id)