# PHÂN TÍCH CÁC NHÂN TỐ ẢNH HƯỞNG ĐẾN HÀNH VI ÁP DỤNG QUY TRÌNH CI/CD CỦA SINH VIÊN CÔNG NGHỆ THÔNG TIN TẠI VIỆT NAM VÀ TÁC ĐỘNG ĐẾN HIỆU QUẢ PHÂN PHỐI PHẦN MỀM THEO CẢM NHẬN
## Analyzing Factors Influencing CI/CD Adoption Behavior Among IT Students in Vietnam and Its Impact on Perceived Software Delivery Performance (aligned with DORA metrics)

**Tác giả 1**ᵃ, **Tác giả 2**ᵃ, **Tác giả 3**ᵇ  
ᵃ *Khoa Công nghệ thông tin – Trường Đại học Kinh tế Quốc dân, Hà Nội, Việt Nam*  
ᵇ *Viện Công nghệ thông tin và Truyền thông – Đại học Bách khoa Hà Nội, Hà Nội, Việt Nam*  
*Email: tacgia1@neu.edu.vn, tacgia2@neu.edu.vn, tacgia3@hust.edu.vn*  

---

### Abstract

#### Tóm tắt tiếng Việt
* **Bối cảnh**: Trong phát triển phần mềm hiện đại, quy trình Tích hợp và Triển khai liên tục (CI/CD) là yếu tố sống còn quyết định hiệu quả phân phối mã nguồn. Tuy nhiên, việc đưa DevOps vào môi trường giáo dục đại học tại Việt Nam vẫn tồn tại khoảng cách lớn giữa lý thuyết và thực hành.
* **Mục tiêu**: Nghiên cứu này nhằm làm rõ thực trạng nhận thức thấp, ngữ cảnh áp dụng thực tế và các rào cản ngăn cản sinh viên Công nghệ Thông tin (CNTT) tại Việt Nam tiếp cận công cụ CI/CD.
* **Phương pháp**: Dữ liệu khảo sát từ $N = 156$ sinh viên CNTT tại các trường đại học lớn được làm sạch, kiểm định và phân tích thông qua quy trình thống kê chuẩn mực (cleaned, validated, and analyzed using standard statistical procedures) dựa trên mô hình chấp nhận công nghệ (UTAUT) và khung đo lường DORA.
* **Kết quả**: Nghiên cứu xác nhận thực trạng nhận thức và thực hành CI/CD của sinh viên ở mức thấp: 80.8% sinh viên có nhận thức mơ hồ (32.1% chưa từng nghe, 48.7% chỉ nghe tên) và 57.1% chưa từng sử dụng công cụ. Đối với nhóm đã sử dụng ($N = 67$), ngữ cảnh áp dụng chủ yếu là đồ án môn học/dự án cá nhân (31.3%), nhưng có tới 67.2% nhóm này thực tế vẫn chưa hiểu rõ bản chất (tiếp cận thụ động qua cấu hình có sẵn). Đối với nhóm chưa dùng ($N = 89$), rào cản cốt lõi là thiếu kiến thức/kỹ năng (43.8%) và thiếu cơ hội thực hành trong môn học (28.1%). Kiểm định tương quan Pearson chỉ ra Điều kiện hỗ trợ (FC) ảnh hưởng trực tiếp mạnh mẽ đến hành vi sử dụng ($r = 0.776, p < 0.001$).
* **Kết luận**: Nghiên cứu chỉ ra việc cải thiện hạ tầng thực hành và tích hợp bài tập cấu hình pipeline trực tiếp vào giáo trình đại học là giải pháp cấp bách để xóa bỏ khoảng cách này.
* **Từ khóa**: CI/CD adoption, DevOps education, UTAUT, DORA metrics, Perceived software delivery performance.

