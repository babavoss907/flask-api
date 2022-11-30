""" This module contains all the validator functions for the Pydantic models"""

from base64 import b64decode
from typing import Union, List

from flaskmicro.common.constants import ID_COLUMN_LENGTH


def count_digits(cls, value, field):
    """Counts the number of digits

    Args:
        cls (Object): respective cls object
        value (int): value to count
        field (ModelField): field details
    Returns:
        int: integer value
    Raises:
        ValueError: ValueError will be raised if given value doesn't have the length specified,
        based on minimum_digits and maximum_digits.
    """
    length = len(str(value))

    field_name = cls.schema()["properties"][field.name]
    if (digits := field_name.get("minimum_digits")) and length < digits:
        raise ValueError(f"ensure this value has at least {digits} digits")
    elif (digits := field_name.get("maximum_digits")) and length > digits:
        raise ValueError(f"ensure this value has at most {digits} digits")
    return value

