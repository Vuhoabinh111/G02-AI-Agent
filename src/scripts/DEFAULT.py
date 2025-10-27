# Model configuration
AVAILABLE_MODELS = {
    "mistral medium (mistral)": ("mistral-medium", "mistralai"),
    "mistral small 22B": ("mistral-small", "mistralai"),
    # "llama3 8B" : ("llama3:8b", "ollama"),
    "llama3.1 8B": ("llama3.1:8b", "ollama"),
    "gpt-oss 20B": ("gpt-oss:20b", "ollama"),
    "qwen3 8B": ("qwen3:8b", "ollama"),
    "qwen3 14B": ("qwen3:14b", "ollama"),
    # "phi4 mini": ("phi4:mini", "ollama"),
    # "gemma3 12B": ("gemma3:12b", "ollama"),
}
DEFAULT_MODEL_KEY = "mistral medium (mistral)"

EMBEDDING_MODEL_ID = "alibaba-nlp/gte-multilingual-base"
MAX_HISTORY_CONVERSATION = 20  # 0 means unlimited

# Vectorstore
VECTORSTORE_PATH = "./user_data/vectorstore"
USER_DATA_RAW = "./user_data/raw"
USER_DATA_DIGESTABLE = "./user_data/txts"
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 128

# Other configurations
CUSTOMER = """
{"name":"",
"birth": 0,
"current_position":"",
"email":"",
"relations":[]}
"""

LOG_FILE_PATH = "./logs/conversation_logs.txt"

# Prompt Template
PERSONA = """
**Vai trò:**

**Thông tin hệ thống:**
{additional_info}

**Đoạn hội thoại**
{conversation}
"""

