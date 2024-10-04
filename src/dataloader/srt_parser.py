from srt import parse


def process_data(data):
    subtitles_raw = parse(data)
    subtitles_processed = []
    for subtitle_raw in subtitles_raw:
        process_subtitle(subtitle_raw)
    return subtitles_processed

    
def process_subtitle(subtitle_raw):
    """Subtitle(index=142, start=datetime.timedelta(seconds=1365, microseconds=609000), 
    end=datetime.timedelta(seconds=1368, microseconds=672000), content='[SPEAKER_06]: 
    With this, I conclude the 48th meeting of the 49th session.', proprietary='')"""
    print(subtitle_raw)
