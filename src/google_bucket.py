from google.cloud import storage

storage_client = storage.Client()
buckets = storage_client.list_buckets()

for bucket in buckets:
    print(bucket.name)

def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket("tfm-parrot-assistant")
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0
    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
    
def download_blob(source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket("tfm-parrot-assistant")
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, "tfm-parrot-assistant", destination_file_name
        )
    )

def list_blobs():
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    blobs = storage_client.list_blobs("tfm-parrot-assistant")
    list_of_blobs = []
    for blob in blobs:
        list_of_blobs.append(blob.name)
        
    return list_of_blobs