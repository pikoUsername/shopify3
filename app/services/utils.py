from typing import TypeVar, Type, List, Iterable, Dict, Any

import sqlalchemy as sa
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


T = TypeVar("T", bound=BaseModel)


def convert_db_obj_to_model(db_obj: sa.Table, model: Type[T]) -> T:
	return model.from_orm(db_obj)


def convert_list_obj_to_model(objects: List[sa.Table], model: Type[T]) -> Iterable[T]:
	models = []

	for obj in objects:
		models.append(model.from_orm(obj))

	return models


def extract_default_value_from_db_obj(db_obj: sa.Table) -> Dict[str, Any]:
	"""
	Extracts created_at, updated_at, id from db obj

	:param db_obj:
	:return:
	"""
	return {
		"id": db_obj.id,
		"created_at": db_obj.created_at,
		"updated_at": db_obj.updated_at,
	}


def convert_sub_objs_to_db_obj(obj_in: T, name: str, db_type: sa.Table) -> sa.Table:
	obj = getattr(obj_in, name)
	data = jsonable_encoder(obj)
	return db_type(**data)


def fill_sub_models(obj_in: dict[str, Any]):
	pass


def detect_sub_models(obj_in: T) -> List[str]:
	result = []

	for key, value in obj_in.__fields__.items():
		if isinstance(value.type_, BaseModel) or issubclass(value.type_, BaseModel):
			result.append(key)

	return result

