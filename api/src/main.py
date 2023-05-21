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
# print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
# print(hdwallet.private_key())
# print(hdwallet.public_key())
# print(hdwallet.p2pkh_address())
# print(hdwallet.xprivate_key(encoded=True))
# print(hdwallet.xprivate_key(encoded=False))
# pubkey = "xprv9s21ZrQH143K2QfnQPtWLMcmRNSR7KA85u3KmoY4oYmSCwtkpvoL7epKHS1pQAzkCZJW7dJLkSYY84Xj2aqSgqoQkv5UhW42vkXkqZSoRG5"
# hdwallet: HDWallet = HDWallet(symbol=BTC, use_default_path=True)
# hdwallet.from_xprivate_key(pubkey, strict=True)
# # Print all Bitcoin HDWallet information's
# print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
#
#
# derived_wallet = hdwallet.from_mnemonic(
#     mnemonic, passphrase=PASSPHRASE
# )

from accounts.router import router as accounts_router
from auth.router import router as auth_router
from fastapi import FastAPI

from database import database

app = FastAPI()
app.include_router(accounts_router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await database.initialize_db()


@app.on_event("shutdown")
async def shutdown():
    pass
