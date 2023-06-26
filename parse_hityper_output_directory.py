import argparse
import logging
import json
import os
import os.path
import sys

from collections import defaultdict

from python_file_path_from_module_search_path_and_module_name import python_file_path_from_module_search_path_and_module_name
from result_dict_from_query_dict_and_prelimary_result_dict import result_dict_from_query_dict_and_prelimary_result_dict


def parse(
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
    module_search_path: str,
    hityper_output_directory_path: str
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
    prelimary_result_dict: defaultdict[
        str, # module_name
        defaultdict[
            str, # class_name_or_global
            defaultdict[
                str, # function_name
                defaultdict[
                    str, # parameter_name_or_return
                    list[str] # type_annotation
                ]
            ]
        ]
    ] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for module_name, module_name_level_query_dict in query_dict.items():
        # python_file_path: 'hityper/module_search_path/src/meerkat/configurations/infrastructure/rest/health/registry.py'
        python_file_path: str = python_file_path_from_module_search_path_and_module_name(
            module_search_path,
            module_name
        )

        # python_file_path_without_extension: 'hityper/module_search_path/src/meerkat/configurations/infrastructure/rest/health/registry'
        python_file_path_without_extension, _ = os.path.splitext(python_file_path)

        # output_json_file_name: 'hityper_module_search_path_src_meerkat_configurations_infrastructure_rest_health_registry_INFERREDTYPES.json'
        output_json_file_name = f"{python_file_path_without_extension.replace('/', '_')}_INFERREDTYPES.json"

        output_json_file_path = os.path.join(hityper_output_directory_path, output_json_file_name)

        if os.path.isfile(output_json_file_path):
            with open(output_json_file_path, 'r') as fp:
                # output_json.keys(): dict_keys(['boot@HealthService', 'global@global', 'post_boot@HealthService'])
                output_json = json.load(fp)

                # potentially_valid_key_to_parameter_name_or_return_list_dict: {: ['container']}
                potentially_valid_key_to_parameter_name_or_return_list_dict: dict[
                    str,
                    list[str]
                ] = dict()

                for class_name_or_global, class_name_or_global_level_query_dict in module_name_level_query_dict.items():
                    # parameter_name_or_return_list: ['container']
                    for function_name, parameter_name_or_return_list in class_name_or_global_level_query_dict.items():
                        # potentially_valid_key: 'boot@HealthService'
                        potentially_valid_key: str = f'{function_name}@{class_name_or_global}'

                        if potentially_valid_key in output_json:
                            # type_prediction_dict_list: [{'category': 'arg', 'name': 'container', 'type': ['str']}, {'category': 'local', 'name': 'container', 'type': ['str']}, {'category': 'return', 'name': 'boot', 'type': ['None']}]
                            type_prediction_dict_list: list[dict] = output_json[potentially_valid_key]

                            # parameter_name_or_return_to_type_annotation_string_list_dict: {'container': ['str'], 'return': ['None']}
                            parameter_name_or_return_to_type_annotation_string_list_dict: dict[
                                str,
                                list[str]
                            ] = dict()
                            for type_prediction_dict in type_prediction_dict_list:
                                category: str = type_prediction_dict['category']
                                name: str = type_prediction_dict['name']
                                
                                if category == 'arg':
                                    parameter_name_or_return_to_type_annotation_string_list_dict[name] = type_prediction_dict['type']
                                elif category == 'return':
                                    parameter_name_or_return_to_type_annotation_string_list_dict['return'] = type_prediction_dict['type']
                            
                            for parameter_name_or_return in parameter_name_or_return_list:
                                if parameter_name_or_return in parameter_name_or_return_to_type_annotation_string_list_dict:
                                    prelimary_result_dict[module_name][class_name_or_global][function_name][parameter_name_or_return] = parameter_name_or_return_to_type_annotation_string_list_dict[parameter_name_or_return]

    return result_dict_from_query_dict_and_prelimary_result_dict(query_dict, prelimary_result_dict)


if __name__ == '__main__':
    # set up logging
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query-dict', type=str, required=True, help='Query dict, e.g. {"src.meerkat.configurations.infrastructure.rest.health.registry": {"HealthService": {"boot": ["container"]}}, "src.meerkat.data_providers.database.mongo.transformers": {"PostDocumentTransformer": {"transform_to_domain_object": ["return"]}}, "src.meerkat.domain.post.value_objects.id": {"Id": {"__init__": ["value"]}}, "src.meerkat.entrypoints.rest.post.registry": {"PostService": {"boot": ["container"]}}}')
    parser.add_argument('-m', '--module-search-path', type=str, required=True, help='Module search path, e.g. hityper/module_search_path')
    parser.add_argument('-o', '--hityper-output-directory', type=str, required=True, help='HiTyper output directory, e.g. hityper/hityper_output_directory')
    args = parser.parse_args()

    query_dict = json.loads(
        args.query_dict
    )

    result_dict = parse(query_dict, args.module_search_path, args.hityper_output_directory)

    json.dump(result_dict, sys.stdout)