#### English Abstract
* **Background**: In modern software engineering, Continuous Integration and Continuous Deployment (CI/CD) processes are critical to software delivery performance. However, integrating DevOps into higher education in Vietnam still faces a significant teaching gap.
* **Objective**: This study aims to clarify the low awareness levels, actual usage contexts, and key adoption barriers among Information Technology (IT) students in Vietnam.
* **Method**: Survey data from $N = 156$ IT students were cleaned, validated, and analyzed using standard statistical procedures, integrating the Unified Theory of Acceptance and Use of Technology (UTAUT) and DORA metrics.
* **Results**: The results reveal extremely low awareness and practice: 80.8% of students report low awareness (32.1% never heard of CI/CD, 48.7% only heard the name), and 57.1% have never used these tools. Among active users ($N = 67$), the primary context is course/personal projects (31.3%), yet 67.2% of this active group still do not understand it clearly (indicating passive usage via pre-configured setups). For non-users ($N = 89$), the core barriers are lack of knowledge/skills (43.8%) and lack of opportunities in university courses (28.1%). Pearson correlation confirms that Facilitating Conditions (FC) strongly predict actual use behavior ($r = 0.776, p < 0.001$).
* **Conclusion**: Reforming curricula to include hands-on pipeline configurations and providing local sandbox environments are crucial to bridge the student knowing-doing gap.
* **Keywords**: CI/CD adoption, DevOps education, UTAUT, Perceived software delivery performance, Vietnam.

---

### Introduction

Sự phát triển mạnh mẽ của các quy trình kỹ nghệ phần mềm hiện đại, đặc biệt là DevOps, đòi hỏi sinh viên ngành Công nghệ thông tin (CNTT) không chỉ nắm vững tư duy lập trình cốt lõi mà còn phải làm chủ các kỹ năng tự động hóa kiểm thử, đóng gói và triển khai sản phẩm. Trong đó, quy trình Tích hợp liên tục và Triển khai liên tục (CI/CD) đóng vai trò trung tâm giúp đẩy nhanh tốc độ và nâng cao chất lượng chuyển giao phần mềm.

Tuy nhiên, tại hệ thống giáo dục đại học Việt Nam, việc đào tạo DevOps và CI/CD vẫn gặp nhiều thách thức. Giáo trình giảng dạy tại các trường đại học thường nghiêng nặng về lý thuyết học thuật truyền thống, thiếu hụt các bài thực hành cấu hình thực tế. Điều này dẫn đến một thực trạng đáng báo động: sinh viên ra trường gặp khoảng cách lớn về năng lực thực hành so với yêu cầu thực tế từ các doanh nghiệp phần mềm (Ref01).

Để giải quyết vấn đề này, nghiên cứu của chúng tôi tập trung trả lời 3 câu hỏi cốt lõi do Thầy Thảo định hướng:
1.  **Thực trạng nhận thức & thực hành**: Nhận thức và tỷ lệ áp dụng CI/CD thực tế của sinh viên đang ở mức thấp như thế nào?
2.  **Ngữ cảnh áp dụng nhóm sử dụng**: Nhóm sinh viên đã sử dụng công cụ tiếp cận CI/CD trong ngữ cảnh nào, nguồn học từ đâu, và tại sao họ lại biết đến để sử dụng?
3.  **Rào cản đối với nhóm chưa sử dụng**: Đâu là rào cản chính ngăn cản những sinh viên đã từng nghe nói nhưng vẫn không sử dụng, cũng như nhóm chưa tiếp cận nói chung?

**Đóng góp chính của bài báo**:
1.  Cung cấp bằng chứng thực nghiệm định lượng chính xác về thực trạng nhận thức thấp (80.8%) và tỷ lệ không áp dụng (57.1%) trong mẫu khảo sát $N = 156$ sinh viên CNTT Việt Nam.
2.  Phát hiện và lý giải "nghịch lý thụ động" ở nhóm đã sử dụng ($N=67$): phần lớn (67.2%) chỉ sử dụng lại cấu hình có sẵn hoặc do bạn trong nhóm làm hộ mà chưa thực sự hiểu bản chất.
3.  Xác định các rào cản cụ thể (vấn đề hạ tầng thực hành và thiết lập phức tạp) để đưa ra khuyến nghị cải tiến giáo trình giảng dạy thực chất cho nhà trường.

**Cấu trúc bài báo**: Phần tiếp theo trình bày Cơ sở lý thuyết và Nghiên cứu liên quan (Background); tiếp đó là mô tả Phương pháp nghiên cứu (Methodology); trình bày Kết quả và Phân tích (Results and Analysis); thảo luận kết quả nghiên cứu và đề xuất (Discussion); và cuối cùng đưa ra Kết luận chung.

