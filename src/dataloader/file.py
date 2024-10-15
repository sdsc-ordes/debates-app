import json
import re
from datetime import datetime, timezone
DATE_PATTERN = "\b\d{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\b"


def write_output_to_file(processed_data, output):
    """write parsed video data to a json file"""
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, indent=4)
    print(f"output can be found at {output}")


def extract_iso_date_from_filename(filename: str):
    """file name is assumed as HRC_20220328.srt"""
    match = re.search(DATE_PATTERN, filename)
    if match:
        date_part = match.group(1)
        date_obj = datetime.strptime(date_part, '%Y%m%d')
        date_obj = date_obj.replace(tzinfo=timezone.utc)
        return date_obj.isoformat()
    else:
        return None
