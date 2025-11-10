
import os
import logging
import time
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from dotenv import load_dotenv

load_dotenv("C:\\Users\\God\\Desktop\\azure-intelligent-search-application\\azure-intelligent-search-application\\config\\.env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def upload_blob(file_path: str, container_name: str, max_retries: int = 5):
    try:
    
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("Missing 'AZURE_STORAGE_CONNECTION_STRING' in .env file")

       
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

       
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        container_created = False
        for attempt in range(1, max_retries + 1):
            try:
                container_client.create_container()
                logging.info(f"Created new container: '{container_name}'")
                container_created = True
                break
            except ResourceExistsError:
                logging.info(f"Container '{container_name}' already exists.")
                container_created = True
                break
            except Exception as e:
                error_msg = str(e)
                if "ContainerBeingDeleted" in error_msg:
                    wait_time = attempt * 10  
                    logging.warning(
                        f"Container is being deleted. Waiting {wait_time}s before retry {attempt}/{max_retries}..."
                    )
                    time.sleep(wait_time)
                else:
                    raise

        if not container_created:
            raise RuntimeError(
                f"Failed to create container after {max_retries} attempts."
            )

        blob_name = os.path.basename(file_path)
        blob_client = container_client.get_blob_client(blob_name)
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            logging.info(f"Successfully uploaded '{blob_name}' to container '{container_name}'")

      
        blob_properties = blob_client.get_blob_properties()
        logging.info(f"Verified: '{blob_name}' uploaded successfully")
        logging.info(f"Size: {blob_properties.size} bytes")
        logging.info(f"Last Modified: {blob_properties.last_modified}")

    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        raise


if __name__ == "__main__":
    file_path = os.path.abspath(r"C:\Users\God\Desktop\azure-intelligent-search-application\azure-intelligent-search-application\data\processed\combined_clustered.json")

    container_name = "policydata"

    logging.info(f"Starting upload for: {file_path}")
    upload_blob(file_path, container_name)