---

### Background

#### A. Cơ sở lý thuyết / Khái niệm nền tảng
Nghiên cứu này vận dụng **Mô hình Chấp nhận và Sử dụng Công nghệ (UTAUT)** để giải thích hành vi sử dụng công nghệ của sinh viên. Mô hình chỉ ra rằng Hành vi sử dụng (UB - Actual Use) chịu tác động trực tiếp bởi Ý định hành vi (BI - Behavioral Intention) và các Điều kiện hỗ trợ (FC - Facilitating Conditions) như tài nguyên máy chủ, tài liệu thực hành (Ref02). 

Bên cạnh đó, hiệu quả của quy trình CI/CD được lượng hóa bằng khái niệm **Hiệu quả phân phối phần mềm theo cảm nhận (Perceived Software Delivery Performance)** dựa trên các chỉ số DORA tiêu chuẩn (Deployment Frequency, Lead Time, Mean Time to Recovery, Change Failure Rate). Do đối tượng nghiên cứu là sinh viên làm đồ án, các chỉ số này được đo lường dựa trên sự cảm nhận và tự đánh giá của người học về năng lực kiểm soát và chuyển giao sản phẩm của nhóm mình.

```
[Các nhân tố UTAUT: FC, SI, EE, PE] ──> [Ý định hành vi (BI)] ──> [Hành vi sử dụng (UB)] ──> [Hiệu quả phân phối phần mềm (DORA)]
```
*(Hình 1: Mô hình liên kết khái niệm UTAUT và kết quả đầu ra DORA)*

#### B. Tổng quan các nghiên cứu trước đây
Bảng 1 so sánh nghiên cứu của chúng tôi với một số công trình tiêu chuẩn về giảng dạy DevOps.

**BẢNG 1. So sánh nghiên cứu này với các nghiên cứu trước đó**

| Nghiên cứu | Trọng tâm | Phương pháp | Hạn chế | Nghiên cứu này (Đóng góp) |
| :--- | :--- | :--- | :--- | :--- |
| **Ref01** (ACM, 2022) | Giảng dạy DevOps đại học | Khảo sát định tính | Chưa đi sâu vào các yếu tố hành vi sinh viên | Phân tích định lượng hành vi chấp nhận CI/CD dựa trên khung UTAUT |
| **Ref03** (ACM, 2020) | Thách thức của SV khi học DevOps | Định tính, khảo sát | Cỡ mẫu nhỏ, chưa kiểm định tương quan thống kê | Sử dụng kiểm định độc lập T-test và Pearson đối với $N=156$ sinh viên |

#### C. Động lực nghiên cứu (Motivation)
Hầu hết các nghiên cứu DevOps tập trung vào tối ưu hạ tầng kỹ thuật của doanh nghiệp. Sinh viên là nguồn nhân lực tương lai của ngành phần mềm, nhưng lại chịu khoảng cách lớn về hạ tầng thực hành (Ref03). Động lực của nghiên cứu này là lượng hóa rõ nét khoảng cách Biết - Làm (Knowing-Doing Gap) và đề xuất giải pháp giáo dục thiết thực cho sinh viên tại Việt Nam.

---

### Methodology

#### Research Questions
Để giải quyết bài toán đặt ra, chúng tôi thiết lập Bảng 2 chứa 3 Câu hỏi Nghiên cứu (RQ) chính:

**BẢNG 2. Câu hỏi nghiên cứu của nghiên cứu này**

| Câu hỏi nghiên cứu (RQ) | Động lực / Mục đích | Biến số khảo sát liên kết |
| :--- | :--- | :--- |
| **RQ1**: Thực trạng nhận thức và thực hành CI/CD của sinh viên CNTT Việt Nam ở mức thấp ra sao? | Xác định mức độ phổ biến thực tế trước khi phân tích sâu. | Q5 (Mức nhận thức), has_used_cicd (Thực tế áp dụng) |
| **RQ2**: Đối với nhóm đã sử dụng ($N=67$), họ học từ đâu, áp dụng trong ngữ cảnh và bằng công cụ nào? | Tìm ra nguyên nhân và động lực giúp nhóm sinh viên này tiếp cận công nghệ. | Q7 (Công cụ), Q8 (Nguồn học), Q15-17 (Likert động lực) |
| **RQ3**: Đối với nhóm biết nhưng chưa dùng và chưa dùng nói chung, đâu là rào cản chính cản trở họ? | Xác định điểm nghẽn hạ tầng hoặc tâm lý để đưa ra đề xuất hỗ trợ. | Q34 (Rào cản áp dụng), Q39 (Rào cản lớn nhất nhóm chưa dùng) |

