from pydantic import BaseModel

class LinksParam(BaseModel):
    links: list[str]
