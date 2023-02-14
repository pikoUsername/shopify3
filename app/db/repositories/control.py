# acces control system
CONTROL_LIST = {"edit", "delete", "read", "create"}


class AccessControl:
	def __init__(self, model_name: str):
		self.model_name = model_name

	def all(self):
		return self.include(*CONTROL_LIST)

	def include(self, *args):
		if args not in CONTROL_LIST:
			raise ValueError(
				f"Your permissions keys {' '.join(*args)} does not match actual permissions keys")
		return self.format(*args)

	def format(self, *args):
		return [f"{perm}_{self.model_name}" for perm in args]

	def check(self, obj, group=None, *args):
		permissions_model = getattr(obj, "permissions", None) or getattr(obj, "perms", None)
		if permissions_model is None:
			raise ValueError("This model doesn't have permissions relationship, or it's empty rel")
		if permissions_model.code:
			pass
