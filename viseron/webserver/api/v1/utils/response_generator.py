"""Helper that lets a user specify fields from an object to return"""

from collections import defaultdict


def __get_nested(obj: any, keys: list, subscript: bool = False) -> object:
    """
    Gets the value of a key in a nested object or dictionary.
    """
    __obj = obj
    for key in keys:
        if subscript:
            __obj = __obj[key]
        else:
            __obj = getattr(__obj, key)
    return __obj


def __set_nested(obj: any, keys: list, value: any):
    """
    Sets the value of a key in a nested object or dictionary
    """
    obj = __get_nested(obj, keys[:-1], True)
    obj[keys[-1]] = value


def __fix(f):
    """
    We need to be able to have a defaultdict that defaults to defaultdict recursively. So this function lets use do that.
    We have to wrap f inside a lambda so that it’s not evaluated when __fix is called.
    """
    return lambda *args, **kwargs: f(__fix(f), *args, **kwargs)


def get_resp_obj(obj: any, fields: list) -> dict:
    """
    Converts a complex nested object/ dictionary into a nested dictionary of only specified keys.
    Args:
        obj: Object/ Dictionary that contains the data.
        fields: List of List of strings, each list should be a list of strings that represent the nested key structure.
    """
    resp_obj = __fix(defaultdict)()

    for field in fields:
        __set_nested(resp_obj, field, __get_nested(obj, field))

    return resp_obj

