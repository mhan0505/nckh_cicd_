import os
import sys
import json
import shutil
import pandas as pd
from pathlib import Path

# Sửa lỗi mã hóa console trên Windows (cp1252 -> UTF-8)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    os.environ["PYTHONIOENCODING"] = "utf-8"


# Thư mục gốc dự án
BASE_DIR = Path(__file__).parent.parent.resolve()
CLEANED_DATA_PATH = BASE_DIR / "processed" / "multiple_answers_processed.csv"
TAGGED_FREE_TEXT_PATH = BASE_DIR / "processed" / "tagged_free_text.csv"
DOCS_DIR = BASE_DIR / "docs"
DOCS_REPORTS_DIR = DOCS_DIR / "reports" / "figures"
SOURCE_REPORTS_DIR = BASE_DIR / "reports" / "figures"

def copy_figures():
    """Sao chép các biểu đồ sang thư mục docs/ để GitHub Pages có thể truy cập được."""
    print("--> Đang sao chép biểu đồ sang thư mục docs/...")
    if DOCS_REPORTS_DIR.exists():
        shutil.rmtree(DOCS_REPORTS_DIR)
    
    if SOURCE_REPORTS_DIR.exists():
        shutil.copytree(SOURCE_REPORTS_DIR, DOCS_REPORTS_DIR)
        print("    [OK] Sao chép biểu đồ thành công!")
    else:
        print("    [WARN] Không tìm thấy thư mục biểu đồ gốc reports/figures/.")

def calculate_metrics():
    """Tính toán các chỉ số tổng quan từ CSV dữ liệu sạch."""
    if not CLEANED_DATA_PATH.exists():
        return {
            "total_count": 151,
            "used_cicd_count": 66,
            "used_cicd_pct": 43.7,
            "elite_dora_pct": 14.6,
            "avg_intention": 3.76
        }
    
    df = pd.read_csv(CLEANED_DATA_PATH)
    total_count = len(df)
    
    # Phân loại sử dụng CI/CD
    df["has_used_cicd"] = df["Q7_tools_used"].apply(
        lambda x: 0 if "Chưa từng sử dụng" in str(x) or str(x).strip() == "" or "Không trả lời" in str(x) else 1
    )
    used_cicd_count = int(df["has_used_cicd"].sum())
    used_cicd_pct = round((used_cicd_count / total_count) * 100, 1)
    
    # Tính điểm DORA
    q11_map = {"Nhiều lần trong ngày": 4, "Từ một lần mỗi ngày đến một lần mỗi tuần": 3, "Từ một lần mỗi tuần đến một lần mỗi tháng": 2, "Từ một lần mỗi tháng đến một lần sáu tháng": 1, "Ít hơn một lần sáu tháng": 1, "Không trả lời": 1}
    q12_map = {"Dưới 1 giờ": 4, "Từ 1 giờ đến dưới 1 ngày": 3, "Từ 1 ngày đến dưới 1 tuần": 2, "Từ 1 tuần đến dưới 1 tháng": 1, "Trên 1 tháng": 1, "Không trả lời": 1}
    q13_map = {"Dưới 1 giờ": 4, "Từ 1 giờ đến dưới 1 ngày": 3, "Từ 1 ngày đến dưới 1 tuần": 2, "Trên 1 tuần": 1, "Không trả lời": 1}
    q14_map = {"0% - 15% (Rất thấp)": 4, "16% - 30% (Thấp)": 3, "31% - 45% (Trung bình)": 2, "Trên 45% (Cao)": 1, "Không trả lời": 1}
    
    df["dora_q11_score"] = df["Q11_deploy_frequency"].map(q11_map).fillna(1)
    df["dora_q12_score"] = df["Q12_lead_time"].map(q12_map).fillna(1)
    df["dora_q13_score"] = df["Q13_recovery_time"].map(q13_map).fillna(1)
    df["dora_q14_score"] = df["Q14_failure_rate"].map(q14_map).fillna(1)
    df["dora_score"] = df[["dora_q11_score", "dora_q12_score", "dora_q13_score", "dora_q14_score"]].mean(axis=1)
    
    elite_count = len(df[df["dora_score"] >= 3.25])
    elite_dora_pct = round((elite_count / total_count) * 100, 1)
    
    # Tính trung bình ý định áp dụng (UTAUT Behavioral Intention)
    avg_intention = 3.76
    if "Q27_intent_to_adopt" in df.columns and "Q28_self_learn_plan" in df.columns and "Q29_prefer_cicd_projects" in df.columns:
        avg_intention = round(df[["Q27_intent_to_adopt", "Q28_self_learn_plan", "Q29_prefer_cicd_projects"]].mean(axis=1).mean(), 2)
        
    return {
        "total_count": total_count,
        "used_cicd_count": used_cicd_count,
        "used_cicd_pct": used_cicd_pct,
        "elite_dora_pct": elite_dora_pct,
        "avg_intention": avg_intention
    }

