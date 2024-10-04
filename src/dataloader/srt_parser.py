import re
from srt import parse, SRTParseError


def process_data(data):
    subtitles_raw = parse(data)
    subtitles_processed = []
    segment_nr = 0
    speaker = None

    for subtitle in subtitles_raw:
        subtitle_dict = process_subtitle(subtitle)
        current_speaker = subtitle_dict["speaker"]
        if current_speaker !=  speaker:
            segment_nr += 1  
            speaker = current_speaker
        subtitle_dict["segment_nr"] = segment_nr    
        subtitles_processed.append(subtitle_dict)   
    return subtitles_processed

    
def process_subtitle(subtitle):
    speaker, fragment = get_speaker(subtitle.content)
    subtitle_dict = {
        "index": subtitle.index,
        "start": subtitle.start.total_seconds(),
        "end": subtitle.end.total_seconds(),
        "fragment": fragment,
        "speaker": speaker,
    } 
    return subtitle_dict

def get_speaker(content):
    """
    expected '[SPEAKER_06]: some text ...'
    """
    match = re.match(r"\[(SPEAKER_\d+)\]:\s*(.*)", content)
    if match:
        speaker = match.group(1)  
        fragment = match.group(2)
        return speaker, fragment
