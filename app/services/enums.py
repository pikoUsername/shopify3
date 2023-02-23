from enum import Enum


class TextEntitiesTypes(str, Enum):
	"""
	Copy pasted from telegram bot api MessageEntity object
	"""
	url = "url"
	phone_number = "phone_number"
	bold = "bold"
	italic = "italic"
	pre = "pre"
	text_link = "text_link"  # a tag
	underline = "underline"
