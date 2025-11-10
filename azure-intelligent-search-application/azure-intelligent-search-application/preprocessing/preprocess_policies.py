import os
import json
import pandas as pd
import numpy as np
from extract_text import extract_docx_text, extract_sections
from clean_data import clean_text, clean_dataframe
from merge_policies import merge_policies

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
OUTPUT_JSON = os.path.join(PROCESSED_DIR, "combined_data.json")

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer)): return int(obj)
        if isinstance(obj, (np.floating)): return float(obj)
        if isinstance(obj, (np.ndarray)): return obj.tolist()
        return super().default(obj)

def run_pipeline():
    print(" Starting preprocessing pipeline...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)

   
    hr_path = os.path.join(RAW_DIR, "HRDataset_v14.csv")
    hr_df = pd.read_csv(hr_path) if os.path.exists(hr_path) else pd.DataFrame()
    if not hr_df.empty:
        hr_df = clean_dataframe(hr_df)
        print(f"Loaded HR dataset with {len(hr_df)} records.")
    else:
        print("No HR dataset found — skipping HR merge.")


    text_data = []
    for file in os.listdir(RAW_DIR):
        if not file.endswith(".docx"):
            continue

        path = os.path.join(RAW_DIR, file)
        print(f"Extracting from: {file}")
        text = extract_docx_text(path)
        text = clean_text(text)
        sections = extract_sections(text)

        text_data.append({
            "policy_name": os.path.splitext(file)[0].replace("_", " ").title(),
            "category": "Information Security" if "security" in file.lower() else "General Policy",
            "summary": sections.get("purpose") or text[:250],
            "sections": sections
        })

   
    print(" Generating structured summaries and highlights...")
    merged = merge_policies(hr_df, text_data)

   
    print(f"Saving to {OUTPUT_JSON} ...")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False, cls=NpEncoder)

    print(f"Done! {len(merged)} policies processed.")
    print(f"Output: {OUTPUT_JSON}")

if __name__ == "__main__":
    run_pipeline()
