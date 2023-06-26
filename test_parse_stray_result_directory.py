import json
import sys

from parse_stray_result_directory import parse


query_dict = {"src.meerkat.configurations.infrastructure.rest.health.registry": {"HealthService": {"boot": ["container"]}}, "src.meerkat.data_providers.database.mongo.transformers": {"PostDocumentTransformer": {"transform_to_domain_object": ["return"]}}, "src.meerkat.domain.post.value_objects.id": {"Id": {"__init__": ["value"]}}, "src.meerkat.entrypoints.rest.post.registry": {"PostService": {"boot": ["container"]}}}

module_search_absolute_path = '/home/jifengwu/dataset_investigation/stray/module_search_path'

stray_result_directory_path = 'stray/result'

result_dict = {"src.meerkat.configurations.infrastructure.rest.health.registry": {"HealthService": {"boot": {"container": []}}}, "src.meerkat.data_providers.database.mongo.transformers": {"PostDocumentTransformer": {"transform_to_domain_object": {"return": []}}}, "src.meerkat.domain.post.value_objects.id": {"Id": {"__init__": {"value": ["uuid.UUID"]}}}, "src.meerkat.entrypoints.rest.post.registry": {"PostService": {"boot": {"container": ["rest.post.registry.PostService"]}}}}

assert parse(query_dict, module_search_absolute_path, stray_result_directory_path) == result_dict
