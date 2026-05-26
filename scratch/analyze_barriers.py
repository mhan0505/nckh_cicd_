import sys
import pandas as pd
import numpy as np
#
# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

# Read multiple_answers_processed.csv
df = pd.read_csv("processed/multiple_answers_processed.csv", encoding="utf-8-sig")
N = len(df)

# Group "Đã dùng CI/CD" vs "Chưa dùng CI/CD"
df["has_used_cicd"] = df["Q7_tools_used"].apply(
    lambda x: 0 if "Chưa từng sử dụng" in str(x) or str(x).strip() == "" or "Không trả lời" in str(x) else 1
)
n_used = df["has_used_cicd"].sum()
n_unused = N - n_used

# Knowing vs Not knowing
df["is_knowing"] = df["Q5_cicd_awareness"].apply(
    lambda x: 1 if x in ["Biết khái niệm cơ bản", "Hiểu rõ và có thể giải thích cho người khác"] else 0
)

print("--- H15: Rào cản theo mức nhận thức ---")
barrier_cols_q34 = [c for c in df.columns if c.startswith("Q34_adoption_barriers__")]
if barrier_cols_q34:
    barrier_names_q34 = [c.replace("Q34_adoption_barriers__", "") for c in barrier_cols_q34]
    
    barriers_low_aware = df[df["is_knowing"] == 0][barrier_cols_q34].mean() * 100
    barriers_high_aware = df[df["is_knowing"] == 1][barrier_cols_q34].mean() * 100
    
    df_barrier_aware = pd.DataFrame({
        "Rào cản": barrier_names_q34,
        "Low_Aware (%)": barriers_low_aware.values,
        "High_Aware (%)": barriers_high_aware.values
    }).sort_values("High_Aware (%)", ascending=False)
    print(df_barrier_aware.to_string(index=False))

print("\n--- H16: Rào cản theo năm học ---")
year_order = ["Năm 1", "Năm 2", "Năm 3", "Năm 4", "Năm 5 hoặc đã tốt nghiệp"]
if barrier_cols_q34:
    barrier_year_data = []
    for yr in year_order:
        subset = df[df["Q2_year"] == yr]
        if len(subset) > 0:
            rates = (subset[barrier_cols_q34].mean() * 100).round(1)
            rates.index = [c.replace("Q34_adoption_barriers__", "") for c in rates.index]
            rates.name = yr
            barrier_year_data.append(rates)
    df_barrier_year = pd.DataFrame(barrier_year_data).T
    print(df_barrier_year.to_string())

print("\n--- H17: Giai đoạn khó nhất của pipeline ---")
diff_cols = [c for c in df.columns if c.startswith("Q33_cicd_difficulties__")]
if diff_cols:
    diff_sums = df[diff_cols].sum().sort_values(ascending=False)
    diff_sums.index = [c.replace("Q33_cicd_difficulties__", "") for c in diff_sums.index]
    for idx, (k, v) in enumerate(diff_sums.items()):
        print(f"{idx+1}. {k}: {v} SV ({v/N*100:.1f}%)")

print("\n--- H18: Kỳ vọng vs thực tế ---")
real_save_time = (df[df["has_used_cicd"] == 1]["Q15_save_time"] >= 4).mean() * 100
real_bug_detect = (df[df["has_used_cicd"] == 1]["Q16_early_bug_detect"] >= 4).mean() * 100
real_confidence = (df[df["has_used_cicd"] == 1]["Q17_job_confidence"] >= 4).mean() * 100

exp_cols_q40 = [c for c in df.columns if c.startswith("Q40_expected_benefit__")]
if exp_cols_q40:
    exp_unused_df = df[df["has_used_cicd"] == 0][exp_cols_q40].mean() * 100
    exp_unused_df.index = [c.replace("Q40_expected_benefit__", "") for c in exp_unused_df.index]
    
    val_exp_time = exp_unused_df.get("Giảm bớt các công việc thủ công lặp đi lặp lại (build, test, deploy)", 0)
    val_exp_bug = exp_unused_df.get("Phát hiện lỗi sớm hơn trong quá trình phát triển phần mềm.", 0)
    val_exp_conf = exp_unused_df.get("Nâng cao kỹ năng DevOps và kinh nghiệm thực tế cho sinh viên.", 0)
    
    print(f"1. Tiết kiệm thời gian / giảm thủ công: Kỳ vọng={val_exp_time:.1f}%, Thực tế={real_save_time:.1f}%")
    print(f"2. Phát hiện lỗi sớm: Kỳ vọng={val_exp_bug:.1f}%, Thực tế={real_bug_detect:.1f}%")
    print(f"3. Tăng tự tin nghề nghiệp: Kỳ vọng={val_exp_conf:.1f}%, Thực tế={real_confidence:.1f}%")