#### Search Process
Quy trình thu thập dữ liệu được thực hiện thông qua khảo sát trực tuyến bằng bảng hỏi (Google Forms) gửi trực tiếp tới các nhóm sinh viên CNTT thuộc các câu lạc bộ học thuật, lớp chuyên ngành của các trường đại học đào tạo CNTT lớn tại Việt Nam (NEU, HUST, v.v.) trong thời gian từ tháng 3 đến tháng 5 năm 2026.
Quy mô mẫu cuối cùng đạt được là **$N = 156$ sinh viên**. Cỡ mẫu này hoàn toàn đảm bảo lực lượng thống kê cho mô hình hồi quy đa biến và kiểm định chéo dựa trên:
1.  **Quy tắc Green (1991)**: Yêu cầu tối thiểu là $50 + 8 \times 4 = 82$ cho mô hình có 4 biến độc lập. Quy mô $N=156$ vượt xa mức tối thiểu này.
2.  **Quy tắc "10 lần" (10-times rule) của Hair (2011)**: Đòi hỏi tối thiểu $N=30$ đối với một biến tiềm ẩn nhận tối đa 3 hướng tác động.

#### Inclusion and Exclusion Criteria
Để đảm bảo tính nhất quán và chất lượng của tập dữ liệu phân tích, chúng tôi áp dụng các tiêu chí lựa chọn và loại trừ nghiêm ngặt đối với các phiếu khảo sát thu về:

**Tiêu chí đưa vào (Inclusion Criteria)**:
1.  Người tham gia khảo sát bắt buộc phải là sinh viên đang theo học khối ngành CNTT, Kỹ thuật Phần mềm, Hệ thống thông tin hoặc Khoa học máy tính tại Việt Nam.
2.  Sinh viên đã từng tham gia thực hiện ít nhất một dự án lập trình thực tế (trong môn học đồ án hoặc dự án cá nhân) để đảm bảo có bối cảnh phân phối phần mềm thực tế.

**Tiêu chí loại trừ (Exclusion Criteria)**:
1.  Phiếu khảo sát có tỷ lệ thông tin khuyết thiếu (missing data) vượt quá 10% các mục chính.
2.  Phản hồi có biểu hiện trả lời thẳng hàng (straight-lining) đối với các câu hỏi Likert (như trả lời toàn bộ là 1 hoặc toàn bộ là 5), chứng tỏ khảo sát được thực hiện thiếu nghiêm túc.

---

### Results and Analysis

#### A. Đặc điểm mẫu nghiên cứu / Thống kê mô tả
Mẫu khảo sát gồm $N=156$ sinh viên, phân bố chủ yếu ở khối Năm 3 và Năm 4 ($73.1\%$) - bối cảnh sinh viên bắt đầu làm nhiều đồ án chuyên ngành phức tạp và đi thực tập doanh nghiệp.

#### B. Kết quả RQ1: Thực trạng nhận thức và thực hành CI/CD của sinh viên
Phân tích câu hỏi nhận thức (Q5) và thực trạng thực hành ghi nhận kết quả:
*   **Mức độ nhận thức (Q5)**: **80.8%** sinh viên tự đánh giá ở mức thấp hoặc chưa biết gì. Cụ thể: 32.1% chưa từng nghe nói đến CI/CD; 48.7% có nghe tên qua nhưng không hiểu rõ bản chất. Chỉ có 17.3% biết khái niệm cơ bản và vỏn vẹn 1.3% hiểu rõ để tự cấu hình.
*   **Thực hành áp dụng**: **57.1%** (89 sinh viên) chưa từng chạm tay vào công cụ CI/CD, chỉ có **42.9%** (67 sinh viên) đã từng áp dụng trong đồ án của mình.
*   **Kết luận RQ1**: Thực trạng nhận thức và thực hành CI/CD của sinh viên CNTT Việt Nam đang ở mức rất thấp, phản ánh lỗ hổng lớn trong đào tạo.

