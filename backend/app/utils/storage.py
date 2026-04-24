"""Storage utility for Google Cloud Storage."""

from typing import Optional
import logging

try:
    from google.cloud import storage

    storage_client = storage.Client()
except ImportError:
    storage_client = None

logger = logging.getLogger(__name__)


def upload_to_gcs(
    bucket_name: str, source_file_name: str, destination_blob_name: str
) -> bool:
    """
    Uploads a file to the bucket.

    Args:
        bucket_name (str): The ID of your GCS bucket.
        source_file_name (str): The path to your file to upload.
        destination_blob_name (str): The ID of your GCS object.

    Returns:
        bool: True if upload was successful, False otherwise.
    """
    if not storage_client:
        logger.warning("Google Cloud Storage client is not initialized.")
        return False

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logger.info(f"File %s uploaded to %s.", source_file_name, destination_blob_name)
        return True
    except Exception as e:
        logger.error(f"Failed to upload to GCS: {e}")
        return False
