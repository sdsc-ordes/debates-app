import json


def write_output_to_file(processed_data, output, title):
    """write parsed video data to a json file"""
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, indent=4)
    print(f"output can be found at {output}")
