import pytest
from coinaddrvalidator.validation import ValidationResult, validate
from fastapi import HTTPException
from models import Account
from modules.wallet import Wallet

from .fixtures import account, user, wallet


@pytest.mark.parametrize("symbol", Wallet.SYMBOLS)
def test_addresses_generation(wallet: Wallet, account: Account, symbol: str):
    addr = wallet.generate_address(symbol, account)
    result: ValidationResult = validate(symbol, addr)
    assert result.valid and result.ticker.upper() == symbol


@pytest.mark.parametrize("symbol", ("BTC", "btc", "bTc", "ETH"))
def test_symbol_validation(wallet: Wallet, symbol: str):
    assert wallet.validate_symbol(symbol) is None


@pytest.mark.parametrize("symbol", ("BTCB", "ELK", "acb", "bdc"))
def test_symbol_validation_fails(wallet: Wallet, symbol: str):
    with pytest.raises(HTTPException):
        wallet.validate_symbol(symbol)
