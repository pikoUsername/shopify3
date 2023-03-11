from typing import Optional, TypeVar, List, Any

import sqlalchemy as sa
from sqlalchemy.orm.attributes import QueryableAttribute
from pydantic import BaseModel
from pydantic.fields import ModelField
from fastapi.encoders import jsonable_encoder
from .mixins import ContextInstanceMixin


T = TypeVar("T", bound=BaseModel)
ST = TypeVar("ST", bound=sa.Table)


class ModelsFiller(ContextInstanceMixin):
	"""
	Используется как резолвер под моделей в моделях pydantic
	находит через метадату таблицу, валидирует, и выдает результат

	Можно использвать как глобальную переменную, так и локальную

	model = GroupsInDB(
		permissions=perms,
		users=[]
		name="",
	)

	SubModelsResolver(meta).resolve(model)

	"""
	def __init__(self, meta: Optional[sa.MetaData] = None) -> None:
		if meta:
			self._tables = meta.tables
		self.meta = meta
		self.max_depth = 2

	def configure(self, meta: sa.Table):
		self.meta = meta
		self._tables = self._tables

	def normalize_model_name(self, name: str) -> str:
		"""
		очищает строку для проверки от не нужного

		:param name:
		:return:
		"""
		s = name.lower()
		i = s.find("indb")
		return name[:i]

	def find_table_by_name(self, name: str) -> sa.Table:
		return self._tables[name]

	def resolve_model_name(self, model: T) -> sa.Table:
		"""
		находит модельку по self._tables

		:param model:
		:return:
		"""
		name = model.__name__
		if hasattr(model, "__tablename__"):
			return model.__tablename__
		name = self.normalize_model_name(name)
		return self.find_table_by_name(name)

	def detect_sub_models(self, model: T) -> List[str]:
		result = []
		for key, value in model.__fields__.items():
			if isinstance(value.type_, BaseModel):
				if not self.resolve_model_name(value):
					raise ValueError("%s is not associated with any tables." % key)
				result.append(key)
		return result

	def validate_relation(self, key: str, db_obj: ST) -> Any:
		"""
		Вызывает еррорку при обнаружении проблемы

		:param key:
		:param db_obj:
		:return:
		"""
		rel = getattr(db_obj, key, None)

		if not rel:
			raise ValueError(
				"wrong configuration, key %s is not associated with any column in table" % key
			)
		if not isinstance(rel, QueryableAttribute) or not rel.class_:
			raise ValueError(
				"column - %s is not any valid relationship" % key
			)
		return rel

	def check_if_iterable(self, field: ModelField) -> bool:
		if field.outer_type_ == field.type_:
			return False
		if isinstance(field.outer_type_.__origin__, (list, set, tuple)):
			return True
		return False

	def resolve_model(self, model: T, db_obj: ST) -> ST:  # db_obj has to be model object
		"""
		Заполнит до окончания, сделает все абсолютно все
		Предологается что модель и таблица алхимии АБСОЛЮТНО точные

		:param model:
		:return:
		"""
		for key, field in model.__fields__.items():
			if isinstance(field.type_, BaseModel):
				if self.check_if_iterable(field):
					for val in field:
						db_rel = self._fill_table_data_by_one(db_obj, key, val)
						getattr(db_obj, key).add(db_rel)
					continue
				db_rel = self._fill_table_data_by_one(db_obj, key, field)
				setattr(db_obj, key, db_rel)

		return db_obj

	def _fill_table_data_by_one(self, db_obj: sa.Table, key: str, field: T) -> sa.Table:
		"""
		Field.type_ должен соответствовать BaseModel

		Предполагается что модельки абсолютно точно реперезентеруют таблицы

		:param db_obj:
		:param key:
		:param field:
		:return:
		"""
		table = self.resolve_model_name(field.type_)
		obj_in_data: dict = jsonable_encoder(field, exclude_unset=True)
		sub_main_obj = table(**obj_in_data)  # noqa
		assert self.validate_relation(key, db_obj)
		if self.detect_sub_models(field.type_):
			self.resolve_model(field, sub_main_obj)

		return sub_main_obj

	def convert_model_to_db_obj(self, obj_in: T) -> sa.Table:
		db_type = self.resolve_model_name(obj_in)

		data = jsonable_encoder(obj_in, exclude_unset=True)
		return db_type(**data)  # noqa