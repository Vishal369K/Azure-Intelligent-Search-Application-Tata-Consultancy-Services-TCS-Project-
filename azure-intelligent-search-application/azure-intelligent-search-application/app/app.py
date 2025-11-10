from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv("C:\\Users\\God\\Desktop\\azure-intelligent-search-application\\azure-intelligent-search-application\\config\\.env")

app = Flask(__name__, template_folder="templates", static_folder="static")

ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "company-policies-index")

if not ENDPOINT or not ADMIN_KEY:
    raise EnvironmentError("AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_ADMIN_KEY must be set in .env")

search_client = SearchClient(
    endpoint=ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(ADMIN_KEY)
)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/search", methods=["POST"])
def api_search():
    try:
        data = request.get_json() or {}
        query = data.get("q", "").strip()
        top = int(data.get("top", 10))

        if not query:
            return jsonify({"error": "Empty query"}), 400

        results = search_client.search(
            search_text=query,
            top=top,
            query_type="simple",
            search_mode="all",  
            scoring_profile="policyTitlePriority",
            select=[
                "policy_name", "summary", "category", "highlights",
                "sections/purpose", "sections/scope", "sections/policy"
            ]
        )
        
        docs = []
        for r in results:
            sections = r.get("sections", {}) or {}
            docs.append({
                "policy_name": r.get("policy_name", "N/A"),
                "category": r.get("category", "N/A"),
                "summary": r.get("summary", "No summary available."),
                "highlights": r.get("highlights", []),
                "purpose": sections.get("purpose", ""),
                "scope": sections.get("scope", ""),
                "policy": sections.get("policy", "")
            })
        
        docs.sort(key=lambda d: query.lower() in d["policy_name"].lower(), reverse=True)
        
        return jsonify({
            "docs": docs,
            "answers": []
        })


    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
