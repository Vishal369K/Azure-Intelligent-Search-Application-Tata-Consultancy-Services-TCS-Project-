import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
load_dotenv("C:\\Users\\God\\Desktop\\azure-intelligent-search-application\\azure-intelligent-search-application\\config\\.env")


CLUSTER_TOPICS = {
    0: "Access Control & Authentication",
    1: "Network & Device Security",
    2: "HR and Employee Policies",
    3: "Backup & Data Retention",
    4: "Change & Patch Management"
}


def search_policies(query: str):
    """Search Azure Cognitive Search index and show results with cluster grouping."""
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    admin_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "company-policies-index")

    client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(admin_key)
    )

    if not query.strip():
        query = "*"


    results = client.search(
        search_text=query,
        search_fields=["policy_name", "summary", "category"],
        select=["policy_name", "category", "summary", "cluster_id"],
        scoring_profile="policyTitlePriority", 
        query_type="simple",
        search_mode="all",
        include_total_count=True,
        top=20
    )

    data = []
    for result in results:
        cluster_val = result.get("cluster_id", None)
        topic_name = CLUSTER_TOPICS.get(cluster_val, "General / Misc")

        data.append({
            "policy_name": result.get("policy_name", "N/A"),
            "category": result.get("category", "N/A"),
            "summary": result.get("summary", "No summary available."),
            "cluster_id": cluster_val,
            "topic": topic_name
        })


    data.sort(key=lambda d: query.lower() in d["policy_name"].lower(), reverse=True)

  
    print(f"\nRetrieved {len(data)} relevant results for '{query}'\n")
    for r in data:
        print(f" Policy: {r['policy_name']}")
        print(f" Category: {r['category']}")
        print(f" Topic: {r['topic']} (Cluster {r['cluster_id']})")
        print(f" Summary: {r['summary']}")
        print("-" * 70)

    return data



if __name__ == "__main__":
    query = input("Enter your search query: ").strip()
    search_policies(query)
