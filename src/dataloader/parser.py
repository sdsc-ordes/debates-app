import re
from srt import parse


def parse_srt_file(data):
    """parse srt file into a subtitle dictionary"""
    subtitles_raw = parse(data)
    subtitles_processed = []
    segment_nr = 0
    speaker_id = None

    for subtitle in subtitles_raw:
        subtitle_dict = _process_subtitle(subtitle)
        current_speaker_id = subtitle_dict["speaker_id"]
        if current_speaker_id !=  speaker_id:
            segment_nr += 1
            speaker_id = current_speaker_id
        subtitle_dict["segment_nr"] = segment_nr
        subtitles_processed.append(subtitle_dict)
    return subtitles_processed


def _process_subtitle(subtitle):
    speaker_id, content = _get_speaker(subtitle.content)
    subtitle_dict = {
        "index": subtitle.index,
        "start": subtitle.start.total_seconds(),
        "end": subtitle.end.total_seconds(),
        "content": content,
        "speaker_id": speaker_id,
    }
    return subtitle_dict


def _get_speaker(content):
    """
    expected '[SPEAKER_06]: some text ...'
    """
    match = re.match(r"\[(SPEAKER_\d+)\]:\s*(.*)", content)
    if match:
        speaker_id = match.group(1)
        content = match.group(2)
        return speaker_id, content
