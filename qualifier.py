import itertools
import string
import random

from typing import Optional, Iterable

def generate_password(
    password_length: int = 8,
    has_symbols: bool = False,
    has_uppercase: bool = False,
    ignored_chars: Optional[Iterable[str]] = None,
    allowed_chars: Optional[Iterable[str]] = None
) -> str:
    """Generates a random password.

    The password will be exactly `password_length` characters.
    If `has_symbols` is True, the password will contain at least one symbol, such as #, !, or @.
    If `has_uppercase` is True, the password will contain at least one upper case letter.
    """

    # If both `ignored_chars` and `allowed_chars` was passes
    if ignored_chars and allowed_chars:
        raise UserWarning("Cannot pass both `ignored_chars` and `allowed_chars` at the same time")

    # Checking if both `has_symbols` and `has_uppercase` is true. If so, minimun password length >= 2
    minimum_len = max(1, has_symbols + has_uppercase)
    if minimum_len > password_length:
        raise UserWarning(f"Cannot have a password of length {password_length}")

    # Checking that password is smaller than 1 000 000 chars
    if password_length > 999999:
        raise UserWarning(f"Password length cannot be greater than 1 000 000 - Passed {password_length}")

    # Getting characters to be used in password generation
    symbols = string.punctuation
    uppercase_ltrs = string.ascii_uppercase
    lowercase_ltrs = string.ascii_lowercase
    digits = string.digits

    # If `ignored_chars` -> True
    if ignored_chars:
        ignored_chars = set(ignored_chars)

        symbols = [char for char in symbols if char not in ignored_chars]
        digits = [char for char in digits if char not in ignored_chars]
        uppercase_ltrs = [char for char in uppercase_ltrs if char not in ignored_chars]
        lowercase_ltrs = [char for char in lowercase_ltrs if char not in ignored_chars]


    # If `allowed_chars` is not empty
    if allowed_chars:
        allowed_chars = set(allowed_chars)

        # Checking if the `allowed_chars` has symbols and/or uppercase letters
        symbols = [char for char in symbols if char in allowed_chars]
        uppercase_ltrs = [char for char in uppercase_ltrs if char in allowed_chars]

        # List of chars
        pool = list(allowed_chars)
    
    else:
        pool = list(itertools.chain(symbols, digits, uppercase_ltrs, lowercase_ltrs))

    # Generating password
    password = random.choices(pool, k=password_length)

    # Checking if generated password `has_symbols` and/or `has_uppercase`
    indices = random.sample(range(password_length),k=has_symbols + has_uppercase)

    if has_symbols:
        if not symbols:
            raise UserWarning("`has_symbols` -> True, but no symbols where found in passed `allowed_chars`")
        # Replace part with random symbol
        password[indices[0]] = random.choice(symbols)

    if has_uppercase:
        if not uppercase_ltrs:
            raise UserWarning("`has_uppercase` -> True, but no uppercase letters were found in passed `allowed_chars`")
        # Replace part with random uppercase letter 
        password[indices[0 + has_symbols]] = random.choice(uppercase_ltrs)

    return "".join(password)