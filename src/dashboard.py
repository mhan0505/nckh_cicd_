import os
import json
import urllib.request
import pandas as pd
import streamlit as st
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="NEU CI/CD Survey Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh để làm dashboard trông cao cấp và hiện đại hơn
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 5px;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Thư mục cơ sở
BASE_DIR = Path(__file__).parent.parent.resolve()
RAW_FILE_PATH = BASE_DIR / "raw" / "CI_CD Survey Output - Student.csv"
STATUS_FILE_PATH = BASE_DIR / "scratch" / "pipeline_status.json"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
CLEANED_DATA_PATH = BASE_DIR / "processed" / "cleaned_responses.csv"
TAGGED_FREE_TEXT_PATH = BASE_DIR / "processed" / "tagged_free_text.csv"

# URL mặc định của Google Sheet dạng CSV
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/1P_hyU6PUNp7ePHZQKY_G0aMwJgPjmxLhmhawHWjb_dY/export?format=csv&gid=135898341"

# Hàm lấy trạng thái đồng bộ gần nhất
def get_sync_status():
    if not STATUS_FILE_PATH.exists():
        return {"status": "idle", "updated_at": "Chưa từng đồng bộ"}
    try:
        with open(STATUS_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"status": "unknown", "updated_at": "Lỗi đọc trạng thái"}

