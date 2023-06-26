import json
import sys

from parse_pyre_stdout import parse


query_dict = {"src.meerkat.configurations.infrastructure.rest.health.registry": {"HealthService": {"boot": ["container"]}}, "src.meerkat.data_providers.database.mongo.transformers": {"PostDocumentTransformer": {"transform_to_domain_object": ["return"]}}, "src.meerkat.domain.post.value_objects.id": {"Id": {"__init__": ["value"]}}, "src.meerkat.entrypoints.rest.post.registry": {"PostService": {"boot": ["container"]}}}

pyre_output_file_path = 'pyre/pyre_output'

result_dict = {"src.meerkat.configurations.infrastructure.rest.health.registry": {"HealthService": {"boot": {"container": []}}}, "src.meerkat.data_providers.database.mongo.transformers": {"PostDocumentTransformer": {"transform_to_domain_object": {"return": []}}}, "src.meerkat.domain.post.value_objects.id": {"Id": {"__init__": {"value": ["uuid.UUID"]}}}, "src.meerkat.entrypoints.rest.post.registry": {"PostService": {"boot": {"container": []}}}}

with open(pyre_output_file_path, 'r') as fp:
    assert parse(query_dict, fp) == result_dict
