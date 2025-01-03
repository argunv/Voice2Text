from unittest.mock import MagicMock


def mock_session():
    mock = MagicMock()
    mock.add = MagicMock()
    mock.commit = MagicMock()
    mock.rollback = MagicMock()
    mock.close = MagicMock()
    return mock
