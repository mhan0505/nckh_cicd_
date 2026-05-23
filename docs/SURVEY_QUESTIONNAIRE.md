# Ngữ cảnh Nghiên cứu & Bản câu hỏi Khảo sát CI/CD

Tài liệu này cung cấp toàn bộ ngữ cảnh, thông tin nghiên cứu khoa học và cấu trúc bảng câu hỏi khảo sát mức độ nhận biết và triển khai CI/CD của sinh viên thuộc nhóm ngành Công nghệ Thông tin tại Việt Nam. Đồng thời, tài liệu cung cấp bảng ánh xạ chi tiết các câu hỏi tiếng Việt sang mã biến (`timestamp`, `Q1` đến `Q40`) trong hệ thống phân tích dữ liệu tự động.

---

## 1. Thông tin chung về Đề tài & Khảo sát

> [!NOTE]
> **Nhóm nghiên cứu**: Nhóm sinh viên/nghiên cứu viên đến từ **Đại học Kinh tế Quốc dân (NEU)**, Hà Nội, Việt Nam.  
> **Giảng viên hướng dẫn**: Thầy Thảo.  
> **Đề tài**: *“Khảo sát mức độ nhận biết và triển khai CI/CD của sinh viên thuộc nhóm ngành Công nghệ Thông tin tại Việt Nam.”*

### Mục tiêu Khảo sát
1. Thu thập dữ liệu thực tế về mức độ nhận biết và hiểu biết khái niệm CI/CD của sinh viên Công nghệ Thông tin tại Việt Nam.
2. Đo lường kinh nghiệm sử dụng thực tế, các công cụ CI/CD phổ biến và mức độ tự động hóa trong các đồ án/dự án của sinh viên.
3. Đánh giá hiệu suất phát triển phần mềm dựa trên các chỉ số **DORA Metrics** (Deployment Frequency, Lead Time for Changes, Mean Time to Recovery, Change Failure Rate).
4. Phân tích các rào cản, khó khăn khi tiếp cận DevOps/CICD bằng lý thuyết chấp nhận công nghệ **UTAUT** (Performance Expectancy, Effort Expectancy, Social Influence, Facilitating Conditions, Behavioral Intention, Use Behavior).
5. Thu thập ý kiến đóng góp, đề xuất từ sinh viên nhằm cải thiện chương trình giảng dạy và hỗ trợ từ nhà trường.

### Phương pháp Thu thập
- **Đối tượng**: Sinh viên các khóa ngành Công nghệ Thông tin, Kỹ thuật Phần mềm, Khoa học Máy tính... tại Việt Nam.
- **Tính chất**: Khảo sát hoàn toàn tự nguyện, ẩn danh và bảo mật thông tin tuyệt đối, chỉ phục vụ nghiên cứu khoa học.
- **Thời lượng dự kiến**: 10 – 15 phút.

---

## 2. Bảng ánh xạ mã biến & Cấu trúc câu hỏi (Q1 - Q40)

