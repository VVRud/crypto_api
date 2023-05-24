import base64
import random
from typing import Callable

import pytest
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Random import get_random_bytes
from modules.encoder import Encoder


def shamir_keys() -> list[tuple[int, str]]:
    key = get_random_bytes(16)
    key_parts = Shamir.split(3, 5, key, ssss=False)
    key_parts = [
        (idx, base64.b64encode(key_part).decode("utf-8"))
        for idx, key_part in key_parts
    ]
    random.shuffle(key_parts)
    return key_parts


def shamir_keys_full() -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    real_keys = shamir_keys()
    return real_keys, real_keys


def shamir_keys_partial() -> (
    tuple[list[tuple[int, str]], list[tuple[int, str]]]
):
    real_keys = shamir_keys()
    return real_keys, real_keys[:3]


def shamir_keys_not_enough() -> (
    tuple[list[tuple[int, str]], list[tuple[int, str]]]
):
    real_keys = shamir_keys()
    return real_keys, real_keys[:2]


def shamir_keys_broken() -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    real_keys = shamir_keys()
    return real_keys, [(5 - idx, key) for idx, key in real_keys]


def random_parts() -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    return shamir_keys(), [
        (i + 1, base64.b64encode(get_random_bytes(16)).decode("utf-8"))
        for i in range(5)
    ]


@pytest.mark.parametrize(
    "text",
    ("123456789", "1234567890123456", "1234567890" * 2, "1234567890" * 1024),
)
@pytest.mark.parametrize("keys", (shamir_keys_full, shamir_keys_partial))
def test_encoding_ok(text: str, keys: Callable):
    keys_encoder, keys_decoder = keys()

    encoder = Encoder(keys_encoder)
    encrypted1 = encoder.encrypt(text)
    encrypted2 = encoder.encrypt(text)

    assert encrypted1 != encrypted2

    decoder = Encoder(keys_decoder)
    decrypted1 = decoder.decrypt(encrypted1)
    decrypted2 = decoder.decrypt(encrypted1)

    assert text == decrypted1
    assert text == decrypted2


@pytest.mark.parametrize(
    "text",
    ("123456789", "1234567890123456", "1234567890" * 2, "1234567890" * 1024),
)
@pytest.mark.parametrize(
    "keys", (shamir_keys_not_enough, shamir_keys_broken, random_parts)
)
def test_encoding_failing(text: str, keys: Callable):
    keys_encoder, keys_decoder = keys()

    encoder = Encoder(keys_encoder)
    encrypted = encoder.encrypt(text)

    with pytest.raises(Exception):
        decoder = Encoder(keys_decoder)
        decoder.decrypt(encrypted)
