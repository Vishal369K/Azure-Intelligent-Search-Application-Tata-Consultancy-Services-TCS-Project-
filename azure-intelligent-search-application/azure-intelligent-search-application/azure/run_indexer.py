import os
import logging
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SearchIndexer,
    IndexingSchedule,
    SearchIndexerDataSourceType,
    FieldMappingFunction
)

load_dotenv("C:\\Users\\God\\Desktop\\azure-intelligent-search-application\\azure-intelligent-search-application\\config\\.env")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run_indexer():
    try:
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        admin_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
        storage_connection = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = "policydata"

        data_source_name = "policy-datasource"
        indexer_name = "policy-indexer"
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "company-policies-index")

        client = SearchIndexerClient(endpoint=endpoint, credential=AzureKeyCredential(admin_key))

        container = SearchIndexerDataContainer(name=container_name)
        data_source = SearchIndexerDataSourceConnection(
            name=data_source_name,
            type=SearchIndexerDataSourceType.AZURE_BLOB,
            connection_string=storage_connection,
            container=container,
            description="Blob data source for policy documents"
        )

        data_source.additional_properties = {
            "dataToExtract": "contentAndMetadata",
            "parsingMode": "jsonArray"
        }

        client.create_or_update_data_source_connection(data_source)
        logging.info("Data source created successfully.")

        indexer = SearchIndexer(
            name=indexer_name,
            data_source_name=data_source_name,
            target_index_name=index_name,
            schedule=IndexingSchedule(interval="PT1H"),
            field_mappings=[
                {"sourceFieldName": "policy_name", "targetFieldName": "policy_id",
                 "mappingFunction": FieldMappingFunction(name="base64Encode")},
                {"sourceFieldName": "policy_name", "targetFieldName": "policy_name"},
                {"sourceFieldName": "category", "targetFieldName": "category"},
                {"sourceFieldName": "summary", "targetFieldName": "summary"},
                {"sourceFieldName": "highlights", "targetFieldName": "highlights"},
                {"sourceFieldName": "sections", "targetFieldName": "sections"},
                {"sourceFieldName": "cluster_id", "targetFieldName": "cluster_id"}

            ],
            parameters={
                "configuration": {
                    "dataToExtract": "contentAndMetadata",
                    "parsingMode": "jsonArray"
                }
            }
        )

        client.create_or_update_indexer(indexer)
        logging.info("Indexer created or updated successfully with sections mapping.")
        client.run_indexer(indexer.name)
        logging.info("Indexer triggered successfully.")

    except Exception as e:
        logging.error(f"Error while running indexer: {str(e)}")

if __name__ == "__main__":
    run_indexer()
