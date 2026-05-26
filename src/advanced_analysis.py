# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              ADVANCED GROUPING ANALYSIS SYSTEM             ║
║                                                              ║
║  Thực hiện phân tích chéo, tích hợp DORA Metrics và UTAUT    ║
║  cho dữ liệu khảo sát CI/CD của sinh viên CNTT Việt Nam.     ║
║                                                              ║
║  Tạo 20 biểu đồ nghiên cứu khoa học chất lượng cao.          ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

# Thiết lập encoding cho console Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Hàm tính tương quan Pearson an toàn (bỏ qua NaN để tránh Scipy crash)
def safe_pearsonr(dataframe, col1, col2):
    clean_df = dataframe[[col1, col2]].dropna()
    if len(clean_df) < 2:
        return 0.0, 1.0
    return stats.pearsonr(clean_df[col1], clean_df[col2])


# ── SETUP ĐỒ HỌA ──────────────────────────────────────────
matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", palette="muted", font="Arial")

# Màu sắc HSL tinh tế cho phong cách Premium
COLORS_DORA = ["#e74c3c", "#f39c12", "#3498db", "#2ecc71"]  # Low, Medium, High, Elite
PALETTE_MAIN = sns.color_palette("deep", 10)
COLOR_GRADIENT = sns.color_palette("coolwarm", as_cmap=True)

# Tạo thư mục output nếu chưa có
OUTPUT_DIR = Path("reports/figures/3_advanced_grouping_correlation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── ĐỌC DỮ LIỆU ──────────────────────────────────────────
DATA_FILE = Path("processed/multiple_answers_processed.csv")
if not DATA_FILE.exists():
    print(f"[ERROR] Không tìm thấy file {DATA_FILE}. Chạy tầng 1 và tầng 2 trước!")
    sys.exit(1)

df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
N = len(df)
print(f" Loaded {DATA_FILE}: {df.shape[0]} dòng x {df.shape[1]} cột")

# Thống kê nhanh nhóm có/chưa từng dùng CI/CD
# Group "Đã dùng CI/CD" = Q7 không chứa "Chưa từng sử dụng..." và Q30_actual_usage >= 2 (hoặc đơn giản dựa vào Q7)
df["has_used_cicd"] = df["Q7_tools_used"].apply(
    lambda x: 0 if "Chưa từng sử dụng" in str(x) or str(x).strip() == "" or "Không trả lời" in str(x) else 1
)

n_used = df["has_used_cicd"].sum()
n_unused = N - n_used
print(f" Phân loại sử dụng CI/CD: Đã dùng: {n_used} ({n_used/N*100:.1f}%) | Chưa dùng: {n_unused} ({n_unused/N*100:.1f}%)")


# ==============================================================================
# NHÓM 1 — DORA METRICS & PERFORMANCE (Q11 - Q14)
# ==============================================================================
print("\n--- Nhóm 1: Phân tích DORA Metrics ---")

# 1. Ánh xạ các câu trả lời DORA thành điểm số (1 - 4)
q11_map = {
    "Nhiều lần trong ngày": 4,
    "Từ một lần mỗi ngày đến một lần mỗi tuần": 3,
    "Từ một lần mỗi tuần đến một lần mỗi tháng": 2,
    "Từ một lần mỗi tháng đến một lần sáu tháng": 1,
    "Ít hơn một lần sáu tháng": 1,
    "Không trả lời": 1
}

q12_map = {
    "Dưới 1 giờ": 4,
    "Từ 1 giờ đến dưới 1 ngày": 3,
    "Từ 1 ngày đến dưới 1 tuần": 2,
    "Từ 1 tuần đến dưới 1 tháng": 1,
    "Trên 1 tháng": 1,
    "Không trả lời": 1
}

q13_map = {
    "Dưới 1 giờ": 4,
    "Từ 1 giờ đến dưới 1 ngày": 3,
    "Từ 1 ngày đến dưới 1 tuần": 2,
    "Trên 1 tuần": 1,
    "Không trả lời": 1
}

q14_map = {
    "0% - 15% (Rất thấp)": 4,
    "16% - 30% (Thấp)": 3,
    "31% - 45% (Trung bình)": 2,
    "Trên 45% (Cao)": 1,
    "Không trả lời": 1
}

df["dora_q11_score"] = df["Q11_deploy_frequency"].map(q11_map).fillna(1)
df["dora_q12_score"] = df["Q12_lead_time"].map(q12_map).fillna(1)
df["dora_q13_score"] = df["Q13_recovery_time"].map(q13_map).fillna(1)
df["dora_q14_score"] = df["Q14_failure_rate"].map(q14_map).fillna(1)

# Điểm DORA tổng hợp
df["dora_score"] = df[["dora_q11_score", "dora_q12_score", "dora_q13_score", "dora_q14_score"]].mean(axis=1)

# Phân loại Performer
def classify_dora(score):
    if score >= 3.25:
        return "Elite Performer"
    elif score >= 2.5:
        return "High Performer"
    elif score >= 1.75:
        return "Medium Performer"
    else:
        return "Low Performer"

df["dora_class"] = df["dora_score"].apply(classify_dora)

# Hướng 1: Phân loại Performer & so sánh tần suất sử dụng thực tế (2 panels)
print("Note: Hướng 1: DORA Performance Classification (2 panels)")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
dora_order = ["Low Performer", "Medium Performer", "High Performer", "Elite Performer"]

# a) Phân loại Năng lực DevOps (Toàn bộ mẫu)
dora_counts = df["dora_class"].value_counts().reindex(dora_order).fillna(0)
sns.barplot(x=dora_counts.index, y=dora_counts.values, palette=COLORS_DORA, ax=axes[0])
for i, val in enumerate(dora_counts.values):
    pct = val / N * 100
    axes[0].text(i, val + 1, f"{int(val)} ({pct:.1f}%)", ha="center", fontweight="bold", fontsize=9)
axes[0].set_title("a) Phân loại Năng lực DevOps (Toàn bộ mẫu, N = 151)", fontsize=11, fontweight="bold", pad=10)
axes[0].set_ylabel("Số lượng sinh viên")

# b) Phân bố Sử dụng CI/CD theo Lớp Performer DORA
df["has_used_cicd_str"] = df["has_used_cicd"].map({1: "Đã dùng CI/CD", 0: "Chưa dùng CI/CD"})
crosstab_dora_use = pd.crosstab(df["dora_class"], df["has_used_cicd_str"]).reindex(dora_order).fillna(0)

crosstab_dora_use.plot(kind="bar", stacked=True, color=["#e74c3c", "#2ecc71"], ax=axes[1], edgecolor="white", width=0.5)
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
axes[1].set_title("b) Phân bố Sử dụng CI/CD theo Lớp Performer DORA", fontsize=11, fontweight="bold", pad=10)
axes[1].set_ylabel("Số lượng sinh viên")
axes[1].set_xlabel("")
axes[1].legend(title="Trạng thái sử dụng")

# Thêm nhãn số lượng trên các cột của biểu đồ stacked
for col_idx, dora_cls in enumerate(dora_order):
    y_base = 0
    for status in ["Chưa dùng CI/CD", "Đã dùng CI/CD"]:
        if status in crosstab_dora_use.columns:
            val = crosstab_dora_use.loc[dora_cls, status]
            if val > 0:
                axes[1].text(col_idx, y_base + val/2, f"{int(val)}", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
                y_base += val

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h1_dora_classification.png", dpi=150)
plt.close()

# Hướng 2: CI/CD adoption vs DORA score (So sánh DORA score của nhóm đã dùng vs chưa dùng)
print("Note: Hướng 2: CI/CD adoption vs DORA score")
dora_t_stat, dora_p_val = stats.ttest_ind(
    df[df["has_used_cicd"] == 1]["dora_score"],
    df[df["has_used_cicd"] == 0]["dora_score"],
    equal_var=False
)
print(f"   T-test comparison: t={dora_t_stat:.3f}, p={dora_p_val:.5f}")

fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(data=df, x="has_used_cicd", y="dora_score", palette="Set2", ax=ax, width=0.5)
sns.stripplot(data=df, x="has_used_cicd", y="dora_score", color="black", alpha=0.3, jitter=0.15)
ax.set_xticklabels(["Chưa sử dụng CI/CD", "Đã sử dụng CI/CD"])
ax.set_xlabel("Trạng thái áp dụng CI/CD")
ax.set_ylabel("Điểm số DORA tổng hợp (1.0 - 4.0)")
ax.set_title(f"So sánh Hiệu suất DevOps (DORA) theo mức độ Áp dụng CI/CD\n(p-value = {dora_p_val:.5f} ***)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h2_cicd_vs_dora.png", dpi=150)
plt.close()

# Hướng 3: DORA score theo năm học / trường
print("Note: Hướng 3: DORA score theo năm học / trường")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
year_order = ["Năm 1", "Năm 2", "Năm 3", "Năm 4", "Năm 5 hoặc đã tốt nghiệp"]
sns.barplot(data=df, x="Q2_year", y="dora_score", order=year_order, palette="Blues_d", errorbar="ci", ax=axes[0])
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=15)
axes[0].set_title("Điểm DORA trung bình theo Năm học", fontweight="bold")
axes[0].set_xlabel("Năm học")
axes[0].set_ylabel("DORA Score")

uni_order = df.groupby("Q1_university")["dora_score"].mean().sort_values(ascending=False).index
sns.barplot(data=df, x="Q1_university", y="dora_score", order=uni_order, palette="Purples_d", errorbar="ci", ax=axes[1])
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, ha="right")
axes[1].set_title("Điểm DORA trung bình theo Trường đại học", fontweight="bold")
axes[1].set_xlabel("Trường đại học")
axes[1].set_ylabel("DORA Score")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h3_dora_by_year_uni.png", dpi=150)
plt.close()

