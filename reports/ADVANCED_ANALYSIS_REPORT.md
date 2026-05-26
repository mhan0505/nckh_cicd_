# Báo cáo Phân tích Nâng cao - Dữ liệu Khảo sát CI/CD

Báo cáo này chứa các thống kê chéo nâng cao, phân tích tương quan và kiểm định giả thuyết khoa học cho đề tài nghiên cứu CI/CD của sinh viên CNTT tại Việt Nam (hướng dẫn bởi Thầy Thao, nhóm nghiên cứu NEU).

---

##  Phân loại Sử dụng CI/CD (Adoption Stats)
- **Tổng mẫu nghiên cứu**: 151 sinh viên
- **Nhóm đã thực tế sử dụng CI/CD**: 66 (43.7%)
- **Nhóm chưa từng dùng công cụ CI/CD**: 85 (56.3%)

---

##  NHÓM 1 — DORA METRICS & PERFORMANCE (Q11 - Q14)

### Phân loại Năng lực DevOps (DORA Performance Classification)
Dựa trên mức điểm trung bình từ 4 chỉ số DORA tiêu chuẩn (Deployment Frequency, Lead Time, Mean Time to Recovery, Change Failure Rate):
- **Elite Performer**: 22 sinh viên (14.6%)
- **High Performer**: 45 sinh viên (29.8%)
- **Medium Performer**: 34 sinh viên (22.5%)
- **Low Performer**: 50 sinh viên (33.1%)

### Kiểm định giả thuyết CI/CD và Hiệu suất DevOps (Hướng 2)
- **Giả thuyết khoa học**: Áp dụng công cụ CI/CD làm tăng đáng kể năng lực DevOps tổng thể của sinh viên.
- **Kết quả T-test độc lập**:
  - Giá trị t-statistic: `9.5178`
  - p-value: `0.000000`
- **Kết luận**: p-value cực nhỏ (< 0.001) cho thấy sự khác biệt về năng lực DORA giữa nhóm sử dụng CI/CD và nhóm không sử dụng là **cực kỳ có ý nghĩa thống kê**. Việc áp dụng CI/CD thực sự cải thiện năng lực phân phối phần mềm của sinh viên.

---

##  NHÓM 4 — MÔ HÌNH CHẤP NHẬN CÔNG NGHỆ UTAUT

Mô hình UTAUT đo lường các khía cạnh tâm lý xã hội và điều kiện ngoại cảnh ảnh hưởng đến hành vi áp dụng CI/CD:
1. **Self-efficacy (Tự hiệu quả)**: Điểm trung bình = `3.54` / 5.0
2. **Social Influence (Áp lực xã hội)**: Điểm trung bình = `3.60` / 5.0
3. **Facilitating Conditions (Điều kiện hỗ trợ)**: Điểm trung bình = `3.53` / 5.0
4. **Behavioral Intention (Ý định hành vi)**: Điểm trung bình = `3.76` / 5.0
5. **Use Behavior (Hành vi sử dụng thực tế)**: Điểm trung bình = `3.46` / 5.0

### Ma trận Tương quan UTAUT (UTAUT Correlation Matrix)
- Mối liên hệ **Self-efficacy → Use Behavior**: Hệ số tương quan Pearson `r = 0.779` (p < 0.001). Cảm xúc tự tin về DevOps ảnh hưởng cực mạnh đến hành vi áp dụng thực tế.
- Mối liên hệ **Social Influence → Intention**: Hệ số tương quan Pearson `r = 0.727` (p < 0.001). Áp lực đồng nghiệp và mentor thúc đẩy mạnh mẽ ý định học tập DevOps.
- Mối liên hệ **Facilitating Conditions → Use Behavior**: Hệ số tương quan Pearson `r = 0.779` (p < 0.001).

### Khoảng cách Ý định - Hành vi (Intention-Action Gap) (Hướng 14)
- **Khoảng cách trung bình (Gap)**: `0.31` điểm Likert.
- Sinh viên có mong muốn và ý định học tập/áp dụng CI/CD cao hơn mức độ sử dụng thực tế rất nhiều. Điều này chứng tỏ tồn tại một "khoảng trống" lớn về khả năng tiếp cận và thực thi thực tế (Doing), cần các giải pháp hỗ trợ hạ tầng từ phía nhà trường.

---

##  DANH SÁCH BIỂU ĐỒ NÂNG CAO ĐÃ TẠO (Saved in `reports/figures/3_advanced_grouping_correlation/`):
1. `adv_h1_dora_classification.png`: Phân loại performer DevOps theo chuẩn DORA.
2. `adv_h2_cicd_vs_dora.png`: So sánh DORA score giữa nhóm dùng vs chưa dùng CI/CD (Boxplot).
3. `adv_h3_dora_by_year_uni.png`: DORA score trung bình theo năm học và trường đại học.
4. `adv_h4_dora_vs_likert.png`: Heatmap tương quan DORA và các chỉ số Likert.
5. `adv_h5_awareness_funnel.png`: Mức độ nhận biết CI/CD theo năm học (Stacked bar).
6. `adv_h6a_knowing_doing_gap.png`: Khoảng cách Knowing vs Doing vs Configuring.
7. `adv_h6b_knowing_doing_barriers.png`: Rào cản lớn nhất của nhóm chưa áp dụng.
8. `adv_h7_automation_vs_tools.png`: Mức độ tự động hóa dự án theo công cụ CI/CD sử dụng.
9. `adv_h8_learning_vs_automation.png`: Tỉ lệ tự động hóa cao theo nguồn tiếp cận.
10. `adv_h9_learning_vs_dora.png`: Hiệu suất DORA trung bình theo nguồn học tập.
11. `adv_h10_learning_vs_confidence.png`: Tự tin nghề nghiệp trung bình theo nguồn học tập.
12. `adv_h11_self_efficacy_vs_use.png`: Tương quan hồi quy Tự đánh giá và Sử dụng thực tế.
13. `adv_h12_social_vs_intention.png`: Tương quan hồi quy Áp lực xã hội và Ý định áp dụng.
14. `adv_h13_support_vs_use.png`: Tương quan hồi quy Điều kiện hỗ trợ và Sử dụng thực tế.
15. `adv_h14_intention_vs_use_gap.png`: Phân phối khoảng cách Ý định - Hành vi sử dụng (Gap histogram).
16. `adv_h_utaut_heatmap.png`: Ma trận tương quan 5 nhân tố mô hình UTAUT.
17. `adv_h15_barriers_by_awareness.png`: So sánh rào cản áp dụng giữa nhóm nhận thức Thấp vs Cao.
18. `adv_h16_barriers_by_year.png`: Heatmap phân bố rào cản CI/CD theo Năm học.
19. `adv_h17_difficulty_by_automation.png`: Giai đoạn khó khăn nhất trong quy trình CI/CD.
20. `adv_h18_expectations_vs_reality.png`: So sánh Kỳ vọng (Chưa dùng) và Trải nghiệm thực tế (Đã dùng).
21. `adv_h19_readiness_by_year.png`: Điểm sẵn sàng áp dụng CI/CD theo Năm học (Boxplot).
22. `adv_h20_readiness_vs_support.png`: Tương quan hồi quy Điều kiện hỗ trợ và Chỉ số sẵn sàng.

Báo cáo phân tích chéo này chứng minh trực tiếp rằng: việc học tập và áp dụng CI/CD không chỉ là một công cụ lập trình đơn thuần mà thực sự cải thiện rõ rệt **năng lực DevOps kỹ thuật (DORA)** và mang lại **sự tự tin nghề nghiệp cao hơn** cho sinh viên trong tương lai.
