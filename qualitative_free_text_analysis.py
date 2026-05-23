# -*- coding: utf-8 -*-
"""Qualitative analysis for open-ended CI/CD survey responses.

This replaces word clouds with a small-sample qualitative workflow:
noise filtering, theme coding, theme summaries, and representative quotes.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

INPUT_FILE = Path("tagged_free_text.csv")
OUTPUT_DIR = Path("output/2_multiple_answers_freetext")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STALE_PATTERNS = ["wordcloud_*.png", "keywords_*.png", "freetext_tags_*.png"]

QUESTION_GROUPS = {
    "cải thiện nhất ở các công cụ": "Cải thiện công cụ",
    "đề xuất nào để thúc đẩy": "Đề xuất thúc đẩy",
    "trang bị mà sinh viên cần": "Trang bị/kỹ năng cần có",
    "dự định học hoặc áp dụng": "Dự định áp dụng",
    "rào cản lớn nhất": "Rào cản",
    "mong đợi điều gì nhất": "Kỳ vọng",
}

THEME_RULES = [
    {
        "theme": "Tích hợp vào chương trình học",
        "keywords": [
            "môn học",
            "học phần",
            "chương trình",
            "giảng dạy",
            "nhà trường",
            "trường",
            "đại học",
            "curriculum",
        ],
    },
    {
        "theme": "Tăng thực hành/lab/workshop",
        "keywords": [
            "thực hành",
            "lab",
            "workshop",
            "seminar",
            "dự án",
            "project",
            "đồ án",
            "repository mẫu",
            "repo mẫu",
        ],
    },
    {
        "theme": "Tài liệu và hướng dẫn rõ ràng",
        "keywords": [
            "tài liệu",
            "hướng dẫn",
            "guide",
            "mẫu",
            "giới thiệu",
            "thông tin",
            "phổ biến",
            "trao đổi",
        ],
    },
    {
        "theme": "Công cụ CI/CD phổ biến",
        "keywords": [
            "github actions",
            "gitlab",
            "jenkins",
            "circle",
            "travis",
            "pipeline",
            "công cụ",
            "tool",
        ],
    },
    {
        "theme": "Nền tảng kỹ thuật DevOps",
        "keywords": [
            "git",
            "docker",
            "container",
            "test",
            "testing",
            "automated testing",
            "cloud",
            "server",
            "deploy",
            "deployment",
            "network",
            "devops",
            "automation",
        ],
    },
    {
        "theme": "Tư duy quy trình và hình dung pipeline",
        "keywords": [
            "quy trình",
            "luồng",
            "hình dung",
            "pipeline visualization",
            "cấu trúc",
            "sản phẩm",
            "tư duy",
        ],
    },
    {
        "theme": "Môi trường và hạ tầng thực hành",
        "keywords": [
            "môi trường",
            "hạ tầng",
            "server",
            "cloud",
            "docker",
            "vận hành",
        ],
    },
]

INVALID_RESPONSES = {
    "",
    "ko",
    "k",
    "khong",
    "không",
    "không có",
    "khong co",
    "không trả lời",
    "no",
    "none",
    "n/a",
    "na",
    "nhi",
}


def normalize_text(text: object) -> str:
    """Lowercase and strip Vietnamese accents for matching."""
    value = "" if pd.isna(text) else str(text).strip().lower()
    value = unicodedata.normalize("NFD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def is_gibberish(text_norm: str) -> bool:
    if re.fullmatch(r"[a-z]*f[dsa]{4,}[a-z]*", text_norm):
        return True
    if len(set(text_norm.replace(" ", ""))) <= 3 and len(text_norm) >= 5:
        return True
    return False


def question_group(question: str) -> str:
    question_norm = normalize_text(question)
    for phrase, group in QUESTION_GROUPS.items():
        if normalize_text(phrase) in question_norm:
            return group
    return "Câu hỏi mở khác"


def assign_themes(row: pd.Series) -> list[str]:
    combined = " ".join(
        [
            normalize_text(row.get("response_raw", "")),
            normalize_text(row.get("response_clean", "")),
            normalize_text(row.get("tags", "")),
        ]
    )
    themes = []
    for rule in THEME_RULES:
        if any(normalize_text(keyword) in combined for keyword in rule["keywords"]):
            themes.append(rule["theme"])
    return themes or ["Khác/ý kiến chung"]


THEME_KEYWORDS = {
    rule["theme"]: [normalize_text(keyword) for keyword in rule["keywords"]]
    for rule in THEME_RULES
}


def score_theme_quote(row: pd.Series, theme: str) -> float:
    text = str(row.get("response_raw", ""))
    text_norm = normalize_text(text)
    token_count = int(row.get("token_count", 0) or 0)
    theme_count = len(row.get("theme_list", []))
    keyword_hits = sum(1 for keyword in THEME_KEYWORDS.get(theme, []) if keyword in text_norm)
    return keyword_hits * 100 + min(token_count, 30) * 5 + min(len(text), 220) * 0.2 - max(theme_count - 1, 0) * 35


def cleanup_old_outputs() -> None:
    for pattern in STALE_PATTERNS:
        for path in OUTPUT_DIR.glob(pattern):
            path.unlink(missing_ok=True)


def plot_response_quality(df: pd.DataFrame) -> None:
    quality = df["include_in_analysis"].map({True: "Có thể phân tích", False: "Loại khỏi phân tích"})
    counts = quality.value_counts().reindex(["Có thể phân tích", "Loại khỏi phân tích"]).fillna(0)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(counts.index, counts.values, color=["#2f7d59", "#b84a4a"], edgecolor="white")
    for bar in bars:
        val = int(bar.get_height())
        pct = val / len(df) * 100 if len(df) else 0
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.4, f"{val} ({pct:.1f}%)", ha="center", fontweight="bold")
    ax.set_ylabel("Số câu trả lời")
    ax.set_title("Chất lượng câu trả lời mở sau khi lọc nhiễu", fontweight="bold", pad=12)
    sns.despine()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "freetext_response_quality.png", dpi=150)
    plt.close()


def plot_theme_overall(theme_counts: pd.Series, n_valid: int) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    colors = sns.color_palette("crest", len(theme_counts))
    ax.barh(theme_counts.index[::-1], theme_counts.values[::-1], color=colors[::-1], edgecolor="white")
    for i, val in enumerate(theme_counts.values[::-1]):
        pct = val / n_valid * 100 if n_valid else 0
        ax.text(val + 0.2, i, f"{int(val)} ({pct:.1f}%)", va="center", fontweight="bold", fontsize=9)
    ax.set_xlabel("Số câu trả lời có nhắc đến chủ đề")
    ax.set_title(f"Chủ đề chính trong câu trả lời mở hợp lệ (n={n_valid})", fontweight="bold", pad=12)
    ax.set_xlim(0, max(theme_counts.max() * 1.25, 1))
    sns.despine(left=True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "freetext_theme_overall.png", dpi=150)
    plt.close()


def plot_theme_by_group(valid_df: pd.DataFrame) -> None:
    exploded = valid_df.explode("theme_list")
    ct = pd.crosstab(exploded["question_group"], exploded["theme_list"])
    ct = ct.loc[ct.sum(axis=1).sort_values(ascending=False).index]
    ct = ct[ct.sum(axis=0).sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(ct, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, linecolor="white", cbar=False, ax=ax)
    ax.set_xlabel("Chủ đề")
    ax.set_ylabel("Nhóm câu hỏi")
    ax.set_title("Bản đồ chủ đề theo từng nhóm câu hỏi mở", fontweight="bold", pad=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "freetext_theme_by_question_group.png", dpi=150)
    plt.close()

    ct.to_csv(OUTPUT_DIR / "freetext_theme_by_question_group.csv", encoding="utf-8-sig")


def build_theme_summary(valid_df: pd.DataFrame) -> pd.DataFrame:
    exploded = valid_df.explode("theme_list")
    rows = []
    for theme, group in exploded.groupby("theme_list"):
        subset = valid_df[valid_df["theme_list"].apply(lambda themes: theme in themes)].copy()
        subset["quote_score"] = subset.apply(lambda row: score_theme_quote(row, theme), axis=1)
        quote_row = subset.sort_values("quote_score", ascending=False).iloc[0]
        groups = (
            subset["question_group"]
            .value_counts()
            .head(3)
            .index
            .tolist()
        )
        rows.append(
            {
                "theme": theme,
                "mentions": len(subset),
                "share_valid_pct": len(subset) / len(valid_df) * 100 if len(valid_df) else 0,
                "top_question_groups": "; ".join(groups),
                "representative_quote": str(quote_row["response_raw"]).strip(),
            }
        )
    return pd.DataFrame(rows).sort_values(["mentions", "theme"], ascending=[False, True])


def write_markdown_report(df: pd.DataFrame, valid_df: pd.DataFrame, theme_summary: pd.DataFrame) -> None:
    invalid_n = len(df) - len(valid_df)
    lines = [
        "# Phân tích định tính câu hỏi mở",
        "",
        "## Chất lượng dữ liệu",
        f"- Tổng câu trả lời mở: {len(df)}",
        f"- Câu trả lời đủ thông tin để phân tích: {len(valid_df)} ({len(valid_df) / len(df) * 100:.1f}%)",
        f"- Câu trả lời bị loại do quá ngắn/không có nội dung/nhiễu: {invalid_n} ({invalid_n / len(df) * 100:.1f}%)",
        "",
        "## Chủ đề nổi bật",
    ]

    for _, row in theme_summary.iterrows():
        lines.extend(
            [
                f"### {row['theme']}",
                f"- Tần suất: {int(row['mentions'])} câu trả lời hợp lệ ({row['share_valid_pct']:.1f}%).",
                f"- Nhóm câu hỏi xuất hiện nhiều: {row['top_question_groups']}.",
                f"- Trích dẫn tiêu biểu: “{row['representative_quote']}”",
                "",
            ]
        )

    lines.extend(
        [
            "## Cách dùng trong báo cáo",
            "- Không nên dùng wordcloud làm bằng chứng chính vì mẫu nhỏ và nhiều câu trả lời ngắn.",
            "- Nên dùng biểu đồ chủ đề để hỗ trợ các kết quả định lượng về rào cản, kỳ vọng và điều kiện hỗ trợ.",
            "- Nên dùng 2-3 trích dẫn tiêu biểu để minh họa cho nhu cầu thực hành, học phần CI/CD và nền tảng kỹ thuật DevOps.",
            "",
        ]
    )
    (OUTPUT_DIR / "FREETEXT_QUALITATIVE_FINDINGS.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing {INPUT_FILE}. Run 1c_free_text_tagging.ipynb first.")

    cleanup_old_outputs()

    df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")
    df["response_norm"] = df["response_raw"].apply(normalize_text)
    df["question_group"] = df["question"].apply(question_group)
    df["theme_list"] = df.apply(assign_themes, axis=1)
    df["themes"] = df["theme_list"].apply(lambda themes: ", ".join(themes))

    df["include_in_analysis"] = ~df["response_norm"].isin(INVALID_RESPONSES)
    df["include_in_analysis"] &= ~df["response_norm"].apply(is_gibberish)
    df["include_in_analysis"] &= (
        (df["token_count"].fillna(0).astype(int) >= 2)
        | (df["themes"] != "Khác/ý kiến chung")
    )

    valid_df = df[df["include_in_analysis"]].copy()
    theme_counts = valid_df.explode("theme_list")["theme_list"].value_counts()
    theme_summary = build_theme_summary(valid_df)

    df.drop(columns=["theme_list"]).to_csv(OUTPUT_DIR / "freetext_coded_responses.csv", index=False, encoding="utf-8-sig")
    theme_summary.to_csv(OUTPUT_DIR / "freetext_theme_summary.csv", index=False, encoding="utf-8-sig")

    plot_response_quality(df)
    if not valid_df.empty:
        plot_theme_overall(theme_counts, len(valid_df))
        plot_theme_by_group(valid_df)
    write_markdown_report(df, valid_df, theme_summary)

    print(f"OK Qualitative free-text analysis complete: {len(valid_df)}/{len(df)} valid responses")
    print(f"   Saved: {OUTPUT_DIR / 'freetext_response_quality.png'}")
    print(f"   Saved: {OUTPUT_DIR / 'freetext_theme_overall.png'}")
    print(f"   Saved: {OUTPUT_DIR / 'freetext_theme_by_question_group.png'}")
    print(f"   Saved: {OUTPUT_DIR / 'freetext_theme_summary.csv'}")
    print(f"   Saved: {OUTPUT_DIR / 'FREETEXT_QUALITATIVE_FINDINGS.md'}")


if __name__ == "__main__":
    main()
