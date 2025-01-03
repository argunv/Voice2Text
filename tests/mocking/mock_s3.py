from unittest.mock import patch


class MockS3Client:
    def upload_file(self, Filename, Bucket, Key):
        print(f"Mock upload: {Filename} to {Bucket}/{Key}")
        return True

    def download_file(self, Bucket, Key, Filename):
        print(f"Mock download: {Bucket}/{Key} to {Filename}")
        return True

@patch("app.core.minio_client.get_minio_client", return_value=MockS3Client())
def mock_s3_client(func):
    return func
