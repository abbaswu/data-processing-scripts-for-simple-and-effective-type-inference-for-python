import ast


def get_parameter_name_list_from_ast_function_def(ast_function_def: ast.FunctionDef) -> list[str]:
    parameter_name_list: list[str] = []

    args: ast.arguments = ast_function_def.args

    for posonlyarg in args.posonlyargs:
        parameter_name_list.append(posonlyarg.arg)

    for arg in args.args:
        parameter_name_list.append(arg.arg)

    vararg: ast.arg | None = args.vararg
    if vararg is not None:
        parameter_name_list.append(vararg.arg)

    for kwonlyarg in args.kwonlyargs:
        parameter_name_list.append(kwonlyarg.arg)

    kwarg: ast.arg | None = args.kwarg
    if kwarg is not None:
        parameter_name_list.append(kwarg.arg)

    return parameter_name_list
