import re
import json
import pandas as pd


def clean_name(name):
    if not name:
        return ""
    cleaned = re.sub(r"(?i)\bUnderdefense Maxi\b\s*-\s*", "", name.strip())
    return cleaned.strip()

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def shorten_text(text, max_sentences=3, max_chars=400):
    if not text:
        return ""
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?]) +', text)
    short_text = " ".join(sentences[:max_sentences])
    if len(short_text) > max_chars:
        short_text = short_text[:max_chars].rsplit(" ", 1)[0] + "..."
    return short_text

def extract_highlights(text):
    if not text:
        return []
    text_lower = text.lower()
    highlights = set()

    keyword_map = {
        "encryption": "Encryption and data protection",
        "patch": "Patch management and vulnerability remediation",
        "vulnerability": "Vulnerability management and risk mitigation",
        "backup": "Backup and recovery controls",
        "access": "Access control and authorization",
        "confidential": "Confidential data handling",
        "training": "Employee awareness and security training",
        "awareness": "Security awareness and employee training",
        "review": "Annual ISMS review and approval",
        "incident": "Incident response and escalation",
        "password": "Authentication and password standards",
        "key": "Cryptographic key management procedures",
        "responsibility": "Defined roles and responsibilities"
    }

    for keyword, desc in keyword_map.items():
        if keyword in text_lower:
            highlights.add(desc)

    return list(highlights)

def process_sections(sections_dict):
    processed = {}
    for key, text in sections_dict.items():
        processed[key] = shorten_text(text)
    return processed

def merge_policies(hr_df: pd.DataFrame, text_data: list) -> list:
    merged_data = []

    for item in text_data:
       
        policy_name = clean_name(item.get("policy_name", "Unknown Policy"))
        category = item.get("category", "General Policy")
        summary_text = item.get("summary", "")
        sections = item.get("sections", {})

        cleaned_summary = shorten_text(summary_text)
        processed_sections = process_sections(sections)
        combined_text = " ".join(list(sections.values()) + [summary_text])
        highlights = extract_highlights(combined_text)

        merged_data.append({
            "policy_name": policy_name,
            "category": category,
            "summary": cleaned_summary,
            "highlights": highlights,
            "sections": processed_sections,
            "responsible_hr": {}
        })

    return merged_data
