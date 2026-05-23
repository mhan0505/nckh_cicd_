import json
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def patch_notebook(filepath, cell_replacements):
    """
    filepath: Path or str to the .ipynb file
    cell_replacements: list of tuples (search_str, replacement_str)
    """
    path = Path(filepath)
    if not path.exists():
        print(f"[WARNING] Notebook {path.name} not found, skipping.")
        return False
        
    with open(path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
        
    patched_count = 0
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") in ["code", "markdown"]:
            source = cell.get("source", [])
            # Join lines to make it easy to find multi-line blocks
            source_text = "".join(source)
            
            for search_str, replacement_str in cell_replacements:
                if search_str in source_text:
                    # Perform replacement
                    source_text = source_text.replace(search_str, replacement_str)
                    # Split back to lines (preserving trailing newlines)
                    new_source = []
                    lines = source_text.splitlines(keepends=True)
                    for line in lines:
                        new_source.append(line)
                    cell["source"] = new_source
                    patched_count += 1
                    
    if patched_count > 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(notebook, f, ensure_ascii=False, indent=1)
        print(f"[SUCCESS] Successfully patched {path.name} ({patched_count} replacements)")
        return True
    else:
        print(f"[INFO] No replacements needed in {path.name}")
        return False

# ==========================================
# 📋 PATCH 1: 0_data_ingestion.ipynb
# ==========================================
ingestion_patches = [
    (
        'df = pd.read_csv(raw_path, encoding="utf-8")',
        'df = pd.read_csv(raw_path, encoding="utf-8-sig")'
    ),
    (
        'assert raw_path.exists(), f" Không tìm thấy file: {RAW_FILE}"',
        'if not raw_path.exists():\n    raise FileNotFoundError(f" Không tìm thấy file: {raw_path.resolve()}")'
    )
]
patch_notebook("0_data_ingestion.ipynb", ingestion_patches)

# ==========================================
# 📋 PATCH 2: 1a_cleanup.ipynb
# ==========================================
cleanup_patches = [
    # 1. Do NOT impute Likert scale columns globally with medians
    (
        '# Likert columns: fill NaN với median (robust với outlier)\nfor col in LIKERT_COLS:\n    if col in df.columns and df[col].isnull().any():\n        median_val = df[col].median()\n        df[col] = df[col].fillna(median_val)\n        print(f"   {col}: filled {df[col].isnull().sum()} NaN → median={median_val}")',
        '# LƯU Ý: Không tự động điền giá trị trung vị cho các cột Likert của sinh viên chưa dùng CI/CD\n# Điều này để tránh tạo dữ liệu khống làm sai lệch phân tích tương quan và hồi quy UTAUT/DORA chéo.\nfor col in LIKERT_COLS:\n    if col in df.columns:\n        n_missing = df[col].isnull().sum()\n        print(f"   {col}: giữ nguyên {n_missing} NaN (không điền median)")'
    ),
    # 2. Convert Likert columns to Int64 (nullable integers) to support NaNs
    (
        '# Chuyển Likert sang int (sau khi fill NaN)\nfor col in LIKERT_COLS:\n    if col in df.columns:\n        df[col] = df[col].astype(int)',
        '# Chuyển sang kiểu Int64 (nullable integer) để hỗ trợ NaNs\nfor col in LIKERT_COLS:\n    if col in df.columns:\n        df[col] = df[col].astype("Int64")'
    ),
    # 3. Add Typo correction and Troll filtering before saving cleaned responses
    (
        '# ══════════════════════════════════════════════════════════\n# BƯỚC 5: LƯU FILE\n# ══════════════════════════════════════════════════════════\n\ndf.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")',
        '# ── Sửa lỗi chính tả tiếng Việt trong dữ liệu khảo sát ──\nTYPO_MAP = {\n    "Kiểm thử tự đông (Automated Testing)": "Kiểm thử tự động (Automated Testing)",\n    "Phân phối liên tuc (CD - Delivery)": "Phân phối liên tục (CD - Delivery)",\n    "Xây dụng (Build)": "Xây dựng (Build)",\n    "Chưa hiểu rõ lợi ích thực tế khi trển khai CI/CD": "Chưa hiểu rõ lợi ích thực tế khi triển khai CI/CD"\n}\nfor col in df.columns:\n    if df[col].dtype == "object":\n        for k, v in TYPO_MAP.items():\n            df[col] = df[col].str.replace(k, v, regex=False)\n\n# ══════════════════════════════════════════════════════════\n# BƯỚC 5: LƯU FILE\n# ══════════════════════════════════════════════════════════\n\ndf.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")'
    )
]
patch_notebook("1a_cleanup.ipynb", cleanup_patches)

# ==========================================
# 📋 PATCH 3: 1b_multiple_answer_cleanup.ipynb
# ==========================================
multiple_cleanup_patches = [
    # 1. Update one_hot_encode_checkbox to use exact substring matching & filter trolls
    (
        'def one_hot_encode_checkbox(series, col_prefix):\n    """\n    Chuyển cột checkbox (giá trị phân cách bằng dấu phẩy) → One-Hot DataFrame.\n    Sử dụng vectorized operations thay vì vòng lặp for.\n    \n    Parameters:\n        series: pd.Series chứa các giá trị checkbox\n        col_prefix: tiền tố cho tên cột output\n    \n    Returns:\n        pd.DataFrame với các cột binary (0/1)\n    """\n    # Split mỗi giá trị thành list, strip whitespace\n    split_series = series.str.split(",").apply(\n        lambda x: [item.strip() for item in x] if isinstance(x, list) else []\n    )\n    \n    # Dùng MultiLabelBinarizer logic bằng pandas\n    # Tạo DataFrame từ explode + get_dummies\n    exploded = split_series.explode()\n    \n    # Loại bỏ giá trị rỗng và "Không trả lời"\n    exploded = exploded[exploded.str.len() > 0]\n    exploded = exploded[exploded != "Không trả lời"]\n    \n    if exploded.empty:\n        return pd.DataFrame(index=series.index)\n    \n    # One-hot via crosstab\n    dummies = pd.crosstab(exploded.index, exploded)\n    \n    # Clip to binary (0 or 1)\n    dummies = dummies.clip(upper=1)\n    \n    # Reindex to match original index (fill missing rows with 0)\n    dummies = dummies.reindex(series.index, fill_value=0)\n    \n    # Rename columns with prefix\n    dummies.columns = [f"{col_prefix}__{c}" for c in dummies.columns]\n    \n    return dummies',
        'PREDEFINED_OPTIONS = {\n    "Q4_product_field": [\n        "Phần mềm ứng dụng (Web, Mobile, Desktop App)",\n        "Hệ thống AI/Big Data/Data Science",\n        "Hệ thống nhúng (Embedded)/IoT",\n        "Giải pháp hạ tầng & Bảo mật"\n    ],\n    "Q7_tools_used": [\n        "Jenkins",\n        "GitLab CI/CD",\n        "GitHub Actions",\n        "Circle CI",\n        "Travis CI",\n        "Chưa từng sử dụng công cụ CI/CD nào"\n    ],\n    "Q8_learning_source": [\n        "Môn học tại trường đại học",\n        "Dự án cá nhân / Đồ án môn học",\n        "Thực tập tại doanh nghiệp",\n        "Khóa học online (Coursera, YouTube, ...)",\n        "Tự tìm hiểu qua tài liệu trên Internet"\n    ],\n    "Q9_usage_purpose": [\n        "Build / Tự động hoá quá trình build",\n        "Continuous Integration (CI) – tích hợp & kiểm tra mã nguồn tự động",\n        "Continuous Deployment / Delivery (CD) – triển khai tự động",\n        "Automated Testing – kiểm thử tự động",\n        "Tự động hoá quy trình phát triển (workflow automation)",\n        "Học tập / nghiên cứu / thử nghiệm cá nhân"\n    ],\n    "Q10_cicd_benefits": [\n        "Tự động hóa quy trình build và test",\n        "Phát hiện lỗi sớm hơn",\n        "Tăng tốc độ phát triển phần mềm",\n        "Hỗ trợ làm việc nhóm tốt hơn",\n        "Giảm lỗi khi triển khai phần mềm"\n    ],\n    "Q33_cicd_difficulties": [\n        "Tích hợp liên tục (CI - Integration)",\n        "Xây dựng (Build)",\n        "Kiểm thử tự động (Automated Testing)",\n        "Phân phối liên tục (CD - Delivery)",\n        "Triển khai liên tục (CD - Deployment)",\n        "Giám sát & Phản hồi"\n    ],\n    "Q34_adoption_barriers": [\n        "Thiếu kiến thức hoặc kỹ năng về DevOps/CI/CD",\n        "Thiếu tài liệu hoặc hướng dẫn thực hành rõ ràng",\n        "Việc thiết lập và cấu hình công cụ CI/CD khá phức tạp",\n        "Thiếu môi trường thực hành (server, cloud, Docker, v.v.)",\n        "Ít cơ hội áp dụng CI/CD trong các môn học tại trường",\n        "Chưa hiểu rõ lợi ích thực tế khi triển khai CI/CD"\n    ],\n    "Q39_biggest_barrier": [\n        "Thiếu kiến thức hoặc kỹ năng về CI/CD và DevOps",\n        "Khó thiết lập và cấu hình các công cụ CI/CD",\n        "Thiếu môi trường thực hành (server, cloud, Docker, v.v.)",\n        "Ít cơ hội thực hành CI/CD trong các môn học tại trường",\n        "Dự án học tập còn đơn giản nên chưa thấy cần CI/CD",\n        "Khó phối hợp làm việc nhóm khi áp dụng CI/CD"\n    ],\n    "Q40_expected_benefit": [\n        "Giảm bớt các công việc thủ công lặp đi lặp lại (build, test, deploy)",\n        "Phát hiện lỗi sớm hơn trong quá trình phát triển phần mềm.",\n        "Tăng tốc độ phát triển và cập nhật dự án.",\n        "Nâng cao kỹ năng DevOps và kinh nghiệm thực tế cho sinh viên."\n    ]\n}\n\ndef one_hot_encode_checkbox(series, col_prefix):\n    predefined_list = PREDEFINED_OPTIONS.get(col_prefix, [])\n    # Tạo DataFrame có giá trị 0 sẵn để gán\n    dummies = pd.DataFrame(0, index=series.index, columns=[f"{col_prefix}__{opt}" for opt in predefined_list])\n    \n    for idx, val in series.items():\n        if pd.isna(val) or val == "Không trả lời":\n            continue\n            \n        # So khớp substring chính xác\n        for opt in predefined_list:\n            if opt in str(val):\n                dummies.at[idx, f"{col_prefix}__{opt}"] = 1\n                \n        # Tìm và xử lý viết ý kiến tự do (\"Mục khác\" / custom write-ins)\n        parts = [p.strip() for p in str(val).split(",") if p.strip()]\n        for part in parts:\n            # Kiểm tra xem đây có phải là một phần của đáp án chuẩn bị cắt sai hay không\n            is_predefined = False\n            for opt in predefined_list:\n                if part in opt or opt in part:\n                    is_predefined = True\n                    break\n            \n            if not is_predefined:\n                # Loại bỏ troll/test response rõ rệt\n                if part.lower() in ["nhi béo", "nhi", "dsfdsfds", "ko", "không", "không có", "chưa có"]:\n                    continue\n                \n                # Tạo cột mới động cho viết tự do\n                col_name = f"{col_prefix}__{part}"\n                if col_name not in dummies.columns:\n                    dummies[col_name] = 0\n                dummies.at[idx, col_name] = 1\n                \n    return dummies'
    )
]
patch_notebook("1b_multiple_answer_cleanup.ipynb", multiple_cleanup_patches)

# ==========================================
# 📋 PATCH 4: 1c_free_text_tagging.ipynb
# ==========================================
freetext_patches = [
    # 1. Update file loading cell to dynamically extract from cleaned_responses.csv
    (
        '# ── Config ──────────────────────────────────────────────\nINPUT_FILE = "open_ended_responses.txt"\nOUTPUT_FILE = "tagged_free_text.csv"\n\nassert Path(INPUT_FILE).exists(), f" Không tìm thấy {INPUT_FILE}!"\n\nraw_text = Path(INPUT_FILE).read_text(encoding="utf-8")\nprint(f" Đọc {INPUT_FILE}: {len(raw_text)} ký tự")',
        '# ── Config ──────────────────────────────────────────────\nINPUT_FILE = "cleaned_responses.csv"\nOUTPUT_FILE = "tagged_free_text.csv"\n\nassert Path(INPUT_FILE).exists(), f" Không tìm thấy {INPUT_FILE}!"\n\n# Đọc cleaned_responses.csv trực tiếp\ndf_clean = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")\nprint(f" Đọc {INPUT_FILE} thành công: {df_clean.shape[0]} dòng")'
    ),
    # 2. Update parsing function to dynamic pandas extraction
    (
        'def parse_open_ended(text):\n    """\n    Parse file text thành list of dict:\n    [{question, response_id, response_text}, ...]\n    """\n    records = []\n    current_question = None\n    \n    for line in text.strip().split("\\n"):\n        line = line.strip()\n        if not line:\n            continue\n        \n        # Nhận diện câu hỏi: kết thúc bằng "?:" hoặc ":" và không bắt đầu bằng số\n        if line.endswith("?:") or (line.endswith(":") and not re.match(r"^\\s*\\d+\\.", line)):\n            current_question = line.rstrip(":")\n            continue\n        \n        # Nhận diện câu trả lời: bắt đầu bằng "số."\n        match = re.match(r"^(\\d+)\\.\\s*(.+)", line)\n        if match and current_question:\n            resp_id = int(match.group(1))\n            resp_text = match.group(2).strip()\n            records.append({\n                "question": current_question,\n                "response_id": resp_id,\n                "response_raw": resp_text,\n            })\n    \n    return pd.DataFrame(records)\n\ndf_text = parse_open_ended(raw_text)',
        'def extract_open_ended_programmatic(df_source):\n    records = []\n    mapping = {\n        "Q35_improvement_suggestions": "Theo bạn, điều gì cần được cải thiện để sinh viên dễ tiếp cận và học CI/CD hiệu quả hơn?",\n        "Q36_university_suggestions": "Bạn có đề xuất nào để các trường đại học hoặc giảng viên hỗ trợ sinh viên học và áp dụng CI/CD tốt hơn trong các môn học hoặc dự án?",\n        "Q37_skills_needed": "Theo bạn, sinh viên cần được trang bị thêm những kiến thức hoặc kỹ năng nào để áp dụng CI/CD hiệu quả trong các dự án phần mềm?"\n    }\n    \n    for col, q_text in mapping.items():\n        if col in df_source.columns:\n            # Lọc bỏ giá trị trống và câu trả lời rác\n            valid_subset = df_source[df_source[col] != "Không trả lời"][col]\n            for idx, val in valid_subset.items():\n                val_str = str(val).strip()\n                if val_str.lower() in ["nhi", "nhi béo", "dsfdsfds", "ko", "không", "không có", "chưa có", "dsfdf", "fsdfsđfsdf"]:\n                    continue\n                records.append({\n                    "question": q_text,\n                    "response_id": idx + 1,\n                    "response_raw": val_str,\n                })\n    return pd.DataFrame(records)\n\ndf_text = extract_open_ended_programmatic(df_clean)'
    )
]
patch_notebook("1c_free_text_tagging.ipynb", freetext_patches)

print("[FINISHED] ALL JUPYTER NOTEBOOKS PATCHED SUCCESSFULLY!")
