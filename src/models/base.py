from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel, Field

Base = declarative_base()

class LinksBaseModel(SQLModel):
    link: str
    created_at: int

class Links(LinksBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
