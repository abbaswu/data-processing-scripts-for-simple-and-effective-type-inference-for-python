from collections import defaultdict


def result_dict_from_query_dict_and_prelimary_result_dict(
    query_dict: dict[
        str, # module_name
        dict[
            str, # class_name_or_global
            dict[
                str, # function_name
                list[
                    str # parameter_name_or_return
                ]
            ]
        ]
    ],
    prelimary_result_dict: defaultdict[
        str, # module_name
        defaultdict[
            str, # class_name_or_global
            defaultdict[
                str, # function_name
                defaultdict[
                    str, # parameter_name_or_return
                    list[
                        str # type_annotation_string
                    ] 
                ]
            ]
        ]
    ]
) -> dict[
    str, # module_name
    dict[
        str, # class_name_or_global
        dict[
            str, # function_name
            dict[
                str, # parameter_name_or_return
                list[
                    str # type_annotation_string
                ]
            ]
        ]
    ]
]:
    result_dict: dict[
        str, # module_name
        dict[
            str, # class_name_or_global
            dict[
                str, # function_name
                dict[
                    str, # parameter_name_or_return
                    list[
                        str # type_annotation_string
                    ]
                ]
            ]
        ]
    ] = dict()

    for module_name, module_name_level_query_dict in query_dict.items():
        module_name_level_result_dict = result_dict[module_name] = dict()
        for class_name_or_global, class_name_or_global_level_query_dict in module_name_level_query_dict.items():
            class_name_or_global_level_result_dict = module_name_level_result_dict[class_name_or_global] = dict()
            for function_name, parameter_name_or_return_list in class_name_or_global_level_query_dict.items():
                function_name_level_result_dict = class_name_or_global_level_result_dict[function_name] = dict()
                for parameter_name_or_return in parameter_name_or_return_list:
                    function_name_level_result_dict[parameter_name_or_return] = prelimary_result_dict[module_name][class_name_or_global][function_name][parameter_name_or_return]

    return result_dict
