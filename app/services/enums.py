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


class PermissionTypes(str, Enum):
	edit = "edit"
	delete = "delete"
	read = "read"
	create = "create"


class GlobalPermissions(Enum):
	anonymous = ""


class GlobalGroups(Enum):
	"""
	Global groups format:
	{name} = {permission_name}
	permission name has to be valid
	"""
	default_user = "anonymous"
