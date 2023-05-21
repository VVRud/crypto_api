# from hdwallet import HDWallet
# from hdwallet.utils import generate_mnemonic, generate_passphrase
# from hdwallet.symbols import BTC
# import hdwallet.symbols as SYMBOLS
# from typing import Optional
#
# import json
#
# STRENGTH: int = 256
# PASSPHRASE: Optional[str] = generate_passphrase(length=64)
#
# if "BTC" in SYMBOLS.__all__:
#     print("HEH")
#
# # Initialize Bitcoin mainnet HDWallet
# hdwallet: HDWallet = HDWallet(symbol=BTC, use_default_path=True)
# # Get Bitcoin HDWallet from entropy
# mnemonic: str = generate_mnemonic(strength=STRENGTH)
# basic_wallet = hdwallet.from_mnemonic(mnemonic)
#
# derived_wallet = hdwallet.from_mnemonic(
#     mnemonic, passphrase=PASSPHRASE
# )
#
# print(hdwallet.private_key())
# print(hdwallet.public_key())
# print(hdwallet.p2pkh_address())
# # Print all Bitcoin HDWallet information's
# print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))

from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()