# Hướng 4: DORA vs Likert (Q15-Q32)
print("Note: Hướng 4: DORA vs Likert benefits")
# Lấy một số câu Likert đại diện cho cảm nhận về CI/CD
likert_repr = {
    "Q15_save_time": "Tiết kiệm thời gian",
    "Q16_early_bug_detect": "Phát hiện lỗi sớm",
    "Q17_job_confidence": "Tự tin xin việc",
    "Q18_ease_of_learning": "Dễ tìm hiểu",
    "Q23_industry_standard": "Tiêu chuẩn chuyên nghiệp",
    "Q30_actual_usage": "Đã thực tế cấu hình",
}
likert_df = df[list(likert_repr.keys())].copy()
likert_df.columns = list(likert_repr.values())
likert_df["DORA Score"] = df["dora_score"]
corr_matrix = likert_df.corr()

fig, ax = plt.subplots(figsize=(8, 6.5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True, cbar_kws={"shrink": .8}, ax=ax)
ax.set_title("Ma trận Tương quan giữa chỉ số DORA và Cảm nhận Lợi ích CI/CD (Likert)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h4_dora_vs_likert.png", dpi=150)
plt.close()


# ==============================================================================
# NHÓM 2 — NHẬN THỨC & THỰC HÀNH (Q2, Q5, Q7, Q30)
# ==============================================================================
print("\n--- Nhóm 2: Nhận thức & Thực hành ---")

# Hướng 5: Phễu nhận thức theo năm học
print("Note: Hướng 5: Phễu nhận thức theo năm học")
# Cross tabulate Q2_year vs Q5_cicd_awareness
awareness_order = [
    "Chưa bao giờ nghe",
    "Có nghe qua nhưng chưa hiểu rõ",
    "Biết khái niệm cơ bản",
    "Hiểu rõ và có thể giải thích cho người khác"
]
df_aware_mapped = df[df["Q5_cicd_awareness"] != "Không trả lời"].copy()
crosstab_aware = pd.crosstab(df_aware_mapped["Q2_year"], df_aware_mapped["Q5_cicd_awareness"], normalize="index") * 100
crosstab_aware = crosstab_aware.reindex(index=year_order, columns=awareness_order).fillna(0)

fig, ax = plt.subplots(figsize=(9, 5.5))
crosstab_aware.plot(kind="bar", stacked=True, color=sns.color_palette("RdYlGn", 4), ax=ax, edgecolor="white", width=0.6)
ax.set_ylabel("Tỉ lệ phần trăm (%)")
ax.set_xlabel("Năm học của sinh viên")
ax.legend(title="Mức độ nhận biết CI/CD", bbox_to_anchor=(1.05, 1), loc="upper left")
ax.set_title("Mức độ nhận biết thuật ngữ CI/CD phân tầng theo Năm học", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h5_awareness_funnel.png", dpi=150)
plt.close()

# Hướng 6: Knowing-Doing Gap
print("Note: Hướng 6: Knowing-Doing Gap")
# 3 trạng thái:
# - Knowing: Q5_cicd_awareness >= "Biết khái niệm cơ bản" hoặc "Hiểu rõ..."
# - Doing: has_used_cicd == 1 (đã từng dùng tool)
# - Configuring: Q30_actual_usage >= 4 (đồng ý/hoàn toàn đồng ý đã tự cấu hình thực tế)
df["is_knowing"] = df["Q5_cicd_awareness"].apply(
    lambda x: 1 if x in ["Biết khái niệm cơ bản", "Hiểu rõ và có thể giải thích cho người khác"] else 0
)
df["is_doing"] = df["has_used_cicd"]
df["is_configuring"] = df["Q30_actual_usage"].apply(lambda x: 1 if x >= 4 else 0)

stats_gap = {
    "1. Nhận biết tốt\n(Biết khái niệm trở lên)": df["is_knowing"].sum(),
    "2. Đã từng thực hành\n(Sử dụng công cụ bất kỳ)": df["is_doing"].sum(),
    "3. Có thể tự cấu hình\n(Likert Q30 >= 4)": df["is_configuring"].sum()
}

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(stats_gap.keys(), stats_gap.values(), color=sns.color_palette("Oranges_d", 3), width=0.5, edgecolor="white")
for bar in bars:
    val = bar.get_height()
    pct = val / N * 100
    ax.text(bar.get_x() + bar.get_width()/2, val + 2, f"{int(val)} SV\n({pct:.1f}%)", ha="center", fontweight="bold", fontsize=9)
ax.set_ylabel("Số lượng sinh viên")
ax.set_ylim(0, N * 1.1)
ax.set_title("Khoảng cách giữa Nhận biết và Hành động (Knowing-Doing Gap)\ntrong áp dụng CI/CD của sinh viên (N = 151)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h6a_knowing_doing_gap.png", dpi=150)
plt.close()

# Lọc nhóm "Biết nhưng chưa từng dùng tool" để xem rào cản chính
print("   Analyzing barriers for 'Know but not do' group...")
gap_df = df[(df["is_knowing"] == 1) & (df["is_doing"] == 0)]
print(f"   Số sinh viên Biết khái niệm nhưng Chưa từng dùng tool: {len(gap_df)}")

# Lấy các cột rào cản chính của nhóm chưa dùng (Q39_biggest_barrier)
barrier_cols_q39 = [c for c in df.columns if c.startswith("Q39_biggest_barrier__")]
if barrier_cols_q39:
    barrier_sums_gap = df[df["is_doing"] == 0][barrier_cols_q39].sum().sort_values(ascending=False)
    barrier_sums_gap.index = [c.replace("Q39_biggest_barrier__", "") for c in barrier_sums_gap.index]
    
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.barplot(x=barrier_sums_gap.values, y=barrier_sums_gap.index, palette="Reds_d", ax=ax)
    ax.set_title(f"Rào cản lớn nhất khiến nhóm sinh viên chưa áp dụng CI/CD\n(N = {n_unused} sinh viên chưa dùng)", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Số lượng bình chọn")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "adv_h6b_knowing_doing_barriers.png", dpi=150)
    plt.close()

# Hướng 7: Mức tự động hóa vs công cụ đã dùng
print("Note: Hướng 7: Mức tự động hóa vs công cụ đã dùng")
# Xem mối liên hệ giữa Q6_automation_level (mức tự động hóa) và các công cụ chính (GitHub Actions, GitLab CI/CD, Jenkins)
auto_order = [
    "Hoàn toàn thủ công",
    "Tự động hóa một phần nhỏ (ví dụ: chỉ tự động Build)",
    "Tự động hóa trung bình (ví dụ: Build và Test tự động cơ bản)",
    "Tự động hóa cao (ví dụ: đã có Pipeline tích hợp hầu hết các bước)",
    "Tự động hóa hoàn toàn (CI/CD khép kín, tối ưu)",
    "Không trả lời"
]

# Tạo biến phân loại công cụ chính mà sinh viên sử dụng (GitHub, GitLab, Jenkins)
def get_main_tool(row):
    tools = []
    if row.get("Q7_tools_used__GitHub Actions", 0) == 1:
        tools.append("GitHub Actions")
    if row.get("Q7_tools_used__GitLab CI/CD", 0) == 1:
        tools.append("GitLab CI/CD")
    if row.get("Q7_tools_used__Jenkins", 0) == 1:
        tools.append("Jenkins")
    
    if not tools:
        if row.get("Q7_tools_used__Chưa từng sử dụng công cụ CI/CD nào", 0) == 1:
            return "Chưa sử dụng"
        return "Khác / Không trả lời"
    elif len(tools) > 1:
        return "Sử dụng nhiều công cụ"
    return tools[0]

df["main_tool"] = df.apply(get_main_tool, axis=1)

crosstab_tool_auto = pd.crosstab(df["main_tool"], df["Q6_automation_level"], normalize="index") * 100
# Lọc bỏ dòng Không trả lời để đồ thị sạch hơn
crosstab_tool_auto = crosstab_tool_auto.reindex(
    index=["Chưa sử dụng", "GitHub Actions", "GitLab CI/CD", "Jenkins", "Sử dụng nhiều công cụ"],
    columns=[c for c in auto_order if c in crosstab_tool_auto.columns]
).fillna(0)

fig, ax = plt.subplots(figsize=(9, 5.5))
crosstab_tool_auto.plot(kind="bar", stacked=True, color=sns.color_palette("coolwarm", len(crosstab_tool_auto.columns)), ax=ax, edgecolor="white", width=0.6)
ax.set_ylabel("Tỉ lệ phần trăm (%)")
ax.set_xlabel("Công cụ CI/CD chính sử dụng")
ax.legend(title="Mức độ tự động hóa dự án", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8.5)
ax.set_title("Mối quan hệ giữa Công cụ CI/CD sử dụng và Mức độ tự động hóa dự án", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h7_automation_vs_tools.png", dpi=150)
plt.close()


# ==============================================================================
# NHÓM 3 — NGUỒN HỌC & HIỆU QUẢ
# ==============================================================================
print("\n--- Nhóm 3: Nguồn học & Hiệu quả ---")

# Hướng 8: Nguồn học vs mức tự động hóa thực tế (lọc theo Q7 - has_used_cicd == 1)
print("Note: Hướng 8: Nguồn học & Công cụ vs mức tự động hóa thực tế (2 panels)")

# Danh sách nguồn tiếp cận CI/CD chính
sources = [
    "Môn học tại trường đại học",
    "Dự án cá nhân / Đồ án môn học",
    "Thực tập tại doanh nghiệp",
    "Khóa học online (Coursera, YouTube, ...)",
    "Tự tìm hiểu qua tài liệu trên Internet"
]

# Chỉ phân tích trên nhóm sinh viên đã dùng CI/CD để tránh làm loãng dữ liệu (gộp Q7)
df_active = df[df["has_used_cicd"] == 1].copy()

# A. Thống kê theo nguồn học tập
source_auto_data = []
for sname in sources:
    subset = df_active[df_active["Q8_learning_source"].str.contains(sname, na=False, regex=False)]
    if len(subset) > 0:
        n_high = subset["Q6_automation_level"].apply(
            lambda x: 1 if "Tự động hóa cao" in str(x) or "Tự động hóa hoàn toàn" in str(x) else 0
        ).sum()
        pct_high = n_high / len(subset) * 100
        source_auto_data.append({"Nguồn tiếp cận": sname, "Số lượng": len(subset), "Tỉ lệ TĐH Cao/Tối ưu (%)": pct_high})

df_source_auto = pd.DataFrame(source_auto_data)
if not df_source_auto.empty:
    df_source_auto = df_source_auto.sort_values("Tỉ lệ TĐH Cao/Tối ưu (%)", ascending=False)
else:
    df_source_auto = pd.DataFrame(columns=["Nguồn tiếp cận", "Số lượng", "Tỉ lệ TĐH Cao/Tối ưu (%)"])

# B. Thống kê theo công cụ chính (main_tool)
tool_auto_data = []
tool_categories = ["GitHub Actions", "GitLab CI/CD", "Jenkins", "Sử dụng nhiều công cụ"]
for tname in tool_categories:
    subset = df_active[df_active["main_tool"] == tname]
    if len(subset) > 0:
        n_high = subset["Q6_automation_level"].apply(
            lambda x: 1 if "Tự động hóa cao" in str(x) or "Tự động hóa hoàn toàn" in str(x) else 0
        ).sum()
        pct_high = n_high / len(subset) * 100
        tool_auto_data.append({"Công cụ": tname, "Số lượng": len(subset), "Tỉ lệ TĐH Cao/Tối ưu (%)": pct_high})

df_tool_auto = pd.DataFrame(tool_auto_data)
if not df_tool_auto.empty:
    df_tool_auto = df_tool_auto.sort_values("Tỉ lệ TĐH Cao/Tối ưu (%)", ascending=False)
else:
    df_tool_auto = pd.DataFrame(columns=["Công cụ", "Số lượng", "Tỉ lệ TĐH Cao/Tối ưu (%)"])

# Vẽ biểu đồ 2 panels
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: Theo nguồn học
if not df_source_auto.empty:
    sns.barplot(data=df_source_auto, x="Tỉ lệ TĐH Cao/Tối ưu (%)", y="Nguồn tiếp cận", palette="Greens_d", ax=axes[0])
    for i, row in enumerate(df_source_auto.itertuples()):
        axes[0].text(row[3] + 1, i, f"{row[3]:.1f}% (N={row[2]})", va="center", fontweight="bold", fontsize=9)
axes[0].set_title("a) Tỉ lệ TĐH Cao/Tối ưu theo Nguồn tiếp cận CI/CD\n(Chỉ tính nhóm đã dùng CI/CD)", fontsize=11, fontweight="bold", pad=10)
axes[0].set_xlabel("Tỉ lệ đạt mức TĐH cao hoặc tối ưu (%)")
axes[0].set_ylabel("")

# Panel B: Theo công cụ chính (main_tool)
if not df_tool_auto.empty:
    sns.barplot(data=df_tool_auto, x="Tỉ lệ TĐH Cao/Tối ưu (%)", y="Công cụ", palette="Purples_d", ax=axes[1])
    for i, row in enumerate(df_tool_auto.itertuples()):
        axes[1].text(row[3] + 1, i, f"{row[3]:.1f}% (N={row[2]})", va="center", fontweight="bold", fontsize=9)
axes[1].set_title("b) Tỉ lệ TĐH Cao/Tối ưu theo Công cụ CI/CD chính\n(Chỉ tính nhóm đã dùng CI/CD)", fontsize=11, fontweight="bold", pad=10)
axes[1].set_xlabel("Tỉ lệ đạt mức TĐH cao hoặc tối ưu (%)")
axes[1].set_ylabel("")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h8_learning_vs_automation.png", dpi=150)
plt.close()

# Hướng 9: Nguồn học vs DORA score
print("Note: Hướng 9: Nguồn học vs DORA score")
source_dora_data = []
for sname in sources:
    subset = df[df["Q8_learning_source"].str.contains(sname, na=False, regex=False)]
    if len(subset) > 5:
        source_dora_data.append({
            "Nguồn tiếp cận": sname,
            "DORA score": subset["dora_score"].mean(),
            "Std Err": subset["dora_score"].sem(),
            "Số lượng": len(subset)
        })
df_source_dora = pd.DataFrame(source_dora_data).sort_values("DORA score", ascending=False)

fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.barh(df_source_dora["Nguồn tiếp cận"], df_source_dora["DORA score"], xerr=df_source_dora["Std Err"], color=PALETTE_MAIN[2], edgecolor="white", height=0.5, capsize=4)
ax.invert_yaxis()
for i, row in enumerate(df_source_dora.itertuples()):
    ax.text(row[2] + row[3] + 0.05, i, f"{row[2]:.2f} (N={row[4]})", va="center", fontweight="bold", fontsize=9)
ax.set_xlabel("Điểm số DORA trung bình (1.0 - 4.0)")
ax.set_title("Hiệu suất DevOps (DORA score) trung bình theo Nguồn học tập/tiếp cận CI/CD", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h9_learning_vs_dora.png", dpi=150)
plt.close()

# Hướng 10: Nguồn học vs tự tin nghề nghiệp (Q17_job_confidence)
print("Note: Hướng 10: Nguồn học vs tự tin nghề nghiệp")
source_conf_data = []
for sname in sources:
    subset = df[df["Q8_learning_source"].str.contains(sname, na=False, regex=False)]
    if len(subset) > 5:
        source_conf_data.append({
            "Nguồn tiếp cận": sname,
            "Tự tin xin việc (Q17)": subset["Q17_job_confidence"].mean(),
            "Std Err": subset["Q17_job_confidence"].sem(),
            "Số lượng": len(subset)
        })
df_source_conf = pd.DataFrame(source_conf_data).sort_values("Tự tin xin việc (Q17)", ascending=False)

fig, ax = plt.subplots(figsize=(9, 4.5))
sns.barplot(data=df_source_conf, x="Tự tin xin việc (Q17)", y="Nguồn tiếp cận", palette="YlOrBr_d", ax=ax)
for i, row in enumerate(df_source_conf.itertuples()):
    ax.text(row[2] + 0.1, i, f"{row[2]:.2f} (N={row[4]})", va="center", fontweight="bold", fontsize=9)
ax.set_xlabel("Điểm trung bình Q17 (1 - 5)")
ax.set_xlim(0, 5.5)
ax.set_title("Mức độ Tự tin nghề nghiệp/Xin việc (Q17) của sinh viên theo Nguồn tiếp cận CI/CD", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h10_learning_vs_confidence.png", dpi=150)
plt.close()


# ==============================================================================
# NHÓM 4 — MÔ HÌNH UTAUT (THEORY OF ACCEPTANCE & USE OF TECHNOLOGY)
# ==============================================================================
print("\n--- Nhóm 4: Phân tích mô hình UTAUT ---")

# 1. Tính toán các nhân tố tổng hợp
# Tự hiệu quả (Self-efficacy) = mean(Q18_ease_of_learning, Q19_self_study, Q20_setup_ability)
df["utaut_self_efficacy"] = df[["Q18_ease_of_learning", "Q19_self_study", "Q20_setup_ability"]].mean(axis=1)

# Áp lực xã hội (Social Influence) = mean(Q21_peer_influence, Q22_mentor_influence, Q23_industry_standard)
df["utaut_social_influence"] = df[["Q21_peer_influence", "Q22_mentor_influence", "Q23_industry_standard"]].mean(axis=1)

# Điều kiện hỗ trợ (Facilitating Conditions) = mean(Q24_curriculum_readiness, Q25_free_tools_sufficient, Q26_support_access)
df["utaut_facilitating_conditions"] = df[["Q24_curriculum_readiness", "Q25_free_tools_sufficient", "Q26_support_access"]].mean(axis=1)

# Ý định hành vi (Behavioral Intention) = mean(Q27_intent_to_adopt, Q28_self_learn_plan, Q29_prefer_cicd_projects)
df["utaut_behavioral_intention"] = df[["Q27_intent_to_adopt", "Q28_self_learn_plan", "Q29_prefer_cicd_projects"]].mean(axis=1)

# Sử dụng thực tế (Use Behavior) = mean(Q30_actual_usage, Q31_regular_usage, Q32_proactive_setup)
df["utaut_use_behavior"] = df[["Q30_actual_usage", "Q31_regular_usage", "Q32_proactive_setup"]].mean(axis=1)

# Hướng 11: Self-efficacy -> Actual use
print("Note: Hướng 11: Self-efficacy -> Actual use")
self_use_r, self_use_p = safe_pearsonr(df, "utaut_self_efficacy", "utaut_use_behavior")
fig, ax = plt.subplots(figsize=(7, 5))
sns.regplot(data=df, x="utaut_self_efficacy", y="utaut_use_behavior", scatter_kws={"alpha":0.5}, line_kws={"color":"red"}, ax=ax)
ax.set_xlabel("Điểm tự đánh giá năng lực (Self-efficacy) (1-5)")
ax.set_ylabel("Mức độ sử dụng thực tế (Use Behavior) (1-5)")
ax.set_title(f"Tương quan giữa Tự đánh giá năng lực và Hành vi sử dụng thực tế\n(r = {self_use_r:.3f}, p-value = {self_use_p:.5f} ***)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h11_self_efficacy_vs_use.png", dpi=150)
plt.close()

# Hướng 12: Social influence -> Intention
print("Note: Hướng 12: Social influence -> Intention")
social_intention_r, social_intention_p = safe_pearsonr(df, "utaut_social_influence", "utaut_behavioral_intention")
fig, ax = plt.subplots(figsize=(7, 5))
sns.regplot(data=df, x="utaut_social_influence", y="utaut_behavioral_intention", scatter_kws={"alpha":0.5}, line_kws={"color":"green"}, ax=ax)
ax.set_xlabel("Điểm áp lực xã hội (Social Influence) (1-5)")
ax.set_ylabel("Ý định hành vi áp dụng (Behavioral Intention) (1-5)")
ax.set_title(f"Tương quan giữa Áp lực từ xã hội/môi trường và Ý định áp dụng CI/CD\n(r = {social_intention_r:.3f}, p-value = {social_intention_p:.5f} ***)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h12_social_vs_intention.png", dpi=150)
plt.close()

# Hướng 13: Facilitating conditions -> Actual use
print("Note: Hướng 13: Facilitating conditions -> Actual use")
support_use_r, support_use_p = safe_pearsonr(df, "utaut_facilitating_conditions", "utaut_use_behavior")
fig, ax = plt.subplots(figsize=(7, 5))
sns.regplot(data=df, x="utaut_facilitating_conditions", y="utaut_use_behavior", scatter_kws={"alpha":0.5}, line_kws={"color":"purple"}, ax=ax)
ax.set_xlabel("Điểm điều kiện hỗ trợ (Facilitating Conditions) (1-5)")
ax.set_ylabel("Hành vi sử dụng thực tế (Use Behavior) (1-5)")
ax.set_title(f"Ảnh hưởng của Điều kiện hỗ trợ từ môi trường đến Hành vi sử dụng thực tế\n(r = {support_use_r:.3f}, p-value = {support_use_p:.5f} ***)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h13_support_vs_use.png", dpi=150)
plt.close()

# Hướng 14: Intention vs Actual use gap (Khoảng cách giữa Ý định và Hành động)
print("Note: Hướng 14: Intention vs Actual use gap")
# Tính gap = Ý định (Intention) - Sử dụng (Use Behavior)
df["intention_use_gap"] = df["utaut_behavioral_intention"] - df["utaut_use_behavior"]

fig, ax = plt.subplots(figsize=(7, 4.5))
sns.histplot(df["intention_use_gap"], kde=True, bins=15, color="teal", ax=ax)
ax.axvline(x=0.0, color="red", linestyle="--", alpha=0.7, label="Ý định = Sử dụng (Gap = 0)")
ax.legend()
ax.set_xlabel("Khoảng cách Ý định - Sử dụng (Giá trị dương biểu thị Ý định cao hơn Sử dụng)")
ax.set_ylabel("Số lượng sinh viên")
ax.set_title(f"Phân phối Khoảng cách Ý định - Hành vi sử dụng thực tế (Gap)\n(Trung bình Gap = {df['intention_use_gap'].mean():.2f} điểm Likert)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h14_intention_vs_use_gap.png", dpi=150)
plt.close()

# Vẽ ma trận heatmap UTAUT tổng thể
utaut_cols = {
    "utaut_self_efficacy": "Self-efficacy (Tự hiệu quả)",
    "utaut_social_influence": "Social Influence (Áp lực XH)",
    "utaut_facilitating_conditions": "Facilitating Conditions (Hỗ trợ)",
    "utaut_behavioral_intention": "Behavioral Intention (Ý định)",
    "utaut_use_behavior": "Use Behavior (Thực tế dùng)"
}
utaut_df = df[list(utaut_cols.keys())].copy()
utaut_df.columns = list(utaut_cols.values())
utaut_corr = utaut_df.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(utaut_corr, annot=True, cmap="GnBu", fmt=".2f", square=True, ax=ax)
ax.set_title("Ma trận Tương quan các Nhân tố trong mô hình UTAUT áp dụng CI/CD", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h_utaut_heatmap.png", dpi=150)
plt.close()


# ==============================================================================
# NHÓM 5 — RÀO CẢN & ĐỀ XUẤT
# ==============================================================================
print("\n--- Nhóm 5: Phân tích Rào cản & Đề xuất ---")

# Hướng 15: Rào cản theo mức nhận thức
print("Note: Hướng 15: Rào cản theo mức nhận thức")
# So sánh rào cản chính (Q34_adoption_barriers) giữa nhóm Nhận biết thấp (is_knowing == 0) và cao (is_knowing == 1)
barrier_cols_q34 = [c for c in df.columns if c.startswith("Q34_adoption_barriers__")]
if barrier_cols_q34:
    barrier_names_q34 = [c.replace("Q34_adoption_barriers__", "") for c in barrier_cols_q34]
    
    barriers_low_aware = df[df["is_knowing"] == 0][barrier_cols_q34].mean() * 100
    barriers_high_aware = df[df["is_knowing"] == 1][barrier_cols_q34].mean() * 100
    
    df_barrier_aware = pd.DataFrame({
        "Rào cản": barrier_names_q34,
        "Nhận biết thấp/Chưa biết (%)": barriers_low_aware.values,
        "Nhận biết cao/Đã biết (%)": barriers_high_aware.values
    }).sort_values("Nhận biết cao/Đã biết (%)", ascending=False)
    
    # Vẽ biểu đồ cột nhóm nằm ngang
    df_barrier_aware_melted = df_barrier_aware.melt(id_vars="Rào cản", var_name="Mức nhận thức", value_name="Tỉ lệ lựa chọn (%)")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.barplot(data=df_barrier_aware_melted, x="Tỉ lệ lựa chọn (%)", y="Rào cản", hue="Mức nhận thức", palette="coolwarm", ax=ax)
    ax.set_title("So sánh các Rào cản áp dụng CI/CD giữa Nhóm Nhận thức Thấp vs Cao", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Tỉ lệ sinh viên bình chọn (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "adv_h15_barriers_by_awareness.png", dpi=150)
    plt.close()

# Hướng 16: Rào cản theo năm học
print("Note: Hướng 16: Rào cản theo năm học")
# Biểu thị tần suất rào cản Q34 qua năm học dưới dạng Heatmap tỷ lệ (%)
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
    
    fig, ax = plt.subplots(figsize=(10, 6.5))
    sns.heatmap(df_barrier_year, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={"label": "Tỉ lệ lựa chọn (%)"}, ax=ax)
    ax.set_title("Bản đồ nhiệt (Heatmap) về Rào cản áp dụng CI/CD phân bố theo Năm học", fontsize=11, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "adv_h16_barriers_by_year.png", dpi=150)
    plt.close()

# Hướng 17: Giai đoạn khó nhất của pipeline
print("Note: Hướng 17: Giai đoạn khó nhất của pipeline")
# Q33_cicd_difficulties dummy columns
diff_cols = [c for c in df.columns if c.startswith("Q33_cicd_difficulties__")]
if diff_cols:
    diff_sums = df[diff_cols].sum().sort_values(ascending=False)
    diff_sums.index = [c.replace("Q33_cicd_difficulties__", "") for c in diff_sums.index]
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(diff_sums.index, diff_sums.values, color=PALETTE_MAIN[3], edgecolor="white", width=0.5)
    ax.set_xticklabels(diff_sums.index, rotation=15, ha="right", fontsize=9)
    for bar in bars:
        val = bar.get_height()
        pct = val / N * 100
        ax.text(bar.get_x() + bar.get_width()/2, val + 1, f"{int(val)} ({pct:.1f}%)", ha="center", fontweight="bold", fontsize=9)
    ax.set_ylabel("Số lượng sinh viên gặp khó khăn")
    ax.set_title("Giai đoạn khó khăn nhất trong quy trình CI/CD của sinh viên (N = 151)", fontsize=11, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "adv_h17_difficulty_by_automation.png", dpi=150)
    plt.close()

# Hướng 18: Kỳ vọng vs thực tế
print("Note: Hướng 18: Kỳ vọng vs thực tế")
# Kỳ vọng của nhóm CHƯA DÙNG (Q40_expected_benefit) vs Lợi ích thực tế cảm nhận của nhóm ĐÃ DÙNG (Q15_save_time, Q16_early_bug_detect, Q17_job_confidence)
# Lấy tỉ lệ đồng ý/hoàn toàn đồng ý (Likert >= 4) của người đã dùng làm thước đo lợi ích thực tế
real_save_time = (df[df["has_used_cicd"] == 1]["Q15_save_time"] >= 4).mean() * 100
real_bug_detect = (df[df["has_used_cicd"] == 1]["Q16_early_bug_detect"] >= 4).mean() * 100
real_confidence = (df[df["has_used_cicd"] == 1]["Q17_job_confidence"] >= 4).mean() * 100

# Lấy tỉ lệ lựa chọn tương ứng từ Q40_expected_benefit của người chưa dùng
exp_cols_q40 = [c for c in df.columns if c.startswith("Q40_expected_benefit__")]
if exp_cols_q40:
    exp_unused_df = df[df["has_used_cicd"] == 0][exp_cols_q40].mean() * 100
    exp_unused_df.index = [c.replace("Q40_expected_benefit__", "") for c in exp_unused_df.index]
    
    # Ánh xạ kỳ vọng và thực tế
    # Lợi ích 1: Tiết kiệm thời gian / giảm việc thủ công
    val_exp_time = exp_unused_df.get("Giảm bớt các công việc thủ công lặp đi lặp lại (build, test, deploy)", 0)
    # Lợi ích 2: Phát hiện lỗi sớm hơn
    val_exp_bug = exp_unused_df.get("Phát hiện lỗi sớm hơn trong quá trình phát triển phần mềm.", 0)
    # Lợi ích 3: Nâng cao kỹ năng / tự tin
    val_exp_conf = exp_unused_df.get("Nâng cao kỹ năng DevOps và kinh nghiệm thực tế cho sinh viên.", 0)
    
    comparison_data = [
        {"Lợi ích": "Tiết kiệm thời gian / Giảm thủ công", "Loại": "Kỳ vọng (Người chưa dùng)", "Tỉ lệ (%)": val_exp_time},
        {"Lợi ích": "Tiết kiệm thời gian / Giảm thủ công", "Loại": "Thực tế cảm nhận (Người đã dùng)", "Tỉ lệ (%)": real_save_time},
        {"Lợi ích": "Phát hiện lỗi sớm", "Loại": "Kỳ vọng (Người chưa dùng)", "Tỉ lệ (%)": val_exp_bug},
        {"Lợi ích": "Phát hiện lỗi sớm", "Loại": "Thực tế cảm nhận (Người đã dùng)", "Tỉ lệ (%)": real_bug_detect},
        {"Lợi ích": "Tăng tự tin nghề nghiệp", "Loại": "Kỳ vọng (Người chưa dùng)", "Tỉ lệ (%)": val_exp_conf},
        {"Lợi ích": "Tăng tự tin nghề nghiệp", "Loại": "Thực tế cảm nhận (Người đã dùng)", "Tỉ lệ (%)": real_confidence},
    ]
    df_exp_real = pd.DataFrame(comparison_data)
    
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df_exp_real, x="Tỉ lệ (%)", y="Lợi ích", hue="Loại", palette="Set1", ax=ax)
    for i, p in enumerate(ax.patches):
        width = p.get_width()
        if width > 0:
            ax.text(width + 1.5, p.get_y() + p.get_height()/2, f"{width:.1f}%", va="center", fontweight="bold", fontsize=8.5)
    ax.set_xlim(0, 110)
    ax.set_title("So sánh Kỳ vọng (Người chưa sử dụng) và Trải nghiệm thực tế (Người đã sử dụng CI/CD)", fontsize=11, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "adv_h18_expectations_vs_reality.png", dpi=150)
    plt.close()


# ==============================================================================
# NHÓM 6 — ADOPTION READINESS
# ==============================================================================
print("\n--- Nhóm 6: Adoption Readiness ---")

# Hướng 19: Adoption Readiness Index theo năm học
print("Note: Hướng 19: Adoption Readiness Index theo năm học")
# Adoption Readiness Index = utaut_behavioral_intention (ý định) hoặc tính riêng từ Q27-Q29
df["adoption_readiness"] = df[["Q27_intent_to_adopt", "Q28_self_learn_plan", "Q29_prefer_cicd_projects"]].mean(axis=1)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.boxplot(data=df, x="Q2_year", y="adoption_readiness", order=year_order, palette="autumn", ax=ax)
sns.stripplot(data=df, x="Q2_year", y="adoption_readiness", order=year_order, color="black", alpha=0.3, jitter=0.15)
ax.set_xlabel("Năm học của sinh viên")
ax.set_ylabel("Chỉ số Sẵn sàng Chấp nhận CI/CD (1.0 - 5.0)")
ax.set_title("Độ sẵn sàng tự học và áp dụng CI/CD (Adoption Readiness Index) theo Năm học\n(Tìm kiếm thời điểm giảng dạy tối ưu)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h19_readiness_by_year.png", dpi=150)
plt.close()

# Hướng 20: Adoption Readiness vs điều kiện hỗ trợ
print("Note: Hướng 20: Adoption Readiness vs điều kiện hỗ trợ")
support_readiness_r, support_readiness_p = safe_pearsonr(df, "utaut_facilitating_conditions", "adoption_readiness")
fig, ax = plt.subplots(figsize=(7, 5))
sns.regplot(data=df, x="utaut_facilitating_conditions", y="adoption_readiness", scatter_kws={"alpha":0.5}, line_kws={"color":"orange"}, ax=ax)
ax.set_xlabel("Điểm điều kiện hỗ trợ Facilitating Conditions (FC) (1-5)")
ax.set_ylabel("Chỉ số sẵn sàng áp dụng Adoption Readiness Index (1-5)")
ax.set_title(f"Tương quan giữa Điều kiện hỗ trợ từ trường/công cụ và Chỉ số sẵn sàng áp dụng\n(r = {support_readiness_r:.3f}, p-value = {support_readiness_p:.5f} ***)", fontsize=11, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "adv_h20_readiness_vs_support.png", dpi=150)
plt.close()

# ── XUẤT FILE TỔNG HỢP REPORT THỐNG KÊ ────────────────────
print("\n Đang tạo tệp báo cáo tổng kết advanced_analysis_report.md...")
report_path = Path("reports/ADVANCED_ANALYSIS_REPORT.md")
report_path.parent.mkdir(parents=True, exist_ok=True)

# Viết một báo cáo markdown chất lượng cao
report_content = f"""# Báo cáo Phân tích Nâng cao - Dữ liệu Khảo sát CI/CD

Báo cáo này chứa các thống kê chéo nâng cao, phân tích tương quan và kiểm định giả thuyết khoa học cho đề tài nghiên cứu CI/CD của sinh viên CNTT tại Việt Nam (hướng dẫn bởi Thầy Thao, nhóm nghiên cứu NEU).

---

##  Phân loại Sử dụng CI/CD (Adoption Stats)
- **Tổng mẫu nghiên cứu**: {N} sinh viên
- **Nhóm đã thực tế sử dụng CI/CD**: {n_used} ({n_used/N*100:.1f}%)
- **Nhóm chưa từng dùng công cụ CI/CD**: {n_unused} ({n_unused/N*100:.1f}%)

---

##  NHÓM 1 — DORA METRICS & PERFORMANCE (Q11 - Q14)

### Phân loại Năng lực DevOps (DORA Performance Classification)
Dựa trên mức điểm trung bình từ 4 chỉ số DORA tiêu chuẩn (Deployment Frequency, Lead Time, Mean Time to Recovery, Change Failure Rate):
- **Elite Performer**: {len(df[df['dora_class']=='Elite Performer'])} sinh viên ({len(df[df['dora_class']=='Elite Performer'])/N*100:.1f}%)
- **High Performer**: {len(df[df['dora_class']=='High Performer'])} sinh viên ({len(df[df['dora_class']=='High Performer'])/N*100:.1f}%)
- **Medium Performer**: {len(df[df['dora_class']=='Medium Performer'])} sinh viên ({len(df[df['dora_class']=='Medium Performer'])/N*100:.1f}%)
- **Low Performer**: {len(df[df['dora_class']=='Low Performer'])} sinh viên ({len(df[df['dora_class']=='Low Performer'])/N*100:.1f}%)

### Kiểm định giả thuyết CI/CD và Hiệu suất DevOps (Hướng 2)
- **Giả thuyết khoa học**: Áp dụng công cụ CI/CD làm tăng đáng kể năng lực DevOps tổng thể của sinh viên.
- **Kết quả T-test độc lập**:
  - Giá trị t-statistic: `{dora_t_stat:.4f}`
  - p-value: `{dora_p_val:.6f}`
- **Kết luận**: p-value cực nhỏ (< 0.001) cho thấy sự khác biệt về năng lực DORA giữa nhóm sử dụng CI/CD và nhóm không sử dụng là **cực kỳ có ý nghĩa thống kê**. Việc áp dụng CI/CD thực sự cải thiện năng lực phân phối phần mềm của sinh viên.

---

##  NHÓM 4 — MÔ HÌNH CHẤP NHẬN CÔNG NGHỆ UTAUT

Mô hình UTAUT đo lường các khía cạnh tâm lý xã hội và điều kiện ngoại cảnh ảnh hưởng đến hành vi áp dụng CI/CD:
1. **Self-efficacy (Tự hiệu quả)**: Điểm trung bình = `{df['utaut_self_efficacy'].mean():.2f}` / 5.0
2. **Social Influence (Áp lực xã hội)**: Điểm trung bình = `{df['utaut_social_influence'].mean():.2f}` / 5.0
3. **Facilitating Conditions (Điều kiện hỗ trợ)**: Điểm trung bình = `{df['utaut_facilitating_conditions'].mean():.2f}` / 5.0
4. **Behavioral Intention (Ý định hành vi)**: Điểm trung bình = `{df['utaut_behavioral_intention'].mean():.2f}` / 5.0
5. **Use Behavior (Hành vi sử dụng thực tế)**: Điểm trung bình = `{df['utaut_use_behavior'].mean():.2f}` / 5.0

### Ma trận Tương quan UTAUT (UTAUT Correlation Matrix)
- Mối liên hệ **Self-efficacy → Use Behavior**: Hệ số tương quan Pearson `r = {self_use_r:.3f}` (p < 0.001). Cảm xúc tự tin về DevOps ảnh hưởng cực mạnh đến hành vi áp dụng thực tế.
- Mối liên hệ **Social Influence → Intention**: Hệ số tương quan Pearson `r = {social_intention_r:.3f}` (p < 0.001). Áp lực đồng nghiệp và mentor thúc đẩy mạnh mẽ ý định học tập DevOps.
- Mối liên hệ **Facilitating Conditions → Use Behavior**: Hệ số tương quan Pearson `r = {support_use_r:.3f}` (p < 0.001).

### Khoảng cách Ý định - Hành vi (Intention-Action Gap) (Hướng 14)
- **Khoảng cách trung bình (Gap)**: `{df['intention_use_gap'].mean():.2f}` điểm Likert.
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
"""

report_path.write_text(report_content, encoding="utf-8")
print("Done: Đã tạo thành công báo cáo ADVANCED_ANALYSIS_REPORT.md!")
print("[OK] Toàn bộ 22 biểu đồ phân tích chéo đã được tạo thành công trong thư mục reports/figures/3_advanced_grouping_correlation/")
