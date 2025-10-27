Tất cả các tính năng được hiển thị lên UI. Requested features:

# Tính năng 1: Conversation

## Input
- Text:
    - Message bình thường của người dùng                                              [x]
    - Các task của người dùng:
        - Tóm tắt tài liệu                                                            [x]
        - Phân tích pháp lý                                                           [x]
        - Tìm kiếm thông tin                                                          [x]
        - Trò chuyện thông thường                                                     [x]
    - Prompt cho mô hình theo dạng phân Task như trên. (Bách phụ trách prompt)        [ ]
    - DEFAULT.py: chứa các thông số mặc định của hệ thống (bao gồm cả prompt)         [ ]
- Url:
    - Phân tích nội dung trong Url
        - Text                             [x]
        - Ảnh                              [ ]

# Tính năng 2: File_upload
- Các tài liệu được người dùng đăng lên sẽ được lưu vào thư mục user_data/raw, sau đó được xử lý và lưu vào thư mục user_data/txts, cuối cùng được lưu vào user_data/vectorstore.
- Xử lý định dạng tài liệu
    - TXT: trực tiếp copy vào thư mục user_data/txts                                 [x]
    - PDF: thực hiện OCR bằng Mistral                                                [x]
    - Các định dạng khác ...                                                         [ ]


