import config
import models
from fastapi import HTTPException
from hdwallet import HDWallet
from hdwallet.symbols import __all__ as SYMBOLS
from hdwallet.utils import generate_mnemonic, generate_passphrase
from modules.encoder import Encoder
from modules.singleton import Singleton
from starlette import status


class Wallet(Singleton):
    LANGUAGE = config.WALLET_LANGUAGE
    STRENGTH = config.WALLET_STRENGTH
    PASSPHRASE_LENGTH = config.PASSPHRASE_LENGTH

    def __init__(self):
        self.encoder = Encoder.get_encoder()

    @classmethod
    def get_wallet(cls):
        return cls()

    @staticmethod
    def normalize_symbol(symbol: str):
        return symbol.upper()

    @staticmethod
    def validate_symbol(symbol: str):
        symbol = Wallet.normalize_symbol(symbol)
        if symbol not in SYMBOLS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Wrong symbol provided."
            )

    def generate_mnemonic(self) -> str:
        mnemonic = generate_mnemonic(language=Wallet.LANGUAGE, strength=Wallet.STRENGTH)
        return self.encoder.encrypt(mnemonic)

    def generate_passphrase(self):
        passphrase = generate_passphrase(length=Wallet.PASSPHRASE_LENGTH)
        return self.encoder.encrypt(passphrase)

    def _get_wallet(self, symbol: str, account: models.Account) -> HDWallet:
        Wallet.validate_symbol(symbol)
        hdwallet = HDWallet(symbol=symbol, use_default_path=True).from_mnemonic(
            mnemonic=self.encoder.decrypt(account.mnemonic),
            language=self.LANGUAGE,
            passphrase=self.encoder.decrypt(account.passphrase),
        )
        return hdwallet

    def generate_address(self, symbol: str, account: models.Account):
        hdwallet = self._get_wallet(symbol, account)
        return hdwallet.p2pkh_address()

    def generate_private_key(self, symbol: str, account: models.Account):
        hdwallet = self._get_wallet(symbol, account)
        return hdwallet.private_key()
