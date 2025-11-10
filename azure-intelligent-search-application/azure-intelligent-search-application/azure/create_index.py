import os
import logging
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    ComplexField,
    ScoringProfile,
    TextWeights
)


load_dotenv("C:\\Users\\God\\Desktop\\azure-intelligent-search-application\\azure-intelligent-search-application\\config\\.env")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_index():
    try:
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        admin_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "company-policies-index")

        client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(admin_key))

        
        fields = [
            SimpleField(name="policy_id", type="Edm.String", key=True, filterable=True),
            SearchableField(name="policy_name", type="Edm.String", searchable=True, sortable=True),
            SearchableField(name="category", type="Edm.String", searchable=True, filterable=True),
            SearchableField(name="summary", type="Edm.String", searchable=True),
            SearchableField(name="highlights", type="Edm.String", searchable=True, collection=True),
        
            ComplexField(
                name="sections",
                fields=[
                    SearchableField(name="purpose", type="Edm.String", searchable=True),
                    SearchableField(name="scope", type="Edm.String", searchable=True),
                    SearchableField(name="policy", type="Edm.String", searchable=True),
                ]
            ),
        
            SimpleField(name="cluster_id", type="Edm.Int32", filterable=True, sortable=True),
        ]


        
        scoring_profiles = [
            ScoringProfile(
                name="policyTitlePriority",
                text_weights=TextWeights(
                    weights={
                        "policy_name": 10.0,  
                        "summary": 2.0,
                        "sections/purpose": 1.5,
                        "sections/scope": 1.5,
                        "sections/policy": 1.2,
                        "highlights": 1.0
                    }
                )
            )
        ]

        index = SearchIndex(
            name=index_name,
            fields=fields,
            scoring_profiles=scoring_profiles
        )

        client.create_or_update_index(index)
        logging.info(f"Index '{index_name}' created with purpose, scope, policy and title priority boost.")

    except Exception as e:
        logging.error(f"Error while creating index: {e}")

if __name__ == "__main__":
    create_index()
