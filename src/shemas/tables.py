from pydantic import BaseModel, ConfigDict, Field


class TableBase(BaseModel):
    name: str = Field(...)
    seats: int = Field(..., description="Количество мест", ge=1)
    location: str = Field(description="Локация стола")


class TableCreate(TableBase):
    pass


class TableModel(TableBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

