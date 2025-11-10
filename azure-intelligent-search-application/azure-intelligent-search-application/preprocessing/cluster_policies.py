import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from tqdm import tqdm

INPUT_FILE = "data/processed/combined_data.json"
OUTPUT_FILE = "data/processed/combined_clustered.json"
NUM_CLUSTERS = 5  

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Run preprocess_policies.py first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f" Clustered dataset saved to: {path}")

def cluster_policies(policies, num_clusters=NUM_CLUSTERS):
    print(f"Clustering {len(policies)} policies into {num_clusters} groups...")

    
    docs = []
    for doc in tqdm(policies, desc="🔍 Preparing text for clustering"):
        combined_text = " ".join([
            doc.get("policy_name", ""),
            doc.get("summary", ""),
            " ".join(doc.get("highlights", [])),
            " ".join(doc.get("sections", {}).values())
        ])
        docs.append(combined_text)

  
    vectorizer = TfidfVectorizer(stop_words="english", max_features=3000)
    X = vectorizer.fit_transform(docs)

   
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    
    for i, doc in enumerate(policies):
        doc["cluster_id"] = int(labels[i])

    return policies

if __name__ == "__main__":
    data = load_data(INPUT_FILE)
    clustered_data = cluster_policies(data)
    save_data(clustered_data, OUTPUT_FILE)