Dưới đây là chi tiết toàn bộ bảng câu hỏi khảo sát và cách chúng được đổi tên trong file xử lý tiền dữ liệu [1a_cleanup.ipynb](file:///d:/NCKH_thay_Thao/data/1a_cleanup.ipynb) phục vụ cho pipeline phân tích.

### Phần 1: Thông tin cá nhân (Nhân khẩu học)

| Mã câu hỏi | Nội dung câu hỏi gốc | Loại câu hỏi | Phương án trả lời / Ghi chú |
| :--- | :--- | :--- | :--- |
| `timestamp` | Dấu thời gian | Hệ thống | Thời gian submit biểu mẫu |
| `Q1_university` | Bạn đang học tại trường nào? * | Single-choice | Đại học Kinh Tế Quốc Dân, Đại học Bách Khoa Hà Nội, Đại học Công Nghệ (ĐHQGHN), Đại học FPT, Đại học Giao thông Vận tải, Mục khác |
| `Q2_year` | Bạn đang học năm mấy? * | Single-choice | Năm 1, Năm 2, Năm 3, Năm 4, Năm 5 hoặc đã tốt nghiệp, Mục khác |
| `Q3_major` | Chuyên ngành hướng đào tạo chính của bạn? * | Single-choice | Công nghệ thông tin, Kỹ thuật phần mềm, Khoa học máy tính, Hệ thống thông tin / Tin học quản lý, An toàn thông tin / Mạng máy tính, Trí tuệ nhân tạo / Khoa học dữ liệu, Toán Tin, Mục khác |
| `Q4_product_field` | Lĩnh vực / Sản phẩm chính mà bạn đang thực hiện? * | Checkbox (Nhiều lựa chọn) | Phần mềm ứng dụng (Web, Mobile, Desktop App), Hệ thống AI/Big Data/Data Science, Hệ thống nhúng (Embedded)/IoT, Giải pháp hạ tầng & Bảo mật, Mục khác |

---

### Phần 2: Thực trạng tiếp cận và áp dụng CI/CD

| Mã câu hỏi            | Nội dung câu hỏi gốc                                                                                | Loại câu hỏi              | Phương án trả lời / Ghi chú                                                                                                                                                                                                                                                                                            |
| :----------------------| :----------------------------------------------------------------------------------------------------| :--------------------------| :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Q5_cicd_awareness`   | Bạn đã từng nghe đến thuật ngữ CI/CD (Continuous Integration / Continuous Deployment) chưa?         | Single-choice             | Chưa bao giờ nghe *(Chuyển đến Q38)*, Có nghe qua nhưng chưa hiểu rõ, Biết khái niệm cơ bản, Hiểu rõ và có thể giải thích cho người khác                                                                                                                                                                               |
| `Q6_automation_level` | Mức độ tự động hóa trong các dự án lập trình mà bạn từng thực hiện là gì? *                         | Single-choice             | Hoàn toàn thủ công, Tự động hóa một phần nhỏ (ví dụ: chỉ tự động Build), Tự động hóa trung bình (ví dụ: Build và Test tự động cơ bản), Tự động hóa cao (ví dụ: đã có Pipeline tích hợp hầu hết các bước), Tự động hóa hoàn toàn (CI/CD khép kín, tối ưu)                                                               |
| `Q7_tools_used`       | Bạn đã từng sử dụng công cụ CI/CD nào trong quá trình học tập hoặc làm dự án cá nhân? *             | Checkbox (Nhiều lựa chọn) | Jenkins, GitLab CI/CD, GitHub Actions, Circle CI, Travis CI, Chưa từng sử dụng công cụ CI/CD nào, Mục khác                                                                                                                                                                                                             |
| `Q8_learning_source`  | Bạn đã tiếp cận CI/CD chủ yếu thông qua nguồn nào?                                                  | Checkbox (Nhiều lựa chọn) | Môn học tại trường đại học, Dự án cá nhân / Đồ án môn học, Thực tập tại doanh nghiệp, Khóa học online (Coursera, YouTube, ...), Tự tìm hiểu qua tài liệu trên Internet, Mục khác                                                                                                                                       |
| `Q9_usage_purpose`    | Bạn sử dụng các công cụ CI/CD đã chọn cho những mục đích nào trong quy trình phát triển phần mềm? * | Checkbox (Nhiều lựa chọn) | Build / Tự động hoá quá trình build, Continuous Integration (CI) – tích hợp & kiểm tra mã nguồn tự động, Continuous Deployment / Delivery (CD) – triển khai tự động, Automated Testing – kiểm thử tự động, Tự động hoá quy trình phát triển (workflow automation), Học tập / nghiên cứu / thử nghiệm cá nhân, Mục khác |
| `Q10_cicd_benefits`   | Theo bạn, CI/CD giúp cải thiện điều gì trong quy trình phát triển phần mềm? *                       | Checkbox (Nhiều lựa chọn) | Tự động hóa quy trình build và test, Phát hiện lỗi sớm hơn, Tăng tốc độ phát triển phần mềm, Hỗ trợ làm việc nhóm tốt hơn, Giảm lỗi khi triển khai phần mềm, Mục khác                                                                                                                                                  |

---

### Phần 3: Chỉ số Hiệu suất Phát triển (DORA Metrics)

> [!TIP]
> Bốn câu hỏi này đo lường các chỉ số DORA tiêu chuẩn để đánh giá hiệu suất kỹ thuật (DevOps Performance) của nhóm phát triển dự án.

| Mã câu hỏi | Nội dung câu hỏi gốc | Loại câu hỏi | Phương án trả lời / Ghi chú |
| :--- | :--- | :--- | :--- |
| `Q11_deploy_frequency` | Trong các dự án lập trình mà bạn từng thực hiện (đồ án, project cá nhân, hoặc project nhóm), bạn cập nhật phiên bản mới của ứng dụng lên môi trường chạy thử (server, hosting, cloud, v.v.) với tần suất như thế nào? * | Single-choice | Nhiều lần trong ngày, Từ một lần mỗi ngày đến một lần mỗi tuần, Từ một lần mỗi tuần đến một lần mỗi tháng, Từ một lần mỗi tháng đến một lần sáu tháng, Ít hơn một lần sáu tháng |
| `Q12_lead_time` | Kể từ thời điểm bạn hoàn thành việc viết code và đẩy lên hệ thống (commit), mất bao lâu để những thay đổi đó thực sự chạy thành công trên môi trường cho người dùng cuối (Production)? * | Single-choice | Dưới 1 giờ, Từ 1 giờ đến dưới 1 ngày, Từ 1 ngày đến dưới 1 tuần, Từ 1 tuần đến dưới 1 tháng, Trên 1 tháng |
| `Q13_recovery_time` | Khi dự án của bạn gặp lỗi nghiêm trọng sau khi cập nhật code (ví dụ: ứng dụng không chạy, lỗi server, lỗi chức năng), bạn thường mất bao lâu để khắc phục và đưa hệ thống hoạt động bình thường trở lại? * | Single-choice | Dưới 1 giờ, Từ 1 giờ đến dưới 1 ngày, Từ 1 ngày đến dưới 1 tuần, Trên 1 tuần |
| `Q14_failure_rate` | Trong các lần bạn cập nhật hoặc triển khai phiên bản mới của dự án (đồ án, project cá nhân, hoặc project nhóm), tỷ lệ gặp lỗi nghiêm trọng khiến hệ thống không hoạt động đúng thường ở mức nào? * | Single-choice | 0% - 15% (Rất thấp), 16% - 30% (Thấp), 31% - 45% (Trung bình), Trên 45% (Cao) |

---

### Phần 4: Đánh giá cảm nhận cá nhân & Ý định sử dụng (Thang đo Likert 1-5)

> [!IMPORTANT]
> Thang đo Likert từ **1 (Hoàn toàn không đồng ý)** đến **5 (Hoàn toàn đồng ý)**. Các câu này được phân nhóm theo các nhân tố của **Mô hình Chấp nhận Công nghệ (UTAUT)** trong phân tích nâng cao.

| Mã câu hỏi | Nội dung câu hỏi gốc | Nhóm UTAUT | Ý nghĩa đo lường |
| :--- | :--- | :--- | :--- |
| `Q15_save_time` | CI/CD giúp tôi tiết kiệm thời gian triển khai trong các dự án học tập | **Performance Expectancy (PE)** | Kỳ vọng hiệu quả công việc |
| `Q16_early_bug_detect` | CI/CD giúp tôi phát hiện lỗi code sớm hơn so với kiểm tra thủ công | **Performance Expectancy (PE)** | Kỳ vọng hiệu quả công việc |
| `Q17_job_confidence` | Biết sử dụng CI/CD giúp tôi tự tin hơn khi thực tập hoặc xin việc | **Performance Expectancy (PE)** | Kỳ vọng giá trị nghề nghiệp |
| `Q18_ease_of_learning` | Tôi thấy việc tìm hiểu CI/CD không quá khó so với các kỹ năng lập trình khác | **Effort Expectancy (EE)** | Kỳ vọng nỗ lực / Dễ học |
| `Q19_self_study` | Tôi có thể tự học CI/CD thông qua tài liệu và hướng dẫn có sẵn trên mạng | **Effort Expectancy (EE)** / **Self-efficacy** | Khả năng tự học |
| `Q20_setup_ability` | Tôi có thể tự thiết lập một pipeline CI/CD đơn giản sau khi đọc hướng dẫn | **Effort Expectancy (EE)** / **Self-efficacy** | Khả năng tự thiết lập |
| `Q21_peer_influence` | Bạn bè / đồng học trong nhóm dự án khuyến khích tôi sử dụng CI/CD | **Social Influence (SI)** | Áp lực từ bạn bè |
| `Q22_mentor_influence` | Giảng viên hoặc mentor trong quá trình thực tập đề cao việc áp dụng CI/CD | **Social Influence (SI)** | Khuyến khích từ thầy cô / mentor |
| `Q23_industry_standard` | CI/CD được coi là kỹ năng tiêu chuẩn mà một lập trình viên chuyên nghiệp cần có | **Social Influence (SI)** | Tiêu chuẩn ngành / Xã hội |
| `Q24_curriculum_readiness` | Chương trình đào tạo tại trường cung cấp đủ kiến thức nền để tôi tiếp cận CI/CD | **Facilitating Conditions (FC)** | Chương trình giảng dạy của trường |
| `Q25_free_tools_sufficient` | Các công cụ CI/CD miễn phí (GitHub Actions, GitLab CI...) đủ để tôi thực hành trong môi trường học tập | **Facilitating Conditions (FC)** | Tài nguyên công cụ miễn phí |
| `Q26_support_access` | Tôi dễ dàng tìm được sự hỗ trợ khi gặp khó khăn với CI/CD (giảng viên, cộng đồng online, tài liệu...) | **Facilitating Conditions (FC)** | Khả năng tiếp cận hỗ trợ |
| `Q27_intent_to_adopt` | Tôi có ý định áp dụng CI/CD vào các dự án học tập hoặc thực tập sắp tới | **Behavioral Intention (BI)** | Ý định hành vi tương lai |
| `Q28_self_learn_plan` | Tôi dự định tự học thêm về CI/CD ngoài chương trình đào tạo chính khoá | **Behavioral Intention (BI)** | Ý định tự học thêm |
| `Q29_prefer_cicd_projects` | Tôi sẽ ưu tiên tham gia các dự án hoặc nhóm có sử dụng CI/CD | **Behavioral Intention (BI)** | Ưu tiên chọn nhóm có CI/CD |
| `Q30_actual_usage` | Tôi đã thực tế cấu hình hoặc sử dụng CI/CD trong ít nhất một dự án | **Use Behavior (UB)** | Kinh nghiệm cấu hình thực tế |
| `Q31_regular_usage` | Tôi thường xuyên dùng CI/CD trong quá trình phát triển phần mềm của mình | **Use Behavior (UB)** | Tần suất sử dụng thực tế |
| `Q32_proactive_setup` | Tôi chủ động đề xuất hoặc thiết lập CI/CD cho nhóm mà không cần ai yêu cầu | **Use Behavior (UB)** | Tính chủ động trong dự án nhóm |

---

### Phần 5: Khó khăn, thách thức & Đề xuất mở rộng

| Mã câu hỏi | Nội dung câu hỏi gốc | Loại câu hỏi | Phương án trả lời / Ghi chú |
| :--- | :--- | :--- | :--- |
| `Q33_cicd_difficulties` | Trong quá trình học tập hoặc thực hiện các dự án lập trình (đồ án, project cá nhân, project nhóm), bạn cảm thấy khó khăn ở những giai đoạn nào của quy trình CI/CD? * | Checkbox (Nhiều lựa chọn) | Tích hợp liên tục (CI - Integration), Xây dựng (Build), Kiểm thử tự động (Automated Testing), Phân phối liên tục (CD - Delivery), Triển khai liên tục (CD - Deployment), Giám sát & Phản hồi, Mục khác |
| `Q34_adoption_barriers` | Theo bạn, những khó khăn hoặc thách thức nào khiến sinh viên khó áp dụng CI/CD trong quá trình học tập và làm dự án? * | Checkbox (Nhiều lựa chọn) | Thiếu kiến thức hoặc kỹ năng về DevOps/CI/CD, Thiếu tài liệu hoặc hướng dẫn thực hành rõ ràng, Việc thiết lập và cấu hình công cụ CI/CD khá phức tạp, Thiếu môi trường thực hành (server, cloud, Docker, v.v.), Ít cơ hội áp dụng CI/CD trong các môn học tại trường, Chưa hiểu rõ lợi ích thực tế khi triển khai CI/CD, Mục khác |
| `Q35_improvement_suggestions` | Theo bạn, điều gì cần được cải thiện để sinh viên dễ tiếp cận và học CI/CD hiệu quả hơn? | Free-text (Mở) | Ý kiến tự do của sinh viên |
| `Q36_university_suggestions` | Bạn có đề xuất nào để các trường đại học hoặc giảng viên hỗ trợ sinh viên học và áp dụng CI/CD tốt hơn trong các môn học hoặc dự án? | Free-text (Mở) | Ý kiến tự do của sinh viên |
| `Q37_skills_needed` | Theo bạn, sinh viên cần được trang bị thêm những kiến thức hoặc kỹ năng nào để áp dụng CI/CD hiệu quả trong các dự án phần mềm? | Free-text (Mở) | Ý kiến tự do của sinh viên |
| `Q38_future_plan` | Bạn có dự định tìm hiểu hoặc áp dụng CI/CD trong các dự án lập trình (đồ án, project cá nhân, project nhóm) trong thời gian tới không? * | Single-choice | Đã từng áp dụng CI/CD trong dự án, Có kế hoạch tìm hiểu và áp dụng trong thời gian tới, Đang trong quá trình tìm hiểu về CI/CD, Chưa có kế hoạch áp dụng CI/CD |
| `Q39_biggest_barrier` | Theo bạn, đâu là rào cản lớn nhất khiến sinh viên chưa áp dụng CI/CD trong các dự án lập trình? | Checkbox (Nhiều lựa chọn) | Thiếu kiến thức hoặc kỹ năng về CI/CD và DevOps, Khó thiết lập và cấu hình các công cụ CI/CD, Thiếu môi trường thực hành (server, cloud, Docker, v.v.), Ít cơ hội thực hành CI/CD trong các môn học tại trường, Dự án học tập còn đơn giản nên chưa thấy cần CI/CD, Khó phối hợp làm việc nhóm khi áp dụng CI/CD, Mục khác |
| `Q40_expected_benefit` | Nếu CI/CD được áp dụng trong các dự án học tập hoặc project cá nhân, bạn mong đợi lợi ích nào nhất? | Checkbox (Nhiều lựa chọn) | Giảm bớt các công việc thủ công lặp đi lặp lại (build, test, deploy), Phát hiện lỗi sớm hơn trong quá trình phát triển phần mềm., Tăng tốc độ phát triển và cập nhật dự án., Nâng cao kỹ năng DevOps và kinh nghiệm thực tế cho sinh viên., Mục khác |
