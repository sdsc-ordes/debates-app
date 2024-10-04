import json


def write_to_file(data, output, title):
    video = {
        "video_title": title,
        "subtitles": data,
    }
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(video, file, indent=4)