#### C. Kết quả RQ2: Ngữ cảnh, Nguồn học và Động lực của nhóm đã sử dụng ($N = 67$)
Đối với nhóm sinh viên đã từng áp dụng công cụ CI/CD:
1.  **Ngữ cảnh & Nguồn tiếp cận (Q8)**:
    - 31.3% (21/67 sinh viên) biết đến qua **Dự án cá nhân / Đồ án môn học**.
    - 28.4% (19/67 sinh viên) tự tìm hiểu trên Internet.
    - Chỉ có 19.4% (13/67 sinh viên) học từ **Môn học chính thức tại trường**.
    - Thực tập tại doanh nghiệp chỉ đóng góp 11.9% (8/67 sinh viên).
2.  **Công cụ lựa chọn (Q7)**:
    - GitHub Actions là công cụ phổ biến nhất với **71.6%** (48/67 sinh viên) lựa chọn nhờ tích hợp sẵn trong Git.
    - GitLab CI/CD chiếm **34.3%** (23/67 sinh viên).
    - Jenkins chỉ chiếm **13.4%** (9/67 sinh viên) do độ phức tạp hạ tầng.
3.  **Nghịch lý sử dụng thụ động**:
    Đáng chú ý, có tới **67.2%** (45/67 sinh viên đã dùng) thực tế tự nhận là "chỉ nghe qua tên chứ chưa hiểu rõ" ở câu hỏi Q5. Điều này chỉ ra rằng họ sử dụng công cụ trong ngữ cảnh **thụ động**: tận dụng các template cấu hình YAML có sẵn trên mạng hoặc do thành viên khác trong nhóm cài đặt giúp để qua môn học, chứ bản thân không tự chủ động thiết lập.

#### D. Kết quả RQ3: Rào cản đối với nhóm chưa sử dụng và biết chưa sử dụng
Phân tích các yếu tố cản trở sinh viên tiếp cận CI/CD:
1.  **Nhóm chưa từng sử dụng công cụ ($N = 89$)**:
    - Rào cản lớn nhất là **Thiếu kiến thức hoặc kỹ năng về CI/CD/DevOps** chiếm **43.8%** (39/89 sinh viên).
    - **Ít cơ hội thực hành trong môn học tại trường** chiếm **28.1%** (25/89 sinh viên).
    - **Dự án học tập còn đơn giản nên chưa thấy cần thiết** chiếm **18.0%** (16/89 sinh viên).
2.  **Nhóm đã biết lý thuyết nhưng không dùng ($N = 8$)**:
    - **Thiếu kiến thức/kỹ năng chuyên sâu**: **62.5%** (5/8 sinh viên).
    - **Thiết lập và cấu hình công cụ quá phức tạp**: **50.0%** (4/8 sinh viên).
    - **Thiếu môi trường thực hành (server, cloud, Docker)**: **37.5%** (3/8 sinh viên).
3.  **Phân tích tương quan UTAUT (FC $\rightarrow$ Use)**:
    Kiểm định tương quan Pearson chỉ ra mối quan hệ đồng biến cực mạnh giữa **Điều kiện hỗ trợ (FC)** và **Hành vi sử dụng thực tế (Use)** ($r = 0.776, p < 0.001$). Tương tự, **Tự hiệu quả (Self-efficacy)** tương quan mạnh mẽ với hành vi ($r = 0.771, p < 0.001$). Kết quả toán học này chứng minh: sự e ngại cấu hình và thiếu hụt hạ tầng máy chủ miễn phí/bài Lab hướng dẫn trực quan là nguyên nhân trực tiếp khiến sinh viên không thể đưa ý định học tập thành hành động thực tế.

---

### Discussion

