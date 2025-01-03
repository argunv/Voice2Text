from app.core.minio_client import get_s3_client


def test_minio_integration():
    client = get_s3_client()

    # Test bucket creation
    bucket_name = "test-bucket"
    client.create_bucket(Bucket=bucket_name)

    # Test file upload
    file_name = "test.txt"
    with open(file_name, "w") as f:
        f.write("test content")

    client.upload_file(file_name, bucket_name, file_name)

    # Test file download
    downloaded_file = f"downloaded_{file_name}"
    client.download_file(bucket_name, file_name, downloaded_file)

    with open(downloaded_file, "r") as f:
        content = f.read()

    assert content == "test content"
