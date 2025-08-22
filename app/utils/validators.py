import re


def is_valid_email(email: str):
    PATTERN = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
    return bool(PATTERN.fullmatch(email))


def is_valid_username(username: str):
    return isinstance(username, str) and username != "" and not any(ch.isspace() for ch in username)


def is_valid_password(pwd: str):
    return len(pwd) >= 5 and any(ch.isdigit() for ch in pwd)
