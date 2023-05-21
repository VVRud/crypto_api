from keys_loader import KeysLoader


def test_normal():
    loader = KeysLoader("keys_config.json")
    assert len(loader.load_aes_keys()) == 3
    assert loader.load_jwt_secret_token() == "123456789012345678901234567890"
