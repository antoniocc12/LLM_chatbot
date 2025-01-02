"""
Version: 1.0

Utility functions/classes related to environment.
"""

import os
from typing import Any, Literal, Callable

from .converter import convert, OnError, ErrorInfo, InvalidValueForConversion, InvalidConversionType


def get_env(
        key: str,
        default_value: Any = None,
        to: Literal[
            "str", "str.lower", "str.upper", "int", "float", "bool", "dict", "list",
            "list.of.str", "list.of.str.lower", "list.of.str.upper", "list.of.int", "list.of.float", "list.of.bool"
        ] = "str",
        remove_whitespace: bool = True,
        list_split_char: str = ",",
        on_error: Callable[[ErrorInfo], Any] = OnError.raise_exception,
) -> Any:
    """
    Returns the converted value of the environment variable. If the key is not present in the environment, then it will
    return the default_value.

    :param on_error: Callable method to decide the action in case of error
    :param key: (str) Name of the environment variable.
    :param default_value: (Any, default=None) Default value if the key is not present in the environment.
    :param to: (str, default="str") Data type to which the value should convert.
        Options  are
            "str", "str.lower", "str.upper", "int", "float", "bool", "list",
            "list.of.str", "list.of.str.lower", "list.of.str.upper", "list.of.int", "list.of.float", "list.of.bool"
    :param remove_whitespace: (bool, default=True) Remove white space from beginning and end of the string.
        Valid only for str and list.of.str conversions.
    :param list_split_char: (str, default=",") Character used to split the value. Valid only for list conversions.
    :return: (Any) Converted value of the env variable.
    """

    value = os.environ.get(key, default_value)
    try:
        value = convert(value, to=to, remove_whitespace=remove_whitespace, list_split_char=list_split_char,
                        on_error=on_error)
    except InvalidValueForConversion:
        raise InvalidValueForConversion(f"Invalid config value [{key}={value}] for '{to}' conversion")
    except InvalidConversionType:
        raise InvalidConversionType(f"Invalid type({to}) for conversion")
    return value
