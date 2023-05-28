from typing import OrderedDict

import pytest
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from alchemyjsonschema import (
    BaseModelWalker,
    DefaultClassfier,
    ForeignKeyWalker,
    NoForeignKeyWalker,
    SchemaFactory,
    StructuralWalker,
)

Base = declarative_base()


class MyModel(Base):
    __tablename__ = "my_model"

    id = Column("id", UUID, primary_key=True)


@pytest.mark.parametrize(
    "walker", [ForeignKeyWalker, NoForeignKeyWalker, StructuralWalker]
)
def test_hybrid_property(walker: BaseModelWalker) -> None:
    schema_factory = SchemaFactory(walker, DefaultClassfier)

    actual = schema_factory(MyModel)

    assert actual == {
        "properties": OrderedDict({"id": {"type": "string", "format": "uuid"}}),
        "required": ["id"],
        "title": "MyModel",
        "type": "object",
    }
