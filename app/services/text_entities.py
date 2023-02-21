from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
	from app.models.domain.text_entities import TextEntitiesInDB


def parse_text(text: str) -> Tuple[str, List[TextEntitiesInDB]]:
	pass
