# CI/CD Survey Analysis Pipeline

Hệ thống phân tích dữ liệu khảo sát CI/CD tự động, được xây dựng theo kiến trúc **Modular Data Pipeline** (3 Tầng) để thay thế cho các file Notebook khổng lồ khó quản lý.

---

## 🎯 Ngữ cảnh Khảo sát & Bản câu hỏi (Survey Context)

Dự án này phân tích bộ dữ liệu thu thập từ cuộc khảo sát khoa học thực hiện bởi nhóm nghiên cứu trường **Đại học Kinh tế Quốc dân (NEU)** (hướng dẫn bởi Thầy Thao):
- **Đề tài**: *“Khảo sát mức độ nhận biết và triển khai CI/CD của sinh viên thuộc nhóm ngành Công nghệ Thông tin tại Việt Nam.”*
- **Mục tiêu**: Đo lường thực trạng tiếp cận, nhận thức, kinh nghiệm áp dụng thực tế và các rào cản khi sử dụng các công cụ CI/CD của sinh viên CNTT tại Việt Nam.

> [!NOTE]
> Chi tiết toàn bộ 40 câu hỏi tiếng Việt cùng với bảng ánh xạ mã hóa biến tương ứng được tài liệu hóa chi tiết tại:  
> 📋 [SURVEY_QUESTIONNAIRE.md](SURVEY_QUESTIONNAIRE.md)

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

   - Toàn bộ biểu đồ (Pie chart, Bar chart, Pareto, phân tích chủ đề câu hỏi mở và biểu đồ nâng cao) sẽ được tự động sinh ra và lưu vào thư mục `output/`.
   - Các file dữ liệu trung gian (`.csv`) và báo cáo tổng hợp cũng được tạo ra để phục vụ việc kiểm tra chéo.

---

## Kiến trúc Hệ thống (3 Tầng)

Dự án được module hóa thành 8 Notebook chạy tuần tự:

### Tầng 1: Data Ingestion (Thu thập)

- `0_data_ingestion.ipynb`: Đọc file raw ban đầu và khởi tạo file chuẩn `responses.csv`.

### Tầng 2: Data Transformation (Tiền xử lý)

- `1a_cleanup.ipynb`: Đổi tên cột VN → English, xử lý giá trị thiếu (Missing values), chuẩn hóa kiểu dữ liệu.
- `1b_multiple_answer_cleanup.ipynb`: Xử lý câu hỏi Checkbox (nhiều đáp án) bằng kỹ thuật One-Hot Encoding.
- `1c_free_text_tagging.ipynb`: Chuẩn hóa văn bản tiếng Việt và gán nhãn chủ đề (Tagging) cho câu hỏi mở.

### Tầng 3: Data Analysis & Visualization (Phân tích & Trực quan hóa)

- `2a_preliminary_analysis.ipynb`: Phân tích biến nhân khẩu học và câu hỏi lựa chọn đơn.
- `2b_multiple_answer_analysis.ipynb`: Thống kê tần suất và vẽ đồ thị Pareto cho các câu hỏi nhiều lựa chọn.
- `2c_free_text_analysis.ipynb`: Phân tích định tính câu hỏi mở: lọc nhiễu, gán chủ đề, tổng hợp insight và trích dẫn tiêu biểu.
- `3_advanced_analysis.ipynb`: Phân tích chéo nâng cao, ánh xạ **DORA Metrics** và kiểm định mô hình **UTAUT** (được mô tả chi tiết ở phần dưới).

---

## 📈 Khung Phân tích Nâng cao (Advanced Analysis)

Tệp notebook nâng cao [3_advanced_analysis.ipynb](3_advanced_analysis.ipynb) tự động chạy tập lệnh phân tích [advanced_analysis.py](advanced_analysis.py) để thực hiện kiểm chứng 20 hướng giả thuyết khoa học:
1. **Nhóm 1 - DORA metrics** (Hiệu suất DevOps thực tế): Phân loại sinh viên theo Low/Medium/High/Elite performer và kiểm định tương quan DORA score với việc áp dụng CI/CD.
2. **Nhóm 2 - Nhận thức & Thực hành**: Phân tích phễu nhận thức theo năm học, xác định khoảng cách "Biết - Làm" (Knowing-Doing Gap) và mối liên hệ giữa các công cụ với mức tự động hóa.
3. **Nhóm 3 - Nguồn học & Hiệu quả**: So sánh hiệu quả của các nguồn tiếp cận (Tự học, trường lớp, thực tập doanh nghiệp) đối với mức tự động hóa thực tế và sự tự tin nghề nghiệp.
4. **Nhóm 4 - Mô hình UTAUT** (Lý thuyết Chấp nhận Công nghệ): Kiểm định mối quan hệ tương quan Pearson và hồi quy giữa các nhân tố (Self-efficacy, Social Influence, Facilitating Conditions, Behavioral Intention, Use Behavior).
5. **Nhóm 5 - Rào cản & Đề xuất**: Bản đồ nhiệt rào cản phân bố theo năm học/mức nhận thức và phân tích giai đoạn pipeline khó khăn nhất.
6. **Nhóm 6 - Adoption Readiness**: Đo lường chỉ số sẵn sàng chấp nhận theo năm học nhằm xác định thời điểm đưa DevOps vào giảng dạy tối ưu.

> [!TIP]
> Kết quả thống kê chi tiết của phân tích chéo cùng các hệ số kiểm định được lưu tại:  
> 📝 [ADVANCED_ANALYSIS_REPORT.md](ADVANCED_ANALYSIS_REPORT.md)

---

## File điều phối: `run_pipeline.py`

Đây là script Python điều phối toàn bộ hệ thống.

- **Fail-fast logic**: Nếu Tầng 1 lỗi, hệ thống sẽ dừng ngay để tránh sai sót dây chuyền.
- **Auto-verification**: Tự động kiểm tra file output sau mỗi bước.
- **Reporting**: Xuất báo cáo tổng kết thời gian chạy và danh sách biểu đồ đã tạo.

---

## Yêu cầu hệ thống

- Python 3.10+
- Thư viện: `pandas`, `matplotlib`, `seaborn`, `nbconvert`, `nbformat`.
