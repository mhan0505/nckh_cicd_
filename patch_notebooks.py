import json
from pathlib import Path

base_dir = Path(".")

# 📋 1. PATCH 2a_preliminary_analysis.ipynb (output -> output/1_demographics_descriptive)
notebook_2a = base_dir / "2a_preliminary_analysis.ipynb"
if notebook_2a.exists():
    with open(notebook_2a, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for cell in data.get("cells", []):
        if cell.get("cell_type") in ["code", "markdown"]:
            source = cell.get("source", [])
            for i, line in enumerate(source):
                if '1_demographics_descriptive' in line:
                    continue
                line = line.replace('os.makedirs("output", exist_ok=True)', 'os.makedirs("output/1_demographics_descriptive", exist_ok=True)')
                line = line.replace('f"output/{filename}"', 'f"output/1_demographics_descriptive/{filename}"')
                line = line.replace('"output/{filename}"', '"output/1_demographics_descriptive/{filename}"')
                line = line.replace('f"output/{f}"', 'f"output/1_demographics_descriptive/{f}"')
                line = line.replace('\'output/{f}\'', '\'output/1_demographics_descriptive/{f}\'')
                line = line.replace('os.listdir("output")', 'os.listdir("output/1_demographics_descriptive")')
                line = line.replace('Saved: output/', 'Saved: output/1_demographics_descriptive/')
                line = line.replace('Thư mục: output/', 'Thư mục: output/1_demographics_descriptive/')
                line = line.replace('`output/`', '`output/1_demographics_descriptive/`')
                source[i] = line
            cell["source"] = source
            
    with open(notebook_2a, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("SUCCESS: Patched 2a_preliminary_analysis.ipynb")

# 📋 2. PATCH 2b_multiple_answer_analysis.ipynb (output -> output/2_multiple_answers_freetext)
notebook_2b = base_dir / "2b_multiple_answer_analysis.ipynb"
if notebook_2b.exists():
    with open(notebook_2b, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for cell in data.get("cells", []):
        if cell.get("cell_type") in ["code", "markdown"]:
            source = cell.get("source", [])
            for i, line in enumerate(source):
                if '2_multiple_answers_freetext' in line:
                    continue
                line = line.replace('os.makedirs("output", exist_ok=True)', 'os.makedirs("output/2_multiple_answers_freetext", exist_ok=True)')
                line = line.replace('f"output/{filename}"', 'f"output/2_multiple_answers_freetext/{filename}"')
                line = line.replace('"output/{filename}"', '"output/2_multiple_answers_freetext/{filename}"')
                line = line.replace('f"output/{f}"', 'f"output/2_multiple_answers_freetext/{f}"')
                line = line.replace('\'output/{f}\'', '\'output/2_multiple_answers_freetext/{f}\'')
                line = line.replace('os.listdir("output")', 'os.listdir("output/2_multiple_answers_freetext")')
                line = line.replace('Saved: output/', 'Saved: output/2_multiple_answers_freetext/')
                line = line.replace('Thư mục: output/', 'Thư mục: output/2_multiple_answers_freetext/')
                line = line.replace('`output/`', '`output/2_multiple_answers_freetext/`')
                source[i] = line
            cell["source"] = source
            
    with open(notebook_2b, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("SUCCESS: Patched 2b_multiple_answer_analysis.ipynb")

# 📋 3. PATCH 2c_free_text_analysis.ipynb (output -> output/2_multiple_answers_freetext)
notebook_2c = base_dir / "2c_free_text_analysis.ipynb"
if notebook_2c.exists():
    with open(notebook_2c, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for cell in data.get("cells", []):
        if cell.get("cell_type") in ["code", "markdown"]:
            source = cell.get("source", [])
            for i, line in enumerate(source):
                if '2_multiple_answers_freetext' in line:
                    continue
                line = line.replace('os.makedirs("output", exist_ok=True)', 'os.makedirs("output/2_multiple_answers_freetext", exist_ok=True)')
                line = line.replace('f"output/{filename}"', 'f"output/2_multiple_answers_freetext/{filename}"')
                line = line.replace('"output/{filename}"', '"output/2_multiple_answers_freetext/{filename}"')
                line = line.replace('f"output/{f}"', 'f"output/2_multiple_answers_freetext/{f}"')
                line = line.replace('\'output/{f}\'', '\'output/2_multiple_answers_freetext/{f}\'')
                line = line.replace('os.listdir("output")', 'os.listdir("output/2_multiple_answers_freetext")')
                line = line.replace('Saved: output/', 'Saved: output/2_multiple_answers_freetext/')
                line = line.replace('Thư mục: output/', 'Thư mục: output/2_multiple_answers_freetext/')
                line = line.replace('`output/`', '`output/2_multiple_answers_freetext/`')
                
                # Special cases in 2c
                line = line.replace('"output/freetext_tags_by_question.png"', '"output/2_multiple_answers_freetext/freetext_tags_by_question.png"')
                line = line.replace('output/freetext_tags_by_question.png', 'output/2_multiple_answers_freetext/freetext_tags_by_question.png')
                
                source[i] = line
            cell["source"] = source
            
    with open(notebook_2c, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("SUCCESS: Patched 2c_free_text_analysis.ipynb")
