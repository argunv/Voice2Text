from pydantic import BaseModel, ValidationError


class VoiceMessage(BaseModel):
    user_id: int
    file_url: str

def validate_voice_message(data: dict):
    try:
        return VoiceMessage(**data)
    except ValidationError as e:
        raise ValueError(f"Validation failed: {e}")
