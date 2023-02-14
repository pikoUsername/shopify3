from app.models.domain.wallet import WalletInDB
from ..common import BaseCrud

from .model import Wallet


class WalletCrud(BaseCrud[Wallet, WalletInDB, WalletInDB]):
	model = Wallet
