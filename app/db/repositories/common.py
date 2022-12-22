from typing import Generic, Type, TypeVar, List, Union, Dict, Any, Optional, Tuple

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import sqlalchemy as sa
from loguru import logger

from app.db.repositories.base import BaseModel as DBBaseModel


ExModelType = TypeVar("ExModelType", bound=DBBaseModel)
ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	"""
	Provides basic CRUD support system,
	with extra method support - get_multi, create_with_relationship, get_or_create

	"""
	__slots__ = "model",

	def __init__(self, model: Type[sa.Table]):
		self.model = model

	async def get(self, db, id: Any) -> Optional[ModelType]:
		return await db.execute(sa.select(self.model).filter(self.model.id == id).first())

	async def get_multi(
			self, db, skip: int = 0, limit: int = 100
	) -> List[ModelType]:
		return await db.run_sync(db.query(self.model).offset(skip).limit(limit).all())

	async def create(self, db, obj_in: CreateSchemaType) -> ModelType:
		obj_in_data = jsonable_encoder(obj_in, exclude_unset=True)
		db_obj = self.model(**obj_in_data)  # type: ignore
		db.add(db_obj)
		await db.commit()
		await db.refresh(db_obj)
		return db_obj

	async def create_with_relationship(
			self,
			db,
			obj_in: CreateSchemaType,
			relationship_model: Union[List[ExModelType], ExModelType],
			field_name: Union[List[str], str],
	) -> ModelType:
		obj_in_data = jsonable_encoder(obj_in, exclude_unset=True)
		db_obj = self.model(**obj_in_data)  # type: ignore
		if isinstance(relationship_model, list) and isinstance(field_name, list):
			for x in zip(relationship_model, field_name):
				setattr(db_obj, x[0], x[1])
		else:
			setattr(db_obj, field_name, relationship_model)
		db.add(db_obj)
		await db.commit()
		await db.refresh(db_obj)
		return db_obj

	async def update(
			self,
			db,
			*,
			db_obj: ModelType,
			obj_in: Union[UpdateSchemaType, Dict[str, Any]]
	) -> ModelType:
		logger.info(
			f"Changed object: {self.model.__tablename__}")
		obj_data = jsonable_encoder(db_obj)
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)
		for field in obj_data:
			if field in update_data:
				setattr(db_obj, field, update_data[field])
		db.add(db_obj)
		await db.commit()
		await db.refresh(db_obj)
		return db_obj

	async def delete(self, db, id: int) -> ModelType:
		logger.info(
			f"Removed object: {self.model.__tablename__} from database data.")

		obj = await db.get(self.model, id)
		await db.delete(obj)
		await db.commit()
		return obj

	async def get_or_create(
			self, db, obj_in: CreateSchemaType, id_name: str = "id"
	) -> Tuple[ModelType, bool]:
		if group := await self.get(db, getattr(obj_in, id_name)):
			return group, False
		return await self.create(db, obj_in.copy(exclude={id_name})), True

