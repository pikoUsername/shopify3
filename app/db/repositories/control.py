# acces control system
from typing import List

CONTROL_LIST = {"edit", "delete", "read", "create"}


class AccessControl:
	def __init__(self, model_name: str):
		self.model_name = model_name

	@classmethod
	def all(cls) -> List[str]:
		return cls.format(*CONTROL_LIST)

	def format(self, *args) -> List[str]:
		if args not in CONTROL_LIST:
			raise ValueError(
				f"Your permissions keys {' '.join(*args)} does not match actual permissions keys")
		return [f"{perm}_{self.model_name}" for perm in args]

