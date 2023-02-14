import decimal

from app.db.repositories.user import Users
from app.core.config import get_app_settings


def check(user: Users, money_change: decimal.Decimal) -> bool:
	if user.is_deactivated or user.wallet.is_frozen:
		return False

	if user.is_stuff and get_app_settings().debug:
		return True

	if money_change < 1000000000:
		return False
	return True  # fuck it just
