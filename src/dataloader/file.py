import json
import os


def write_parsed_data_to_file(parsed_data, output):
    """write parsed video data to a json file"""
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, indent=4)
    print(f"output can be found at {output}")


def get_data_from_file(filepath):
    """reads data from a file and returns the data"""
    with open(filepath, "r") as file:
        data = file.read()
    return data