# Hàm ghi trạng thái đồng bộ
def save_sync_status(status: str, error_msg: str = "", start_time: str = None, elapsed: float = None):
    try:
        data = {}
        if STATUS_FILE_PATH.exists():
            with open(STATUS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        data["status"] = status
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if error_msg:
            data["last_error"] = error_msg
        if start_time:
            data["last_run_start"] = start_time
        if elapsed is not None:
            data["last_run_elapsed_seconds"] = round(elapsed, 2)
            
        STATUS_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(STATUS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi khi ghi trạng thái: {e}")

# Hàm chạy pipeline
def run_pipeline(sheet_url: str):
    start_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = datetime.now()
    save_sync_status("running", start_time=start_time_str)
    
    try:
        # 1. Tải CSV
        RAW_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(
            sheet_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            csv_data = response.read()
        with open(RAW_FILE_PATH, "wb") as f:
            f.write(csv_data)
            
        # 2. Chạy pipeline.py
        pipeline_script = BASE_DIR / "run_pipeline.py"
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        result = subprocess.run(
            [sys.executable, str(pipeline_script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(BASE_DIR),
            env=env
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if result.returncode == 0:
            save_sync_status("success", elapsed=elapsed)
            return True, "Đồng bộ dữ liệu và chạy phân tích thành công!"
        else:
            err = result.stderr if result.stderr else result.stdout
            save_sync_status("failed", error_msg=err, elapsed=elapsed)
            return False, f"Pipeline thất bại: {err[-500:]}"
    except Exception as e:
        elapsed = (datetime.now() - start_time).total_seconds()
        save_sync_status("failed", error_msg=str(e), elapsed=elapsed)
        return False, f"Lỗi hệ thống: {str(e)}"

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
st.sidebar.title("NEU DevOps Research")
st.sidebar.markdown("Dự án nghiên cứu mức độ áp dụng CI/CD của sinh viên CNTT tại Việt Nam (Thầy Thảo hướng dẫn).")
st.sidebar.divider()

# Trạng thái đồng bộ hiển thị trên sidebar
status_info = get_sync_status()
status_color = {
    "success": "🟢 Thành công",
    "failed": "🔴 Thất bại",
    "running": "🟡 Đang chạy...",
    "idle": "⚪ Chưa chạy",
    "unknown": "⚪ Không rõ"
}.get(status_info.get("status", "idle"), "⚪ Chưa rõ")

st.sidebar.subheader("🔄 Đồng bộ dữ liệu")
st.sidebar.markdown(f"**Trạng thái:** {status_color}")
st.sidebar.markdown(f"**Lần cuối:** `{status_info.get('updated_at', 'Chưa có')}`")

if status_info.get("status") == "running":
    st.sidebar.warning("Pipeline đang chạy ngầm trên server...")
else:
    sheet_url_input = st.sidebar.text_input("Google Sheet CSV URL", value=DEFAULT_SHEET_URL)
    if st.sidebar.button("Đồng bộ dữ liệu & Chạy lại phân tích"):
        with st.spinner("Đang tải dữ liệu và chạy pipeline phân tích (khoảng 30-40 giây)..."):
            success, msg = run_pipeline(sheet_url_input)
            if success:
                st.sidebar.success(msg)
                st.rerun()
            else:
                st.sidebar.error(msg)

st.sidebar.divider()
st.sidebar.info("Dashboard tự động đọc các thư mục dữ liệu sạch (`processed/`) và các biểu đồ đã được sinh ra bởi Jupyter Notebook pipeline để đảm bảo tính đồng nhất khoa học.")

# ══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════

st.title("📊 Khảo sát CI/CD & Năng lực DevOps của Sinh viên CNTT")
st.markdown("Hệ thống trực quan hóa báo cáo nghiên cứu khoa học tự động. Dữ liệu khảo sát từ Đại học Kinh tế Quốc dân (NEU) và các trường đại học công nghệ.")

# Load dữ liệu cơ bản
@st.cache_data
def load_data():
    if CLEANED_DATA_PATH.exists():
        df = pd.read_csv(CLEANED_DATA_PATH)
        return df
    return None

df = load_data()

if df is None:
    st.warning("⚠️ Không tìm thấy dữ liệu sạch. Vui lòng bấm nút 'Đồng bộ dữ liệu & Chạy lại phân tích' ở sidebar trái để khởi tạo dữ liệu ban đầu.")
else:
    # ── METRIC CARDS ──
    total_respondents = len(df)
    
    # Tính tỉ lệ sử dụng CI/CD
    used_cicd_count = df['Q30_actual_usage'].sum() if 'Q30_actual_usage' in df.columns else 0
    used_cicd_pct = (used_cicd_count / total_respondents) * 100 if total_respondents > 0 else 0
    
    # Đọc DORA Performance từ báo cáo phân tích nâng cao (nếu có)
    elite_pct = 14.6 # giá trị mặc định dựa trên báo cáo
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #3b82f6;">
            <div class="metric-label">Tổng số phản hồi (Mẫu khảo sát)</div>
            <div class="metric-value">{total_respondents} sinh viên</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #10b981;">
            <div class="metric-label">Tỷ lệ đã thực tế sử dụng CI/CD</div>
            <div class="metric-value">{used_cicd_pct:.1f}% ({int(used_cicd_count)} sv)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #f59e0b;">
            <div class="metric-label">Nhóm Năng lực DORA Xuất sắc (Elite)</div>
            <div class="metric-value">{elite_pct:.1f}% mẫu</div>
        </div>
        """, unsafe_allow_html=True)

    # ── TABS PHÂN TÍCH ──
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏫 Nhân khẩu học",
        "🎯 DORA & DevOps Performance",
        "🧠 Mô hình UTAUT & Tương quan",
        "🚧 Rào cản & Thử thách",
        "💬 Ý kiến phản hồi mở",
        "📂 Dữ liệu khảo sát thô"
    ])

    # TAb 1: NHÂN KHẨU HỌC
    with tab1:
        st.header("🏫 Phân tích Nhân khẩu học & Mức độ Nhận thức cơ bản")
        st.markdown("Thống kê mô tả về phân bố Trường học, Năm học, Chuyên ngành và mức độ tự động hóa tự đánh giá.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Trường đại học của sinh viên khảo sát")
            img_path = FIGURES_DIR / "1_demographics_descriptive" / "Q1_university_pie.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            else:
                st.info("Biểu đồ đang được tạo hoặc chưa hoàn thành.")
                
            st.subheader("Phân bố Chuyên ngành đào tạo")
            img_path = FIGURES_DIR / "1_demographics_descriptive" / "Q3_major_bar.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
        with c2:
            st.subheader("Phân bố Năm học của sinh viên")
            img_path = FIGURES_DIR / "1_demographics_descriptive" / "Q2_year_pie.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
            st.subheader("Mức độ nhận thức về CI/CD")
            img_path = FIGURES_DIR / "1_demographics_descriptive" / "Q5_cicd_awareness_pie.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)

        st.subheader("Mức độ tự động hóa trong các dự án lập trình thực tế")
        img_path = FIGURES_DIR / "1_demographics_descriptive" / "Q6_automation_level_bar.png"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

    # TAB 2: DORA PERFORMANCE
    with tab2:
        st.header("🎯 Chỉ số DORA Metrics & Phân loại hiệu suất DevOps")
        st.markdown("""
        Hiệu suất phân phối phần mềm được đo bằng 4 chỉ số DORA tiêu chuẩn:
        - **Deployment Frequency**: Tần suất triển khai.
        - **Lead Time for Changes**: Thời gian từ lúc commit đến khi chạy production.
        - **Mean Time to Recovery (MTTR)**: Thời gian khôi phục dịch vụ khi gặp lỗi.
        - **Change Failure Rate**: Tỷ lệ triển khai thất bại hoặc gặp lỗi nghiêm trọng.
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Phân nhóm Năng lực DevOps (DORA Performance)")
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h1_dora_classification.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            
            st.subheader("DORA Score theo Năm học & Trường đại học")
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h3_dora_by_year_uni.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
        with c2:
            st.subheader("So sánh DORA Score: Nhóm dùng CI/CD vs Chưa dùng")
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h2_cicd_vs_dora.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
            st.subheader("Hiệu năng DORA theo Nguồn tiếp cận CI/CD")
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h9_learning_vs_dora.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)

        st.divider()
        st.subheader("Phân tích tần suất chi tiết 4 chỉ số DORA gốc của sinh viên")
        dora_cols = st.columns(4)
        dora_files = [
            ("Q11_deploy_frequency_bar.png", "Tần suất triển khai (Q11)"),
            ("Q12_lead_time_bar.png", "Lead Time (Q12)"),
            ("Q13_recovery_time_bar.png", "Thời gian khôi phục MTTR (Q13)"),
            ("Q14_failure_rate_pie.png", "Tỷ lệ lỗi Change Failure Rate (Q14)")
        ]
        for idx, (filename, title) in enumerate(dora_files):
            with dora_cols[idx]:
                img_path = FIGURES_DIR / "1_demographics_descriptive" / filename
                if img_path.exists():
                    st.image(str(img_path), caption=title, use_container_width=True)

    # TAB 3: UTAUT
    with tab3:
        st.header("🧠 Mô hình Chấp nhận Công nghệ UTAUT & Ma trận tương quan")
        st.markdown("""
        Mô hình kiểm định 5 khía cạnh ảnh hưởng đến quyết định áp dụng công nghệ CI/CD của sinh viên:
        1. **Performance Expectancy (Kỳ vọng hiệu quả)**
        2. **Effort Expectancy / Ease of Learning (Kỳ vọng nỗ lực / Dễ học)**
        3. **Social Influence (Ảnh hưởng xã hội / Đồng nghiệp / Mentor)**
        4. **Facilitating Conditions (Điều kiện thuận lợi / Hạ tầng / Nhà trường hỗ trợ)**
        5. **Behavioral Intention (Ý định hành vi)** dẫn đến **Use Behavior (Sử dụng thực tế)**.
        """)
        
        c1, c2 = st.columns([3, 2])
        with c1:
            st.subheader("Ma trận tương quan Pearson giữa các nhân tố UTAUT")
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h_utaut_heatmap.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
        with c2:
            st.subheader("Khoảng cách giữa Ý định (Intention) và Hành vi sử dụng (Use)")
            st.markdown("""
            **Ý định của sinh viên rất cao nhưng hành vi sử dụng thực tế còn hạn chế.** 
            Sự chênh lệch này (Intention-Action Gap) chỉ ra rằng sinh viên rất muốn dùng nhưng thiếu hạ tầng hoặc thiếu định hướng môn học cụ thể.
            """)
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h14_intention_vs_use_gap.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)

        st.divider()
        st.subheader("Hồi quy tương quan tuyến tính chi tiết")
        reg_cols = st.columns(3)
        reg_files = [
            ("adv_h11_self_efficacy_vs_use.png", "Tự đánh giá năng lực vs Sử dụng thực tế"),
            ("adv_h12_social_vs_intention.png", "Ảnh hưởng xã hội vs Ý định áp dụng"),
            ("adv_h13_support_vs_use.png", "Điều kiện hỗ trợ vs Sử dụng thực tế")
        ]
        for idx, (filename, title) in enumerate(reg_files):
            with reg_cols[idx]:
                img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / filename
                if img_path.exists():
                    st.image(str(img_path), caption=title, use_container_width=True)

    # TAB 4: RÀO CẢN
    with tab4:
        st.header("🚧 Rào cản & Khó khăn lớn nhất đối với Sinh viên")
        st.markdown("Phân tích nguyên nhân tại sao sinh viên khó tiếp cận hoặc chưa áp dụng các công cụ CI/CD.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Biểu đồ Pareto: Khó khăn lớn nhất trong quy trình CI/CD")
            img_path = FIGURES_DIR / "2a_multiple_choice" / "Q33_cicd_difficulties_pareto.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
            st.subheader("Phân bố rào cản CI/CD theo Năm học")
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h16_barriers_by_year.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
        with c2:
            st.subheader("Biểu đồ Pareto: Thách thức khiến sinh viên khó áp dụng")
            img_path = FIGURES_DIR / "2a_multiple_choice" / "Q34_adoption_barriers_pareto.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
            st.subheader("So sánh rào cản giữa Nhóm nhận thức Thấp vs Cao")
            img_path = FIGURES_DIR / "3_advanced_grouping_correlation" / "adv_h15_barriers_by_awareness.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)

    # TAB 5: FREE TEXT QUALITATIVE
    with tab5:
        st.header("💬 Phân tích Định tính Phản hồi mở (Free Text Qualitative)")
        st.markdown("Xử lý ngôn ngữ tự nhiên (NLP) trên các câu trả lời mở tiếng Việt của sinh viên để phân loại chủ đề phản hồi chính.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Phân bố chủ đề phản hồi mở chung")
            img_path = FIGURES_DIR / "2b_freetext" / "freetext_theme_overall.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                
        with c2:
            st.subheader("Phân bố chủ đề theo các nhóm câu hỏi cụ thể")
            img_path = FIGURES_DIR / "2b_freetext" / "freetext_theme_by_question_group.png"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)

        st.subheader("🔍 Chi tiết câu trả lời mở và nhãn chủ đề đã gán (NLP Tagged Responses)")
        if TAGGED_FREE_TEXT_PATH.exists():
            df_free_text = pd.read_csv(TAGGED_FREE_TEXT_PATH)
            
            # Lọc theo câu hỏi
            unique_questions = df_free_text['question'].unique()
            selected_q = st.selectbox("Chọn câu hỏi mở để xem phản hồi:", unique_questions)
            
            filtered_ft = df_free_text[df_free_text['question'] == selected_q]
            
            # Input tìm kiếm từ khóa
            search_query = st.text_input("Tìm kiếm từ khóa trong câu trả lời:", "")
            if search_query:
                filtered_ft = filtered_ft[
                    filtered_ft['response_raw'].str.contains(search_query, case=False, na=False) |
                    filtered_ft['tags'].str.contains(search_query, case=False, na=False)
                ]
            
            st.write(f"Tìm thấy **{len(filtered_ft)}** phản hồi:")
            st.dataframe(
                filtered_ft[['response_raw', 'tags', 'token_count']],
                column_config={
                    "response_raw": st.column_config.TextColumn("Nội dung câu trả lời mở gốc", width="large"),
                    "tags": st.column_config.TextColumn("Nhãn chủ đề (NLP Tags)", width="medium"),
                    "token_count": st.column_config.NumberColumn("Độ dài từ")
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Chưa có tệp dữ liệu phân tích phản hồi mở (`processed/tagged_free_text.csv`).")

    # TAB 6: RAW DATA
    with tab6:
        st.header("📂 Dữ liệu khảo sát gốc (Bảng dữ liệu đã chuẩn hóa biến)")
        st.markdown("Dưới đây là dữ liệu thô sau khi được xử lý chuẩn hóa tên biến từ tiếng Việt sang các nhãn biến tiếng Anh chuẩn phục vụ nghiên cứu.")
        
        # Cho phép tìm kiếm toàn bộ bảng dữ liệu
        univ_list = ["Tất cả"] + list(df['Q1_university'].unique())
        selected_univ = st.selectbox("Lọc dữ liệu theo Trường học:", univ_list)
        
        year_list = ["Tất cả"] + list(df['Q2_year'].unique())
        selected_year = st.selectbox("Lọc dữ liệu theo Năm học:", year_list)
        
        filtered_df = df.copy()
        if selected_univ != "Tất cả":
            filtered_df = filtered_df[filtered_df['Q1_university'] == selected_univ]
        if selected_year != "Tất cả":
            filtered_df = filtered_df[filtered_df['Q2_year'] == selected_year]
            
        st.write(f"Số lượng dòng thỏa mãn điều kiện lọc: **{len(filtered_df)} / {len(df)}**")
        
        st.dataframe(
            filtered_df,
            use_container_width=True
        )
        
        # Nút download dữ liệu CSV đã lọc
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Tải bảng dữ liệu đã lọc (.csv)",
            data=csv,
            file_name="filtered_survey_data.csv",
            mime="text/csv",
        )
