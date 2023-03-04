from typing import TypeVar, Type, List, Iterable

import sqlalchemy as sa
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


def convert_db_obj_to_model(db_obj: sa.Table, model: Type[T]) -> T:
	return model.from_orm(db_obj)


def convert_list_obj_to_model(objects: List[sa.Table], model: Type[T]) -> Iterable[T]:
	models = []

	for obj in objects:
		models.append(model.from_orm(obj))

	return models
