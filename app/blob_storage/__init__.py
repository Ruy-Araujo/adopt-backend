import logging
import os

from azure.storage.blob import BlobServiceClient


def upload_file(file_name, data):

    try:
        credential = os.getenv("AZURE_BLOB_CREDENTIAL")
        service = BlobServiceClient(account_url=os.getenv('AZURE_ACCOUNT_URL'), credential=credential)
        container_client = service.get_container_client(os.getenv("AZURE_CONTAINER_NAME"))
        blob_client = container_client.get_blob_client(file_name)
    except Exception as e:
        logging.error(f"Erro ao conectar ao Azure Blob Storage: {e}")
        print(f"Erro ao conectar ao Azure Blob Storage: {e}")

    try:
        blob_client.upload_blob(data)
        logging.info(f"Arquivo {file_name} enviado com sucesso!")
        print(f"Arquivo {file_name} enviado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao fazer upload do arquivo: {e}")
        print(f"Erro ao fazer upload do arquivo: {e}")
