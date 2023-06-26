import types
import typing

import pudb


def type_annotation_to_string(
    type_annotation: type | types.GenericAlias | typing._GenericAlias | typing._SpecialGenericAlias | typing._SpecialForm | typing.TypeVar | None
) -> str:
    # type_annotation: None
    # type_annotation: builtins.NoneType
    if type_annotation is None or type_annotation is type(None):
        return 'None'
    # type_annotation: list
    elif isinstance(type_annotation, type):
        return f'{type_annotation.__module__}.{type_annotation.__name__}'
    # type_annotation: list | int
    elif isinstance(type_annotation, types.UnionType):
        arg_string_list: list[str] = []
        for arg in type_annotation.__args__:
            arg_string_list.append(type_annotation_to_string(arg))
        
        return ' | '.join(arg_string_list)
    # type_annotation: typing.list[pathman._impl.s3.S3Path], typing.List[pathman._impl.s3.S3Path]
    elif isinstance(type_annotation, (types.GenericAlias, typing._GenericAlias)):
        origin_string: str = type_annotation_to_string(type_annotation.__origin__)

        arg_string_list: list[str] = []
        for arg in type_annotation.__args__:
            arg_string_list.append(type_annotation_to_string(arg))

        return ''.join((origin_string, '[', ', '.join(arg_string_list), ']'))
    # type_annotation: typing.List
    elif isinstance(type_annotation, typing._SpecialGenericAlias):
        return type_annotation_to_string(type_annotation.__origin__)
    # type_annotation: typing.Any
    elif isinstance(type_annotation, typing._SpecialForm):
        return str(type_annotation)
    # type_annotation: ~_TS3Path
    elif isinstance(type_annotation, typing.TypeVar):
        return type_annotation_to_string(type_annotation.__bound__)
    else:
        pudb.set_trace()
