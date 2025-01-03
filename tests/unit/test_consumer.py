from app.consumer.tasks import transcribe_audio


def test_transcribe_audio(mocker):
    mock_model = mocker.patch("app.consumer.tasks.whisper.load_model")
    mock_model.return_value.transcribe.return_value = {"text": "test transcription"}

    result = transcribe_audio("test_file_path")
    assert result == "test transcription"
