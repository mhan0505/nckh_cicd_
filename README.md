# CI/CD Survey Analysis Pipeline

Hệ thống phân tích dữ liệu khảo sát CI/CD tự động, được xây dựng theo kiến trúc **Modular Data Pipeline** (3 Tầng) để thay thế cho các file Notebook khổng lồ khó quản lý.

---

## Hướng dẫn nhanh (Quick Start)

Khi có dữ liệu mới từ Google Forms, hãy thực hiện các bước sau:

0. import thư viện :

   ```
   pip install -r requirements.txt

   ```
1. **Chuẩn bị dữ liệu**:

   - Tải file phản hồi từ Google Sheets xuống máy dưới dạng `.csv`.
   - Lưu vào thư mục này với tên chính xác là: `CI_CD Survey Output - Student.csv`.
   - Nếu có các câu trả lời mở mới, hãy cập nhật vào file: `open_ended_responses.txt`.
2. **Chạy Phân tích**:

   - Mở Terminal/Command Prompt tại thư mục này.
   - Chạy lệnh "Nhạc trưởng":
     ```bash
     python run_pipeline.py
     ```
3. **Lấy kết quả**:

   - Toàn bộ biểu đồ (Pie chart, Bar chart, Pareto, WordCloud) sẽ được tự động sinh ra và lưu vào thư mục `output/`.
   - Các file dữ liệu trung gian (`.csv`) cũng được tạo ra để phục vụ việc kiểm tra chéo.

---

## Kiến trúc Hệ thống (3 Tầng)

Dự án được module hóa thành 7 Notebook chạy tuần tự:

### Tầng 1: Data Ingestion (Thu thập)

- `0_data_ingestion.ipynb`: Đọc file raw ban đầu và khởi tạo file chuẩn `responses.csv`.

### Tầng 2: Data Transformation (Tiền xử lý)

- `1a_cleanup.ipynb`: Đổi tên cột VN → English, xử lý giá trị thiếu (Missing values), chuẩn hóa kiểu dữ liệu.
- `1b_multiple_answer_cleanup.ipynb`: Xử lý câu hỏi Checkbox (nhiều đáp án) bằng kỹ thuật One-Hot Encoding.
- `1c_free_text_tagging.ipynb`: Chuẩn hóa văn bản tiếng Việt và gán nhãn chủ đề (Tagging) cho câu hỏi mở.

### Tầng 3: Data Analysis & Visualization (Phân tích)

- `2a_preliminary_analysis.ipynb`: Phân tích biến nhân khẩu học và câu hỏi lựa chọn đơn.
- `2b_multiple_answer_analysis.ipynb`: Thống kê tần suất và vẽ đồ thị Pareto cho các câu hỏi nhiều lựa chọn.
- `2c_free_text_analysis.ipynb`: Phân tích từ khóa (Top Keywords) và vẽ Mây từ vựng (WordCloud).

---

## File điều phối: `run_pipeline.py`

Đây là script Python điều phối toàn bộ hệ thống.

- **Fail-fast logic**: Nếu Tầng 1 lỗi, hệ thống sẽ dừng ngay để tránh sai sót dây chuyền.
- **Auto-verification**: Tự động kiểm tra file output sau mỗi bước.
- **Reporting**: Xuất báo cáo tổng kết thời gian chạy và danh sách biểu đồ đã tạo.

---

## Yêu cầu hệ thống

- Python 3.10+
- Thư viện: `pandas`, `matplotlib`, `seaborn`, `wordcloud`, `nbconvert`, `nbformat`.
