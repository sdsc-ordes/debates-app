import json
import re
from datetime import datetime, timezone
DATE_PATTERN = "\d{8}"


def write_output_to_file(processed_data, output):
    """write parsed video data to a json file"""
    with open(output, 'w', encoding='utf-8') as file:
        if "_id" in processed_data.keys():
            processed_data["_id"] = str(processed_data["_id"])
        json.dump(processed_data, file, indent=4)
    print(f"output can be found at {output}")


def extract_iso_date_from_filename(filepath: str):
    """file name is assumed as HRC_20220328.srt"""
    try:
        filename = filepath.split("/")[-1]
        match = re.search(DATE_PATTERN, filename)
        if match:
            date_part = match[0]
            date_obj = datetime.strptime(date_part, '%Y%m%d')
            date_obj = date_obj.replace(tzinfo=timezone.utc)
            return date_obj.isoformat()
        else:
            return None
    except Exception as e:
        print(f"date could not be derived from filename: an exception occurred{e}")
        return None
