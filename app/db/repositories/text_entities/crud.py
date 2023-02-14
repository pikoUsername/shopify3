from app.models.domain.text_entities import TextEntitiesInDB
from ..common import BaseCrud

from .model import TextEntity


class TextEntitiesCRUD(
	BaseCrud[TextEntity, TextEntitiesInDB, TextEntitiesInDB]
):
	model = TextEntity
