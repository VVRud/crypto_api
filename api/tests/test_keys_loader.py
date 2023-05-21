from keys_loader import KeysLoader


def test_normal():
    loader = KeysLoader("keys_config.json")
    assert len(loader.key_parts) == 3