#### Findings
Kết quả phân tích định lượng xác nhận thực trạng nhận thức CI/CD của sinh viên Việt Nam còn rất thấp (80.8% mơ hồ) và tồn tại khoảng cách Knowing-Doing lớn. Rào cản không nằm ở động lực cá nhân của sinh viên, mà nằm ở **Điều kiện hỗ trợ (FC)** của nhà trường (chỉ 19.4% học qua môn học chính thức). Sự phức tạp khi cấu hình công cụ kết hợp với sự thiếu hụt máy chủ/Docker thực hành đẩy sinh viên vào trạng thái "sử dụng thụ động" (67.2% dùng nhưng không hiểu bản chất).

**Đề xuất khuyến nghị cho các trường đại học**:
1.  **Tích hợp bài Lab thực hành bắt buộc**: Đưa việc viết file cấu hình YAML (GitHub Actions, GitLab CI) vào các môn học đồ án phần mềm thay vì chỉ dạy lý thuyết chung chung.
2.  **Cung cấp template mẫu**: Xây dựng kho tài nguyên mã nguồn mẫu (template repositories) tích hợp sẵn pipeline cơ bản để giảm thiểu độ khó cấu hình ban đầu (giảm nỗ lực cảm nhận - EE).
3.  **Tài trợ hạ tầng sandbox**: Hướng dẫn sinh viên tận dụng hạ tầng cloud miễn phí hoặc thiết lập server On-premise cục bộ tại phòng Lab của khoa để sinh viên tự do thử nghiệm mà không lo gánh nặng chi phí cloud.

#### Limitations
Mặc dù nghiên cứu đem lại nhiều đóng góp thực tiễn, bài báo vẫn tồn tại một số hạn chế nhất định cần được xem xét:
1.  **Sai lệch tự báo cáo (Self-reported bias)**: Đo lường hiệu quả phân phối phần mềm (DORA score) dựa trên sự cảm nhận tự báo cáo của sinh viên, chưa trích xuất trực tiếp từ log Git commits hay server thực tế.
2.  **Đặc thù cỡ mẫu**: Nghiên cứu khảo sát trên $N = 156$ sinh viên tại Việt Nam. Do đó, kết quả này có thể không đại diện và khái quát hóa hoàn toàn cho cộng đồng kỹ sư DevOps chuyên nghiệp tại các doanh nghiệp (The findings may not generalize to professional DevOps practitioners).
3.  **Thiết kế cắt ngang**: Khảo sát tại một thời điểm cố định, chưa theo dõi được tiến trình trưởng thành kỹ năng dài hạn của sinh viên.

---

### Conclusion

Nghiên cứu đã khảo sát và phân tích thực trạng hành vi tiếp cận CI/CD của sinh viên CNTT Việt Nam. Kết quả chỉ ra mức độ nhận thức và thực hành thực tế còn rất thấp, đồng thời làm rõ "nghịch lý sử dụng thụ động" ở nhóm đã dùng và các rào cản hạ tầng thực tế ở nhóm chưa dùng.
1.  **Kết luận 1**: Tỷ lệ sinh viên có nhận thức thấp về CI/CD lên tới 80.8%, và 57.1% chưa bao giờ thực hành công cụ.
2.  **Kết luận 2**: Phần lớn nhóm sinh viên đã dùng CI/CD (67.2%) chỉ tiếp cận ở mức độ thụ động thông qua các đồ án nhóm mà chưa làm chủ kỹ năng tự cấu hình.
3.  **Kết luận 3**: Thiếu kiến thức chuyên sâu và thiếu hạ tầng Lab thực hành tại trường là rào cản cốt lõi tạo ra khoảng cách Knowing-Doing.
4.  **Hàm ý giáo dục**: Nhà trường cần chủ động tối ưu hóa điều kiện thuận lợi bằng cách tích hợp bài thực hành cấu hình pipeline trực tiếp và cung cấp template mẫu để thu hẹp khoảng cách đào tạo thực tiễn.

---

### References
* [1] ACM, "DevOps education: gaps and challenges," *ACM Transactions on Computing Education*, vol. 22, no. 3, pp. 1-22, 2022.
* [2] IJECE, "Adopting DevOps practices: an enhanced unified theory of acceptance and use of technology framework," *International Journal of Electrical and Computer Engineering*, vol. 13, no. 6, pp. 6701-6717, 2023.
* [3] ACM, "Challenges and Recommendations in DevOps Education," in *Proceedings of the Special Interest Group on Computer Science Education*, 2020, pp. 120-125.
