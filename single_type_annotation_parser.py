 from lark import Lark


parser = Lark(r"""
single_type_annotation: qualified_class_name | subscription | "None" | "'" single_type_annotation "'" | "\"" single_type_annotation "\""
qualified_class_name: module_name "." class_name | class_name
module_name: NAME | module_name "." NAME
class_name: NAME
subscription:  qualified_class_name "[" type_annotation_list "]"
type_annotation_list: nonempty_type_annotation_list | 
nonempty_type_annotation_list: type_annotation_list_element | type_annotation_list_element "," nonempty_type_annotation_list | type_annotation_list_element ","
type_annotation_list_element: single_type_annotation | "..." | "[" type_annotation_list "]"

%import python.NAME
%import common.WS

%ignore WS
""",
start='single_type_annotation',
parser='lalr')

single_type_annotation_with_parenthesis_to_python_file_path_dict: dict[str, str] = dict()
qualified_class_name_without_module_name_to_python_file_path_dict: dict[str, str] = dict()
empty_type_annotation_list_to_python_file_path_dict: dict[str, str] = dict()
