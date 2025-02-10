import yaml


def parse_metadata(metadata):
    parsed_metadata = yaml.load(metadata, Loader=yaml.FullLoader)
    return parsed_metadata
