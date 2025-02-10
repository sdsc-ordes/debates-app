from typing import List, Dict

SUBTITLE_TYPE_TRANSCRIPT = "transcript"
SUBTITLE_TYPE_TRANSLATION = "translation"
SUBTITLE_TYPE_TRANSCRIPT_EDITED = "transcript_edited"
SUBTITLE_TYPE_TRANSLATION_EDITED = "translation_edited"


def merge_and_segment(data_orig: List[Dict], data_en: List[Dict]) -> List[Dict]:
    # Combine data_orig and data_en
    combined = data_orig + data_en

    # Sort by start time
    combined.sort(key=lambda x: x['start'])

    # Merge and create segments
    segments = []
    current_speaker = None
    segment_start = None
    segment_end = None
    segment_nr = 1  # Start segment numbering at 1

    for entry in combined:
        speaker = entry['speaker_id']
        start = entry['start']
        end = entry['end']

        if speaker != current_speaker:
            # Save the previous segment if it exists
            if current_speaker is not None:
                segments.append({
                    'segment_nr': segment_nr,
                    'speaker_id': current_speaker,
                    'start': segment_start,
                    'end': segment_end
                })
                segment_nr += 1  # Increment segment number

            # Start a new segment
            current_speaker = speaker
            segment_start = start
            segment_end = end
        else:
            # Extend the current segment
            segment_end = max(segment_end, end)

    # Add the last segment
    if current_speaker is not None:
        segments.append({
            'segment_nr': segment_nr,
            'speaker_id': current_speaker,
            'start': segment_start,
            'end': segment_end
        })

    return segments

def get_speakers_from_segments(segments):
    # Extract a unique list of speaker dictionaries
    seen_speakers = set()
    unique_speakers = []

    for segment in segments:
        speaker_id = segment["speaker_id"]
        if speaker_id not in seen_speakers:
            seen_speakers.add(speaker_id)
            unique_speakers.append({"speaker_id": speaker_id})
    return unique_speakers


def assign_segments_to_subtitles(subtitles, segments):
    for subtitle in subtitles:
        # Find the segment where the subtitle falls within the timeframe
        for segment in segments:
            if segment["start"] <= subtitle["start"] <= segment["end"]:
                subtitle["segment_nr"] = segment["segment_nr"]
                break
        else:
            # If no segment is found, assign None or another default value
            subtitle["segment_nr"] = None
    return subtitles
