from app.core.utils import generate_file_hash


def test_generate_file_hash(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("test content")

    file_hash = generate_file_hash(file)
    assert len(file_hash) == 64  # SHA-256 хэш