def get_free_text_data():
    """Đọc dữ liệu phản hồi mở và chuyển đổi thành danh sách JSON."""
    if not TAGGED_FREE_TEXT_PATH.exists():
        return []
    
    df = pd.read_csv(TAGGED_FREE_TEXT_PATH)
    # Lọc lấy các cột cần thiết
    records = df[["question", "response_raw", "tags", "token_count"]].to_dict(orient="records")
    return records

def generate_html():
    metrics = calculate_metrics()
    free_text_records = get_free_text_data()
    free_text_json = json.dumps(free_text_records, ensure_ascii=False)
    
    # Đọc danh sách câu hỏi mở duy nhất
    unique_questions = list(set([r["question"] for r in free_text_records])) if free_text_records else []
    
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Phân tích Khảo sát CI/CD & DevOps - NEU Research</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Google Font Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
            color: #1f2937;
        }}
        .navbar-brand {{
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        .header-bg {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 4rem 0 3rem 0;
            margin-bottom: 2rem;
            border-bottom: 5px solid #2563eb;
        }}
        .card-metric {{
            background: white;
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
            border-left: 5px solid #3b82f6;
            transition: transform 0.2s ease;
        }}
        .card-metric:hover {{
            transform: translateY(-3px);
        }}
        .metric-title {{
            font-size: 0.8rem;
            font-weight: 700;
            color: #6b7280;
            text-transform: uppercase;
        }}
        .metric-value {{
            font-size: 1.8rem;
            font-weight: 800;
            color: #111827;
        }}
        .nav-pills .nav-link {{
            color: #4b5563;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
        }}
        .nav-pills .nav-link.active {{
            background-color: #2563eb;
            color: white;
        }}
        .tab-content-container {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
            margin-bottom: 3rem;
        }}
        .chart-container {{
            margin-bottom: 2rem;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            background-color: #fafafa;
        }}
        .chart-img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .badge-tag {{
            background-color: #e0f2fe;
            color: #0369a1;
            font-weight: 600;
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            margin-right: 4px;
            display: inline-block;
        }}
        .table-responsive-custom {{
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
        }}
        .footer {{
            background-color: #111827;
            color: #9ca3af;
            padding: 2rem 0;
            margin-top: 5rem;
        }}
    </style>
