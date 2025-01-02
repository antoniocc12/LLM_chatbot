"""
Version: 1.0

Utility functions/classes related to environment.
"""

import json
from typing import Any, Literal, Callable


class InvalidValueForConversion(Exception):
    pass


class InvalidConversionType(Exception):
    pass


class ErrorInfo:

    def __init__(self, to: str,
                 value: Any,
                 exception: str,
                 exception_class: type):
        self.to = to
        self.value = value
        self.exception = exception
        self.exception_class = exception_class


class OnError:

    @staticmethod
    def raise_exception(error_info: ErrorInfo):
        raise error_info.exception_class(error_info.exception)

    @staticmethod
    def return_none(error_info: ErrorInfo):
        return None

    @staticmethod
    def return_value(error_info: ErrorInfo):
        return error_info.value


def convert(
        value: str,
        to: Literal[
            "str", "str.lower", "str.upper", "int", "float", "bool", "dict", "list",
            "list.of.str", "list.of.str.lower", "list.of.str.upper", "list.of.int", "list.of.float", "list.of.bool"
        ] = "str",
        remove_whitespace: bool = True,
        list_split_char: str = ",",
        on_error: Callable[[ErrorInfo], Any] = OnError.raise_exception,
) -> Any:
    """
    The value is converted to the specific datatype/format specified in the `to` parameter.
    In case of error, the OnError method passed to on_error parameter will be called.

    :param value: (str) Value that needs to be converted.
    :param to: (str, default="str") Data type or format to which the value should be converted.
        Options  are
            "str", "str.lower", "str.upper", "int", "float", "bool", "list",
            "list.of.str", "list.of.str.lower", "list.of.str.upper", "list.of.int", "list.of.float", "list.of.bool"
    :param remove_whitespace: (bool, default=True) Remove white space from beginning and end of the string.
        Valid only for str and list.of.str conversions.
    :param list_split_char: (str, default=",") Character used to split the value. Valid only for list conversions.
    :param on_error: Callable method to decide the action in case of error
    :return: (Any) Converted value of the env variable.
    :raises InvalidValueForConversion: If the value cannot be converted to the given format.
    :raises InvalidConversionType: If the `to` param is not in the supported types.
    """

    if to == "str":
        # String conversion.
        value = str(value).strip() if remove_whitespace else str(value)
    elif to == "str.lower":
        # String conversion with lower-case modifier.
        value = convert(value=value, to="str", remove_whitespace=remove_whitespace).lower()
    elif to == "str.upper":
        # String conversion with upper-case modifier.
        value = convert(value=value, to="str", remove_whitespace=remove_whitespace).upper()
    elif to == "int":
        #  Integer conversion.
        try:
            value = int(value)
        except Exception as e:
            return on_error(ErrorInfo(to=to,
                                      value=value,
                                      exception=f"Invalid value '{value}' for integer conversion.",
                                      exception_class=InvalidValueForConversion))

    elif to == "float":
        #  Float conversion.
        try:
            value = float(value)
        except Exception as e:
            return on_error(ErrorInfo(to=to,
                                      value=value,
                                      exception=f"Invalid value '{value}' for float conversion.",
                                      exception_class=InvalidValueForConversion))

    elif to == "dict":
        try:
            # Dict conversion
            value = convert(value=value, to="str", remove_whitespace=True)
            value = json.loads(value)
        except Exception as e:
            return on_error(ErrorInfo(to=to,
                                      value=value,
                                      exception=f"Invalid value '{value}' for dict conversion",
                                      exception_class=InvalidValueForConversion))

    elif to == "bool":
        #  Boolean conversion.
        value = convert(value=value, to="str.lower", remove_whitespace=True)
        truthy_values = ['true', 't', 'yes', 'y', 'on', '1']
        falsy_values = ['false', 'f', 'no', 'n', 'off', '0']
        if value in truthy_values:
            value = True
        elif value in falsy_values:
            value = False
        else:
            return on_error(ErrorInfo(to=to,
                                      value=value,
                                      exception=f"Invalid value '{value}' for boolean conversion.",
                                      exception_class=InvalidValueForConversion))
    elif to == "list":
        #  List conversion. By default, list conversion convert the value to list of strings.
        value = convert(
            value=value,
            to="list.of.str",
            remove_whitespace=remove_whitespace,
            list_split_char=list_split_char,
            on_error=on_error
        )
    elif to.startswith("list.of."):
        #  List of subtype conversion.
        sub_type = to.replace("list.of.", "", 1)
        value = list(map(
            lambda v: convert(value=v, to=sub_type, remove_whitespace=remove_whitespace, on_error=on_error),
            convert(value=value, to="str",
                    remove_whitespace=remove_whitespace, on_error=on_error).split(list_split_char)
        ))
    else:
        return on_error(ErrorInfo(to=to,
                                  value=value,
                                  exception=f"Invalid type '{to}' for conversion.",
                                  exception_class=InvalidConversionType))
    return value
