import config
import models
from fastapi import HTTPException
from hdwallet import HDWallet
from hdwallet.symbols import BCH, BTC, DASH, DOGE, ETH, RVN, ZEC
from hdwallet.utils import generate_mnemonic, generate_passphrase
from modules.encoder import Encoder
from starlette import status


class Wallet:
    """Wallet related class for managing addresses and accounts."""

    LANGUAGE = config.WALLET_LANGUAGE
    STRENGTH = config.WALLET_STRENGTH
    PASSPHRASE_LENGTH = config.PASSPHRASE_LENGTH
    SYMBOLS = [BTC, ETH, BCH, DASH, DOGE, ZEC, RVN]

    def __init__(self):
        self.encoder = Encoder.get_encoder()

    @classmethod
    def get_wallet(cls):
        """Get wallet context"""
        return cls()

    @staticmethod
    def normalize_symbol(symbol: str):
        """Normalize entered symbol to existing format."""
        return symbol.upper()

    def validate_symbol(self, symbol: str):
        """Validate symbol exists."""
        symbol = Wallet.normalize_symbol(symbol)
        if symbol not in self.SYMBOLS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wrong symbol provided. Available symbols are: {self.SYMBOLS}",
            )

    def generate_mnemonic(self) -> str:
        """Generate account mnemonic phrase."""
        mnemonic = generate_mnemonic(
            language=Wallet.LANGUAGE, strength=Wallet.STRENGTH
        )
        return self.encoder.encrypt(mnemonic)

    def generate_passphrase(self):
        """Generate account passphrase"""
        passphrase = generate_passphrase(length=Wallet.PASSPHRASE_LENGTH)
        return self.encoder.encrypt(passphrase)

    def _get_wallet(self, symbol: str, account: models.Account) -> HDWallet:
        """Retrieve wallet for an account."""
        self.validate_symbol(symbol)
        hdwallet = HDWallet(symbol=symbol, use_default_path=True).from_mnemonic(
            mnemonic=self.encoder.decrypt(account.mnemonic),
            language=self.LANGUAGE,
            passphrase=self.encoder.decrypt(account.passphrase),
        )
        return hdwallet

    def generate_address(self, symbol: str, account: models.Account):
        """Generate address for an account."""
        hdwallet = self._get_wallet(symbol, account)
        return hdwallet.p2pkh_address()

    def generate_private_key(self, symbol: str, account: models.Account):
        """Generate private key for an account."""
        hdwallet = self._get_wallet(symbol, account)
        return hdwallet.private_key()
