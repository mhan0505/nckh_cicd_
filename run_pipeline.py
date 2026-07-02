#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║            MASTER PIPELINE — "NHẠC TRƯỞNG"               ║
║                                                              ║
║  Chạy tuần tự toàn bộ 3 tầng Data Pipeline:                 ║
║    Tầng 1  →  Data Ingestion                                 ║
║    Tầng 2  →  Data Transformation / Cleaning                 ║
║    Tầng 3  →  Data Analysis & Visualization                  ║
║                                                              ║
║  Dừng ngay lập tức nếu bất kỳ notebook nào thất bại.        ║
║                                                              ║
║  Cách chạy:  python run_pipeline.py                          ║
╚══════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import time
import os
from pathlib import Path
from datetime import datetime

# ── Fix Windows console encoding (cp1252 → UTF-8) ─────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ["PYTHONIOENCODING"] = "utf-8"

# ══════════════════════════════════════════════════════════════
# CẤU HÌNH PIPELINE
# ══════════════════════════════════════════════════════════════

# Thư mục gốc = nơi chứa script này
BASE_DIR = Path(__file__).parent.resolve()

# Tự động tạo các thư mục đầu ra cần thiết nếu chưa tồn tại (tránh lỗi trên máy clone mới)
for folder in ["interim", "processed", "reports", "reports/figures", "reports/free_text", "scratch"]:
    (BASE_DIR / folder).mkdir(parents=True, exist_ok=True)


# Định nghĩa 3 tầng — mỗi tầng là list các notebook
PIPELINE = [
    {
        "tier": "TẦNG 1",
        "name": "Data Ingestion",
        "icon": "",
        "notebooks": [
            "notebooks/0_data_ingestion.ipynb",
        ],
        "expected_outputs": [
            "interim/responses.csv",
        ],
    },
    {
        "tier": "TẦNG 2",
        "name": "Data Transformation / Cleaning",
        "icon": "",
        "notebooks": [
            "notebooks/1a_cleanup.ipynb",
            "notebooks/1b_multiple_answer_cleanup.ipynb",
            "notebooks/1c_free_text_tagging.ipynb",
        ],
        "expected_outputs": [
            "processed/cleaned_responses.csv",
            "processed/multiple_answers_processed.csv",
            "processed/tagged_free_text.csv",
        ],
    },
    {
        "tier": "TẦNG 3",
        "name": "Data Analysis & Visualization",
        "icon": "",
        "notebooks": [
            "notebooks/2a_preliminary_analysis.ipynb",
            "notebooks/2b_multiple_answer_analysis.ipynb",
            "notebooks/2c_free_text_analysis.ipynb",
            "notebooks/3_advanced_analysis.ipynb",
        ],
        "expected_outputs": [
            "reports/figures/1_demographics_descriptive/",
            "reports/figures/2a_multiple_choice/",
            "reports/figures/2b_freetext/",
            "reports/figures/3_advanced_grouping_correlation/",
            "reports/free_text/",
        ],
    },
]


# ══════════════════════════════════════════════════════════════
# HÀM THỰC THI NOTEBOOK
# ══════════════════════════════════════════════════════════════

def print_header(text, char="═", width=60):
    """In header đẹp."""
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}")


