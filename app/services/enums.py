from enum import Enum


class TextEntitiesTypes(str, Enum):
	"""
	Copy pasted from telegram bot api MessageEntity object
	"""
	mention = "mention"
	hashtag = "hashtag"
	url = "url"
	phone_number = "phone_number"
	bold = "bold"
	italic = "italic"
	pre = "pre"
	code = "code"
	text_link = "text_link"
