from pydantic import BaseConfig, BaseModel


class RWModel(BaseModel):
	@classmethod
	def get_table_name(cls):
		if hasattr(cls, '__tablename__'):
			return cls.__tablename__
		s = cls.__name__.lower()
		s = s.strip("indb")
		return s.capitalize()

	class Config(BaseConfig):
		orm_mode = True