def print_step(icon, text):
    """In bước thực thi."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"  [{timestamp}] {icon} {text}")


def execute_notebook(notebook_name, base_dir):
    """
    Thực thi 1 notebook bằng nbconvert (ExecutePreprocessor).
    
    Sử dụng subprocess để gọi:
        python -m jupyter nbconvert --to notebook --execute <file>
    
    Returns:
        (success: bool, elapsed_seconds: float, error_msg: str)
    """
    notebook_path = base_dir / notebook_name
    executed_dir = base_dir / "reports" / "executed_notebooks"
    executed_dir.mkdir(parents=True, exist_ok=True)
    
    if not notebook_path.exists():
        return False, 0.0, f"File không tồn tại: {notebook_path}"
    
    cmd = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--output-dir", str(executed_dir),
        "--output", notebook_path.name,
        "--ExecutePreprocessor.timeout=600",    # Timeout 10 phút/cell
        "--ExecutePreprocessor.kernel_name=python3",
        f"--ExecutePreprocessor.cwd={base_dir}",
        str(notebook_path),
    ]
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(base_dir),
            timeout=1200,  # Timeout tổng 20 phút/notebook
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            return True, elapsed, ""
        else:
            # Trích xuất dòng lỗi quan trọng nhất
            stderr = result.stderr.strip()
            # Lọc lấy dòng cuối cùng chứa Error
            error_lines = [
                line for line in stderr.split("\n")
                if "Error" in line or "Exception" in line
            ]
            short_error = error_lines[-1] if error_lines else stderr[-500:]
            return False, elapsed, short_error
            
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        return False, elapsed, "TIMEOUT: TIMEOUT: Notebook chạy quá 20 phút!"
    except Exception as e:
        elapsed = time.time() - start_time
        return False, elapsed, f"Exception: {str(e)}"


def verify_outputs(expected_outputs, base_dir):
    """Kiểm tra các file output có tồn tại sau khi chạy."""
    missing = []
    for output in expected_outputs:
        path = base_dir / output
        if output.endswith("/"):
            # Kiểm tra thư mục
            if not path.is_dir():
                missing.append(output)
            elif not any(path.iterdir()):
                missing.append(f"{output} (thư mục rỗng)")
        else:
            if not path.exists():
                missing.append(output)
            elif path.stat().st_size == 0:
                missing.append(f"{output} (file rỗng!)")
    return missing


# ══════════════════════════════════════════════════════════════
# MAIN — NHẠC TRƯỞNG ĐIỀU PHỐI
# ══════════════════════════════════════════════════════════════

def main():
    """Chạy toàn bộ pipeline tuần tự."""
    
    pipeline_start = time.time()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print_header(f" MASTER PIPELINE — BẮT ĐẦU CHẠY  ({now_str})")
    print(f"   Working directory: {BASE_DIR}")
    
    total_notebooks = sum(len(tier["notebooks"]) for tier in PIPELINE)
    print(f"   Tổng notebooks: {total_notebooks}")
    print(f"   Tổng tầng: {len(PIPELINE)}")
    
    # ── Tracking ──
    results = []          # [(notebook, success, elapsed)]
    current_nb = 0        # Đếm notebook hiện tại
    
    for tier in PIPELINE:
        tier_name = tier["tier"]
        tier_desc = tier["name"]
        tier_icon = tier["icon"]
        notebooks = tier["notebooks"]
        expected = tier["expected_outputs"]
        
        print_header(f"{tier_icon}  {tier_name}: {tier_desc}", char="─")
        
        tier_start = time.time()
        tier_success = True
        
        for nb in notebooks:
            current_nb += 1
            progress = f"[{current_nb}/{total_notebooks}]"
            
            print_step("", f"{progress} Đang chạy: {nb} ...")
            
            success, elapsed, error = execute_notebook(nb, BASE_DIR)
            results.append((nb, success, elapsed))
            
            if success:
                print_step("[OK]", f"{progress} Thành công: {nb}  ({elapsed:.1f}s)")
            else:
                print_step("[ERROR]", f"{progress} THẤT BẠI: {nb}  ({elapsed:.1f}s)")
                print(f"\n{'!'*60}")
                print(f"  [ERROR] LỖI TẠI: {nb}")
                print(f"   Chi tiết: {error}")
                print(f"{'!'*60}")
                
                # DỪNG PIPELINE NGAY LẬP TỨC
                print(f"\n  [STOP] PIPELINE DỪNG LẠI — Không chạy tiếp các notebook sau.")
                print(f"  Note: Hãy mở {nb} trong Jupyter để debug lỗi, rồi chạy lại pipeline.")
                
                _print_summary(results, pipeline_start, success=False, stopped_at=nb)
                sys.exit(1)
        
        # ── Verify outputs sau mỗi tầng ──
        tier_elapsed = time.time() - tier_start
        missing = verify_outputs(expected, BASE_DIR)
        
        if missing:
            print_step("[WARN]", f"Thiếu output: {', '.join(missing)}")
            print(f"\n  [STOP] PIPELINE DỪNG — Output của {tier_name} không đầy đủ.")
            _print_summary(results, pipeline_start, success=False, stopped_at=tier_name)
            sys.exit(1)
        else:
            print_step("[OK]", f"{tier_name} hoàn tất ({tier_elapsed:.1f}s) — Output verified OK")
    
    # ── Thành công toàn bộ ──
    _print_summary(results, pipeline_start, success=True)


def _print_summary(results, pipeline_start, success, stopped_at=None):
    """In báo cáo tổng kết."""
    
    total_elapsed = time.time() - pipeline_start
    
    status = "[OK] THÀNH CÔNG" if success else "[ERROR] THẤT BẠI"
    
    print_header(f" BÁO CÁO PIPELINE — {status}")
    
    # Bảng kết quả
    print(f"\n  {'Notebook':<42} {'Trạng thái':<12} {'Thời gian':>10}")
    print(f"  {'─'*42} {'─'*12} {'─'*10}")
    
    for nb, ok, elapsed in results:
        icon = "[OK]" if ok else "[ERROR]"
        status_text = "OK" if ok else "FAILED"
        print(f"  {nb:<42} {icon} {status_text:<9} {elapsed:>8.1f}s")
    
    print(f"  {'─'*66}")
    print(f"  {'TỔNG CỘNG':<42} {'':12} {total_elapsed:>8.1f}s")
    
    # Thống kê
    n_ok = sum(1 for _, ok, _ in results if ok)
    n_fail = sum(1 for _, ok, _ in results if not ok)
    total_nb = sum(len(t["notebooks"]) for t in PIPELINE)
    n_skip = total_nb - len(results)
    
    print(f"\n   Thống kê:")
    print(f"     [OK] Thành công:  {n_ok}")
    print(f"     [ERROR] Thất bại:   {n_fail}")
    if n_skip > 0:
        print(f"     SKIP:  Bỏ qua:    {n_skip}")
    print(f"       Tổng time:  {total_elapsed:.1f}s ({total_elapsed/60:.1f} phút)")
    
    if success:
        # Đếm biểu đồ output
        output_dir = BASE_DIR / "reports" / "figures"
        if output_dir.is_dir():
            charts = list(output_dir.glob("**/*.png"))
            print(f"\n  Charts: Biểu đồ đã tạo: {len(charts)} file trong reports/figures/")
            for chart in sorted(charts):
                size_kb = chart.stat().st_size / 1024
                print(f"      {chart.name} ({size_kb:.0f} KB)")
        
        print(f"\n  Done: Pipeline hoàn tất thành công!")
    else:
        if stopped_at:
            print(f"\n  [STOP] Dừng tại: {stopped_at}")
        print(f"  Note: Sửa lỗi rồi chạy lại: python run_pipeline.py")


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
