# acces control system
from typing import List

CONTROL_LIST = {"update", "delete", "read", "create"}  # DONT DARE TO CHANGE!!!!


class AccessControl:
	def __init__(self, model_name: str):
		self.model_name = model_name

	def all(self) -> List[str]:
		return self.format(*CONTROL_LIST)

	def format(self, *args) -> List[str]:
		try:
			first_arg = args[0]
		except IndexError:
			pass
		else:
			if first_arg == "*":
				return self.all()

		for arg in args:
			if arg not in CONTROL_LIST:
				raise ValueError(
					f"Your permissions keys {', '.join(args)} does not match actual permissions keys")

		return [f"{perm}_{self.model_name}" for perm in args]

