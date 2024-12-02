from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator ,model_validator


class Image(BaseModel):
    query: str
    image_url: str
    image_data: bytes
    width: int
    height: int
    downloaded_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(frozen=True)

 