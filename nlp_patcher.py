import json
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def patch_notebook(filepath, cell_replacements):
    path = Path(filepath)
    if not path.exists():
        print(f"[WARNING] Notebook {path.name} not found.")
        return False
        
    with open(path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
        
    patched_count = 0
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") in ["code", "markdown"]:
            source = cell.get("source", [])
            source_text = "".join(source)
            
            for search_str, replacement_str in cell_replacements:
                if search_str in source_text:
                    source_text = source_text.replace(search_str, replacement_str)
                    new_source = source_text.splitlines(keepends=True)
                    cell["source"] = new_source
                    patched_count += 1
                    
    if patched_count > 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(notebook, f, ensure_ascii=False, indent=1)
        print(f"[SUCCESS] Patched {path.name} ({patched_count} replacements)")
        return True
    return False

# ==========================================
# 📋 PATCH 1: 1c_free_text_tagging.ipynb
# ==========================================
freetext_patches = [
    # Enhance normalize_text to join common Vietnamese IT/survey compound words
    (
        'def normalize_text(text):\n    """Chuẩn hóa: lowercase, bỏ dấu câu, bỏ số đứng riêng."""\n    if not isinstance(text, str):\n        return ""\n    text = text.lower().strip()\n    # Bỏ dấu câu (giữ chữ cái Unicode + khoảng trắng)\n    text = re.sub(r"[^\\w\\s]", " ", text, flags=re.UNICODE)\n    # Bỏ số đứng riêng\n    text = re.sub(r"\\b\\d+\\b", "", text)\n    # Chuẩn hóa khoảng trắng\n    text = re.sub(r"\\s+", " ", text).strip()\n    return text',
        'VIETNAMESE_COMPOUND_WORDS = {\n    # ── IT & DevOps Chuyên Ngành ───────────────────────\n    "sinh viên": "sinh_viên",\n    "giảng viên": "giảng_viên",\n    "nhà trường": "nhà_trường",\n    "doanh nghiệp": "doanh_nghiệp",\n    "môn học": "môn_học",\n    "học phần": "học_phần",\n    "chương trình": "chương_trình",\n    "giảng dạy": "giảng_dạy",\n    "đào tạo": "đào_tạo",\n    "đại học": "đại_học",\n    "thực tập": "thực_tập",\n    "lý thuyết": "lý_thuyết",\n    "thực hành": "thực_hành",\n    "thực tế": "thực_tế",\n    "kinh nghiệm": "kinh_nghiệm",\n    "kiến thức": "kiến_thức",\n    "kỹ năng": "kỹ_năng",\n    "công cụ": "công_cụ",\n    "phần mềm": "phần_mềm",\n    "mã nguồn": "mã_nguồn",\n    "quy trình": "quy_trình",\n    "sơ đồ": "sơ_đồ",\n    "luồng đi": "luồng_đi",\n    # ── Hoạt động & Triển khai ─────────────────────────\n    "phát triển phần mềm": "phát_triển_phần_mềm",\n    "phát triển": "phát_triển",\n    "triển khai": "triển_khai",\n    "áp dụng": "áp_dụng",\n    "sử dụng": "sử_dụng",\n    "tích hợp liên tục": "tích_hợp_liên_tục",\n    "tích hợp": "tích_hợp",\n    "tự động hóa": "tự_động_hóa",\n    "kiểm thử tự động": "kiểm_thử_tự_động",\n    "kiểm thử": "kiểm_thử",\n    "tự động": "tự_động",\n    "phát hiện lỗi": "phát_hiện_lỗi",\n    "thiết lập": "thiết_lập",\n    "cấu hình": "cấu_hình",\n    "môi trường": "môi_trường",\n    # ── Động từ / Danh từ khảo sát khác ───────────────\n    "giới thiệu": "giới_thiệu",\n    "thực hiện": "thực_hiện",\n    "tìm hiểu": "tìm_hiểu",\n    "tự tìm hiểu": "tự_tìm_hiểu",\n    "tự học": "tự_học",\n    "đề xuất": "đề_xuất",\n    "thúc đẩy": "thúc_đẩy",\n    "mong đợi": "mong_đợi",\n    "hiệu quả": "hiệu_quả",\n    "thông tin": "thông_tin",\n    "nền tảng": "nền_tảng",\n    "cung cấp": "cung_cấp",\n    "lập trình": "lập_trình",\n    "quản lý": "quản_lý",\n    "tổ chức": "tổ_chức",\n    "khó khăn": "khó_khăn",\n    "rào cản": "rào_cản",\n    "tiết kiệm": "tiết_kiệm",\n    "thời gian": "thời_gian",\n    # ── Khắc phục các âm tiết rời ở 3 biểu đồ mới ──────\n    "cơ hội": "cơ_hội",\n    "giảm bớt": "giảm_bớt",\n    "công việc": "công_việc",\n    "thủ công": "thủ_công",\n    "lặp đi lặp lại": "lặp_đi_lặp_lại",\n    "quá trình": "quá_trình",\n    "tốc độ": "tốc_độ",\n    "dự án": "dự_án",\n    "đơn giản": "đơn_giản",\n    "kế hoạch": "kế_hoạch",\n    "thời gian tới": "thời_gian_tới",\n    "chưa có": "chưa_có",\n    "chưa áp dụng": "chưa_áp_dụng",\n    "thiếu kiến thức": "thiếu_kiến_thức",\n    "thiếu môi trường": "thiếu_môi_trường",\n    "phổ biến": "phổ_biến",\n    "đầy đủ": "đầy_đủ",\n    "tiếp cận": "tiếp_cận",\n    "biện pháp": "biện_pháp",\n    "chủ động": "chủ_động"\n}\n\ndef normalize_text(text):\n    """Chuẩn hóa: lowercase, bỏ dấu câu, bỏ số đứng riêng, ghép từ ghép tiếng Việt."""\n    if not isinstance(text, str):\n        return ""\n    text = text.lower().strip()\n    # Bỏ dấu câu (giữ chữ cái Unicode + khoảng trắng)\n    text = re.sub(r"[^\\w\\s]", " ", text, flags=re.UNICODE)\n    # Bỏ số đứng riêng\n    text = re.sub(r"\\b\\d+\\b", "", text)\n    # Ghép từ ghép tiếng Việt (ưu tiên cụm dài trước)\n    for k in sorted(VIETNAMESE_COMPOUND_WORDS.keys(), key=len, reverse=True):\n        text = text.replace(k, VIETNAMESE_COMPOUND_WORDS[k])\n    # Chuẩn hóa khoảng trắng\n    text = re.sub(r"\\s+", " ", text).strip()\n    return text'
    )
]
patch_notebook("1c_free_text_tagging.ipynb", freetext_patches)

# ==========================================
# 📋 PATCH 2: 2c_free_text_analysis.ipynb
# ==========================================
analysis_patches = [
    # Replace y-axis labels with space-restored compound words in plot_top_keywords
    (
        '    ax.set_yticks(range(len(freq)))\n    ax.set_yticklabels(freq.index, fontsize=10)\n    ax.invert_yaxis()',
        '    ax.set_yticks(range(len(freq)))\n    # Thay thế dấu gạch dưới thành dấu cách để hiển thị từ ghép tự nhiên\n    clean_labels = [str(label).replace("_", " ") for label in freq.index]\n    ax.set_yticklabels(clean_labels, fontsize=10)\n    ax.invert_yaxis()'
    ),
    # Redirect output images to 2_multiple_answers_freetext subfolder
    (
        'os.makedirs("output", exist_ok=True)',
        'os.makedirs("output/2_multiple_answers_freetext", exist_ok=True)'
    ),
    (
        'plt.savefig(f"output/{filename}"',
        'plt.savefig(f"output/2_multiple_answers_freetext/{filename}"'
    ),
    (
        'print(f"   💾 Saved: output/{filename}")',
        'print(f"   💾 Saved: output/2_multiple_answers_freetext/{filename}")'
    ),
    (
        'plt.savefig("output/freetext_tags_by_question.png"',
        'plt.savefig("output/2_multiple_answers_freetext/freetext_tags_by_question.png"'
    ),
    (
        'print("   💾 Saved: output/freetext_tags_by_question.png")',
        'print("   💾 Saved: output/2_multiple_answers_freetext/freetext_tags_by_question.png")'
    ),
    (
        'output_files = sorted([f for f in os.listdir("output") if f.endswith(".png")])',
        'output_files = sorted([f for f in os.listdir("output/2_multiple_answers_freetext") if f.endswith(".png")])'
    ),
    (
        "size_kb = os.path.getsize(f'output/{f}') / 1024",
        "size_kb = os.path.getsize(f'output/2_multiple_answers_freetext/{f}') / 1024"
    ),
    (
        'print(f"   Tổng file trong output/: {len(output_files)}")',
        'print(f"   Tổng file trong output/2_multiple_answers_freetext/: {len(output_files)}")'
    )
]
patch_notebook("2c_free_text_analysis.ipynb", analysis_patches)

print("[FINISHED] NLP NOTEBOOK PATCHES COMPLETED SUCCESSFULLY!")
