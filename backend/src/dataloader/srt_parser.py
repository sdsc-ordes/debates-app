import re
from srt import parse as ext_srt_parse


class SrtParseException(Exception):
    pass


def parse_subtitles(data):
    """parse srt file into a subtitle dictionary"""
    subtitles_raw = ext_srt_parse(data)
    subtitles_processed = []
    segment_nr = 0
    speaker_id = None
    for subtitle in subtitles_raw:
        processed_subtitle = _process_subtitle(subtitle)
        current_speaker_id = processed_subtitle["speaker_id"]
        if current_speaker_id !=  speaker_id:
            segment_nr += 1
            speaker_id = current_speaker_id
        subtitles_processed.append(processed_subtitle)
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
    raise SrtParseException("No speakers in transcript")