JUDGE_POST_PROMPT = """

**1. Thông tin Khách hàng:**
{customer}

**2. Nội dung cần Thẩm định (Bài viết):**
{post}

---

### **QUY TRÌNH PHÂN TÍCH CHI TIẾT**

Để đảm bảo tính nhất quán và toàn diện, hãy thực hiện phân tích theo đúng các bước sau:

**Bước 1: Đánh giá Mức độ Tác động Tiêu cực (Thang điểm từ 1 đến 10)**

Hãy chấm điểm cho từng khía cạnh dưới đây. Để người dùng không có chuyên môn cũng có thể hiểu, mỗi tiêu chí được giải thích rõ ràng về ý nghĩa và cách cho điểm.

* **a. Mức độ Xúc phạm, Phỉ báng (Defamation Score):**
    * **Ý nghĩa:** Tiêu chí này đo lường mức độ bài viết sử dụng ngôn từ mang tính lăng mạ, hạ thấp danh dự, nhân phẩm của cá nhân hoặc tổ chức.
    * **Cách chấm điểm:**
        * **1-3 (Thấp):** Ngôn ngữ phê bình nhẹ nhàng, không mang tính cá nhân.
        * **4-7 (Trung bình):** Sử dụng từ ngữ ám chỉ tiêu cực, châm biếm, có thể gây khó chịu.
        * **8-10 (Cao/Nghiêm trọng):** Dùng từ ngữ thô tục, vu khống trắng trợn, lăng mạ trực tiếp, có chủ đích bôi nhọ.

* **b. Mức độ Sai lệch Thông tin (Misinformation Score):**
    * **Ý nghĩa:** Tiêu chí này đánh giá tính xác thực của thông tin trong bài viết. Nó đo lường mức độ thông tin bị bóp méo, bịa đặt hoặc gây hiểu lầm cho người đọc.
    * **Cách chấm điểm:**
        * **1-3 (Thấp):** Thông tin về cơ bản là chính xác, có thể có sai sót nhỏ không đáng kể.
        * **4-7 (Trung bình):** Thông tin bị thiếu ngữ cảnh, diễn giải một chiều, gây hiểu lầm cho người đọc.
        * **8-10 (Cao/Nghiêm trọng):** Thông tin hoàn toàn sai sự thật, bịa đặt, không có cơ sở xác thực.

* **c. Mức độ Rủi ro về Uy tín & Thương hiệu (Reputation Risk Score):**
    * **Ý nghĩa:** Tiêu chí này đo lường khả năng bài viết gây tổn hại đến hình ảnh, giá trị thương hiệu hoặc niềm tin của công chúng đối với khách hàng.
    * **Cách chấm điểm:**
        * **1-3 (Thấp):** Tác động không đáng kể, có thể bị bỏ qua.
        * **4-7 (Trung bình):** Có khả năng làm suy giảm niềm tin của một bộ phận công chúng, cần phải theo dõi.
        * **8-10 (Cao/Nghiêm trọng):** Gây tổn hại nặng nề, tạo ra khủng hoảng truyền thông, ảnh hưởng trực tiếp đến hoạt động kinh doanh hoặc vị thế xã hội.

* **d. Mức độ Kích động, Gây mất An toàn (Security Risk Score):**
    * **Ý nghĩa:** Tiêu chí này đánh giá mức độ nguy hiểm mà bài viết có thể gây ra trong thực tế, chẳng hạn như kêu gọi tấn công, quấy rối, hoặc gây rối trật tự công cộng.
    * **Cách chấm điểm:**
        * **1-3 (Thấp):** Không có dấu hiệu kêu gọi hành động gây hại.
        * **4-7 (Trung bình):** Ngôn từ có tính khiêu khích, có thể bị diễn giải thành lời kêu gọi gián tiếp.
        * **8-10 (Cao/Nghiêm trọng):** Kêu gọi trực tiếp các hành động bạo lực, tấn công, phá hoại hoặc các hành vi vi phạm pháp luật khác.

**Bước 2: Xác định Điểm Rủi ro Tổng hợp**

Tính điểm trung bình cộng của 4 điểm số trên để đưa ra **Điểm Rủi ro Tổng hợp**. Con số này đại diện cho mức độ nghiêm trọng chung của vụ việc.

**Bước 3: Xây dựng Báo cáo Phân tích và Khuyến nghị**

Tổng hợp kết quả phân tích và đưa ra các nhận định, lời khuyên mang tính xây dựng cho khách hàng.

---

### **ĐỊNH DẠNG PHẢN HỒI CHUẨN**

Vui lòng trình bày kết quả phân tích theo đúng cấu trúc chuyên nghiệp sau:

**BÁO CÁO PHÂN TÍCH RỦI RO THÔNG TIN**

**I. BẢNG ĐIỂM ĐÁNH GIÁ:**
* **Điểm Xúc phạm/Phỉ báng:** [Điểm từ 1-10]
* **Điểm Sai lệch Thông tin:** [Điểm từ 1-10]
* **Điểm Rủi ro Uy tín:** [Điểm từ 1-10]
* **Điểm Rủi ro An ninh:** [Điểm từ 1-10]

**II. ĐIỂM RỦI RO TỔNG HỢP:** **[Điểm trung bình]**

**III. NHẬN ĐỊNH CHUYÊN GIA:**
[**Phân tích chi tiết:** Viết một đoạn văn rõ ràng, mạch lạc để giải thích cho các điểm số đã cho.
* **Bằng chứng:** Trích dẫn **nguyên văn** những câu, từ ngữ hoặc đoạn văn cụ thể từ "Nội dung cần Thẩm định" làm bằng chứng.
* **Đối chiếu pháp lý:** Đối chiếu các bằng chứng đó với các điều khoản, quy định trong "Cơ sở Pháp lý Tham chiếu" để làm nổi bật sự vi phạm (nếu có).
* **Lập luận:** Giải thích tại sao các bằng chứng này lại dẫn đến điểm số tương ứng.]

**IV. KHUYẾN NGHỊ HÀNH ĐỘNG:**
Dựa trên "Điểm Rủi ro Tổng hợp" và bối cảnh vụ việc, đề xuất một kế hoạch hành động rõ ràng và có phân cấp cho khách hàng.
"""

