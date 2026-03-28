from __future__ import annotations

import hashlib
import random
import secrets
import time
from hmac import compare_digest

from django.conf import settings


def _captcha_key(flow: str) -> str:
    return f"math_captcha:{flow}"


def create_math_captcha(session, flow: str) -> str:
    a = random.randint(2, 20)
    b = random.randint(2, 20)
    op = random.choice(["+", "-"])
    answer = a + b if op == "+" else a - b
    salt = secrets.token_hex(8)
    digest = hashlib.sha256(f"{answer}:{salt}:{settings.SECRET_KEY}".encode("utf-8")).hexdigest()
    question = f"What is {a} {op} {b}?"
    session[_captcha_key(flow)] = {
        "digest": digest,
        "salt": salt,
        "exp": int(time.time()) + 300,
        "question": question,
    }
    session.modified = True
    return question


def get_math_captcha_question(session, flow: str, force_new: bool = False) -> str:
    data = session.get(_captcha_key(flow))
    if force_new or not data or int(time.time()) > int(data.get("exp", 0)) or not data.get("question"):
        return create_math_captcha(session, flow)
    return str(data["question"])


def verify_math_captcha(session, flow: str, answer_text: str) -> bool:
    data = session.get(_captcha_key(flow))
    if not data:
        return False
    if int(time.time()) > int(data.get("exp", 0)):
        session.pop(_captcha_key(flow), None)
        session.modified = True
        return False
    try:
        answer = int(str(answer_text).strip())
    except Exception:
        return False

    digest = hashlib.sha256(f"{answer}:{data['salt']}:{settings.SECRET_KEY}".encode("utf-8")).hexdigest()
    valid = compare_digest(digest, data["digest"])
    if valid:
        session.pop(_captcha_key(flow), None)
        session.modified = True
    return valid


def captcha_failure_message() -> str:
    messages = [
        "What is that, pal? Can't do basic math?",
        "Numbers 1, you 0. Try again.",
        "That answer belongs in a different universe.",
        "Quick reboot your brain and try once more.",
        "Close, but the calculator in your head is on airplane mode.",
    ]
    return f"Failed because: (Captcha) {random.choice(messages)}"
