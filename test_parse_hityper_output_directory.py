import json
import sys

from parse_hityper_output_directory import parse


query_dict = {"src.meerkat.configurations.infrastructure.rest.health.registry": {"HealthService": {"boot": ["container"]}}, "src.meerkat.data_providers.database.mongo.transformers": {"PostDocumentTransformer": {"transform_to_domain_object": ["return"]}}, "src.meerkat.domain.post.value_objects.id": {"Id": {"__init__": ["value"]}}, "src.meerkat.entrypoints.rest.post.registry": {"PostService": {"boot": ["container"]}}}

module_search_path = 'hityper/module_search_path'

hityper_output_directory_path = 'hityper/hityper_output_directory'

result_dict = {"src.meerkat.configurations.infrastructure.rest.health.registry": {"HealthService": {"boot": {"container": ["str"]}}}, "src.meerkat.data_providers.database.mongo.transformers": {"PostDocumentTransformer": {"transform_to_domain_object": {"return": []}}}, "src.meerkat.domain.post.value_objects.id": {"Id": {"__init__": {"value": ["str"]}}}, "src.meerkat.entrypoints.rest.post.registry": {"PostService": {"boot": {"container": ["str"]}}}}

assert parse(query_dict, module_search_path, hityper_output_directory_path) == result_dict
