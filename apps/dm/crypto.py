import base64
import hashlib

from cryptography.fernet import Fernet
from django.conf import settings


def _cipher() -> Fernet:
    seed = f"{settings.SECRET_KEY}|dchat-dm-v1".encode("utf-8")
    key = base64.urlsafe_b64encode(hashlib.sha256(seed).digest())
    return Fernet(key)


def encrypt_text(value: str) -> str:
    return _cipher().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_text(value: str) -> str:
    return _cipher().decrypt(value.encode("utf-8")).decode("utf-8")