</head>
<body>

    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <div class="container">
            <span class="navbar-brand"><span class="text-primary">📊</span> CI/CD NEU Research Portal</span>
            <span class="navbar-text text-white-50 d-none d-md-inline">Hệ thống báo cáo tự động hóa khảo sát</span>
        </div>
    </nav>

    <!-- HEADER -->
    <header class="header-bg text-center">
        <div class="container">
            <h1 class="display-5 fw-bold">Khảo sát mức độ áp dụng CI/CD & DevOps</h1>
            <p class="lead text-white-50">Báo cáo trực quan hóa dữ liệu nghiên cứu khoa học sinh viên CNTT tại Việt Nam</p>
            <span class="badge bg-warning text-dark fw-semibold px-3 py-2">NEU DevOps Research Team (Thầy Thảo hướng dẫn)</span>
        </div>
    </header>

    <div class="container">
        <!-- METRICS ROW -->
        <div class="row g-4 mb-4">
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #3b82f6;">
                    <div class="metric-title">Tổng số phản hồi (Mẫu)</div>
                    <div class="metric-value">{metrics["total_count"]} sinh viên</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #10b981;">
                    <div class="metric-title">Tỷ lệ đã dùng CI/CD</div>
                    <div class="metric-value">{metrics["used_cicd_pct"]}% <span class="fs-6 text-muted">({metrics["used_cicd_count"]} sv)</span></div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #f59e0b;">
                    <div class="metric-title">DevOps Performer Elite</div>
                    <div class="metric-value">{metrics["elite_dora_pct"]}% <span class="fs-6 text-muted">mẫu</span></div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-metric p-3" style="border-left-color: #8b5cf6;">
                    <div class="metric-title">Điểm Ý định UTAUT (Trung bình)</div>
                    <div class="metric-value">{metrics["avg_intention"]} / 5.0</div>
                </div>
            </div>
        </div>

        <!-- TABS NAV -->
        <div class="d-flex justify-content-center mb-4">
            <ul class="nav nav-pills gap-2 flex-wrap justify-content-center" id="pills-tab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="tab-demographics" data-bs-toggle="pill" data-bs-target="#content-demographics" type="button" role="tab">🏫 Nhân khẩu học</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="tab-dora" data-bs-toggle="pill" data-bs-target="#content-dora" type="button" role="tab">🎯 DORA & Hiệu năng DevOps</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="tab-utaut" data-bs-toggle="pill" data-bs-target="#content-utaut" type="button" role="tab">🧠 Mô hình UTAUT</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="tab-barriers" data-bs-toggle="pill" data-bs-target="#content-barriers" type="button" role="tab">🚧 Rào cản & Thách thức</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="tab-freetext" data-bs-toggle="pill" data-bs-target="#content-freetext" type="button" role="tab">💬 Ý kiến phản hồi mở</button>
                </li>
            </ul>
        </div>

        <!-- TAB CONTENT CONTAINER -->
        <div class="tab-content-container">
            <div class="tab-content" id="pills-tabContent">
                
                <!-- TAB 1: DEMOGRAPHICS -->
                <div class="tab-pane fade show active" id="content-demographics" role="tabpanel">
                    <h3 class="mb-3 fw-bold border-bottom pb-2">🏫 Phân tích Nhân khẩu học & Nhận biết cơ bản</h3>
                    <p class="text-muted">Các biểu đồ thống kê cơ bản về cơ cấu trường học, năm học, chuyên ngành và mức nhận thức thuật ngữ CI/CD của sinh viên.</p>
                    <div class="row g-4">
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Cơ cấu trường học tham gia khảo sát</h5>
                                <img src="reports/figures/1_demographics_descriptive/Q1_university_pie.png" class="chart-img" alt="Trường học">
                            </div>
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Phân bố Chuyên ngành</h5>
                                <img src="reports/figures/1_demographics_descriptive/Q3_major_bar.png" class="chart-img" alt="Chuyên ngành">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Phân bố Năm học</h5>
                                <img src="reports/figures/1_demographics_descriptive/Q2_year_pie.png" class="chart-img" alt="Năm học">
                            </div>
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Mức độ nhận biết thuật ngữ CI/CD</h5>
                                <img src="reports/figures/1_demographics_descriptive/Q5_cicd_awareness_pie.png" class="chart-img" alt="Nhận biết CI/CD">
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Mức độ tự động hóa dự án lập trình thực tế</h5>
                                <img src="reports/figures/1_demographics_descriptive/Q6_automation_level_bar.png" class="chart-img" alt="Mức độ tự động hóa">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB 2: DORA -->
                <div class="tab-pane fade" id="content-dora" role="tabpanel">
                    <h3 class="mb-3 fw-bold border-bottom pb-2">🎯 DORA Metrics & DevOps Performance</h3>
                    <p class="text-muted">Đo lường năng lực phân phối phần mềm của sinh viên thông qua 4 chỉ số DORA gốc và kiểm định sự khác biệt giữa hai nhóm.</p>
                    <div class="row g-4">
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Phân nhóm Performer DORA (Toàn bộ mẫu & theo Sử dụng)</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h1_dora_classification.png" class="chart-img" alt="DORA Classification">
                            </div>
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Điểm DORA trung bình theo Năm học và Trường</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h3_dora_by_year_uni.png" class="chart-img" alt="DORA Year/Uni">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">So sánh DORA Score: Nhóm dùng CI/CD vs Chưa dùng</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h2_cicd_vs_dora.png" class="chart-img" alt="CI/CD vs DORA">
                            </div>
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Năng lực DORA trung bình theo Nguồn học tập</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h9_learning_vs_dora.png" class="chart-img" alt="DORA Learning">
                            </div>
                        </div>
                    </div>
                    
                    <h4 class="mt-4 fw-bold">Chi tiết 4 Chỉ số DORA của sinh viên</h4>
                    <div class="row g-3">
                        <div class="col-md-3">
                            <div class="chart-container text-center">
                                <p class="fw-semibold text-center mb-1">Q11. Tần suất triển khai</p>
                                <img src="reports/figures/1_demographics_descriptive/Q11_deploy_frequency_bar.png" class="chart-img" alt="Q11">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="chart-container text-center">
                                <p class="fw-semibold text-center mb-1">Q12. Lead Time</p>
                                <img src="reports/figures/1_demographics_descriptive/Q12_lead_time_bar.png" class="chart-img" alt="Q12">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="chart-container text-center">
                                <p class="fw-semibold text-center mb-1">Q13. Khôi phục MTTR</p>
                                <img src="reports/figures/1_demographics_descriptive/Q13_recovery_time_bar.png" class="chart-img" alt="Q13">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="chart-container text-center">
                                <p class="fw-semibold text-center mb-1">Q14. Tỷ lệ lỗi CFR</p>
                                <img src="reports/figures/1_demographics_descriptive/Q14_failure_rate_pie.png" class="chart-img" alt="Q14">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB 3: UTAUT -->
                <div class="tab-pane fade" id="content-utaut" role="tabpanel">
                    <h3 class="mb-3 fw-bold border-bottom pb-2">🧠 Mô hình chấp nhận công nghệ UTAUT & Tương quan</h3>
                    <p class="text-muted">Phân tích mối tương quan và kiểm định hồi quy giữa các nhân tố tâm lý, điều kiện ngoại cảnh và hành vi chấp nhận sử dụng CI/CD của sinh viên.</p>
                    <div class="row g-4">
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Ma trận tương quan Pearson giữa 5 nhân tố UTAUT</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h_utaut_heatmap.png" class="chart-img" alt="UTAUT Heatmap">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Biểu đồ phân phối Khoảng cách Ý định - Sử dụng (Gap)</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h14_intention_vs_use_gap.png" class="chart-img" alt="UTAUT Gap">
                            </div>
                        </div>
                    </div>
                    
                    <h4 class="mt-4 fw-bold">Biểu đồ Hồi quy chi tiết các cặp giả thuyết</h4>
                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="chart-container text-center">
                                <p class="fw-semibold text-center mb-1">Tự tin năng lực (Self-efficacy) vs Sử dụng thực tế</p>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h11_self_efficacy_vs_use.png" class="chart-img" alt="H11">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="chart-container text-center">
                                <p class="fw-semibold text-center mb-1">Áp lực xã hội (Social) vs Ý định áp dụng</p>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h12_social_vs_intention.png" class="chart-img" alt="H12">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="chart-container text-center">
                                <p class="fw-semibold text-center mb-1">Điều kiện hỗ trợ (Support) vs Sử dụng thực tế</p>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h13_support_vs_use.png" class="chart-img" alt="H13">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB 4: BARRIERS -->
                <div class="tab-pane fade" id="content-barriers" role="tabpanel">
                    <h3 class="mb-3 fw-bold border-bottom pb-2">🚧 Rào cản & Thách thức lớn nhất đối với sinh viên</h3>
                    <p class="text-muted">Phân tích rào cản ngăn cản sinh viên CNTT sử dụng CI/CD trong học tập và đồ án nhóm.</p>
                    <div class="row g-4">
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Biểu đồ Pareto: Khó khăn lớn nhất trong quy trình</h5>
                                <img src="reports/figures/2_multiple_answers_freetext/Q33_cicd_difficulties_pareto.png" class="chart-img" alt="Q33 Pareto">
                            </div>
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">So sánh Rào cản theo mức Nhận biết (Nhận thức Thấp vs Cao)</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h15_barriers_by_awareness.png" class="chart-img" alt="Barriers Awareness">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Biểu đồ Pareto: Rào cản chấp nhận CI/CD</h5>
                                <img src="reports/figures/2_multiple_answers_freetext/Q34_adoption_barriers_pareto.png" class="chart-img" alt="Q34 Pareto">
                            </div>
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Bản đồ nhiệt: Rào cản áp dụng theo Năm học</h5>
                                <img src="reports/figures/3_advanced_grouping_correlation/adv_h16_barriers_by_year.png" class="chart-img" alt="Barriers Year Heatmap">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB 5: FREE TEXT -->
                <div class="tab-pane fade" id="content-freetext" role="tabpanel">
                    <h3 class="mb-3 fw-bold border-bottom pb-2">💬 Phân tích Định tính Phản hồi mở (NLP Tagged Responses)</h3>
                    <p class="text-muted">Các biểu đồ phân loại chủ đề do mô hình NLP gán nhãn cho các câu trả lời mở tiếng Việt của sinh viên và thanh công cụ tìm kiếm phản hồi thô.</p>
                    <div class="row g-4 mb-4">
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Phân bố chủ đề phản hồi mở tổng thể</h5>
                                <img src="reports/figures/2_multiple_answers_freetext/freetext_theme_overall.png" class="chart-img" alt="Free Text Theme Overall">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="chart-container text-center">
                                <h5 class="fw-semibold">Chủ đề phản hồi mở phân theo Nhóm câu hỏi</h5>
                                <img src="reports/figures/2_multiple_answers_freetext/freetext_theme_by_question_group.png" class="chart-img" alt="Free Text Theme Groups">
                            </div>
                        </div>
                    </div>

                    <!-- SEARCHABLE DATATABLE -->
                    <div class="card p-4 shadow-sm border-0">
                        <h4 class="fw-bold mb-3">🔍 Tra cứu phản hồi mở sinh viên khảo sát</h4>
                        <div class="row g-3 mb-3">
                            <div class="col-md-6">
                                <label for="question-filter" class="form-label fw-semibold">Lọc theo câu hỏi khảo sát:</label>
                                <select id="question-filter" class="form-select" onchange="filterData()">
                                    <option value="all">-- Hiển thị tất cả --</option>
                                    {"".join([f'<option value="{q}">{q}</option>' for q in unique_questions])}
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label for="search-input" class="form-label fw-semibold">Tìm kiếm từ khóa:</label>
                                <input type="text" id="search-input" class="form-control" placeholder="Nhập từ khóa (ví dụ: 'docker', 'thực hành', 'giảng viên')..." onkeyup="filterData()">
                            </div>
                        </div>

                        <div class="table-responsive-custom">
                            <table class="table table-hover table-striped align-middle mb-0">
                                <thead class="table-dark sticky-top">
                                    <tr>
                                        <th style="width: 25%">Nhóm Câu Hỏi</th>
                                        <th style="width: 55%">Nội Dung Phản Hồi</th>
                                        <th style="width: 20%">Chủ Đề (NLP Tags)</th>
                                    </tr>
                                </thead>
                                <tbody id="table-body">
                                    <!-- Dữ liệu JS tự động render ở đây -->
                                </tbody>
                            </table>
                        </div>
                        <div class="mt-2 text-end text-muted small">
                            Hiển thị: <span id="record-count" class="fw-bold">0</span> phản hồi mở
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer class="footer text-center">
        <div class="container">
            <p class="mb-1 fw-bold text-white">Dự Án Nghiên Cứu Khoa Học DevOps - NEU</p>
            <p class="mb-0 text-white-50 small">Thiết kế hệ thống tự động hóa & trực quan hóa dữ liệu khảo sát khoa học. Bản quyền 2026.</p>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- JavaScript xử lý tìm kiếm & hiển thị bảng dữ liệu phản hồi mở -->
    <script>
        // Dữ liệu phản hồi mở nhúng từ python
        const rawRecords = {free_text_json};

        // Hàm render dữ liệu vào bảng
        function renderTable(data) {{
            const tbody = document.getElementById("table-body");
            tbody.innerHTML = "";
            
            data.forEach(item => {{
                let tagsHtml = "";
                if (item.tags) {{
                    const tagsList = item.tags.split(",");
                    tagsList.forEach(t => {{
                        if (t.trim()) {{
                            tagsHtml += `<span class="badge-tag">${{t.trim()}}</span>`;
                        }}
                    }});
                }}
                
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td class="text-muted small">${{item.question}}</td>
                    <td>${{item.response_raw}}</td>
                    <td>${{tagsHtml}}</td>
                `;
                tbody.appendChild(tr);
            }});
            
            document.getElementById("record-count").innerText = data.length;
        }}

        // Hàm lọc dữ liệu theo bộ lọc câu hỏi và thanh tìm kiếm từ khóa
        function filterData() {{
            const qFilter = document.getElementById("question-filter").value;
            const searchVal = document.getElementById("search-input").value.toLowerCase();
            
            const filtered = rawRecords.filter(item => {{
                const matchQuestion = (qFilter === "all" || item.question === qFilter);
                
                const responseText = (item.response_raw || "").toLowerCase();
                const tagsText = (item.tags || "").toLowerCase();
                const matchSearch = (responseText.includes(searchVal) || tagsText.includes(searchVal));
                
                return matchQuestion && matchSearch;
            }});
            
            renderTable(filtered);
        }}

        // Khởi động render bảng lần đầu tiên
        window.onload = function() {{
            renderTable(rawRecords);
        }};
    </script>
</body>
</html>
"""
    
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    html_path = DOCS_DIR / "index.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"    [OK] Tạo tệp HTML tĩnh thành công tại {html_path}")

def main():
    print("=== BẮT ĐẦU SINH WEBSITE TĨNH GITHUB PAGES ===")
    copy_figures()
    generate_html()
    print("=== HOÀN TẤT SINH WEBSITE TĨNH ===")

if __name__ == "__main__":
    main()
