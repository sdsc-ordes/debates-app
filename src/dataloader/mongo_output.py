import json
import os
import uuid
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

MONGO_URL = os.getenv("DEBATES_MONGO_URL")
MONGO_DB = os.getenv("DEBATES_MONGO_DB")
COLLECTION_VIDEOS = os.getenv("DEBATES_COLLECTION_VIDEOS")


def write_to_file(data, output, title):
    video_data = get_video_data(data, title)
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(video_data, file, indent=4)
    print(f"output can be found at {output}")    


def get_video_data(data, title):
    video_data = {
        "video_title": title,
        "speakers": get_speakers(data),
        "segments": get_segments(data),
        "subtitles": get_subtitles(data),
        "corrections": [],
        "video_s3_id": str(uuid.uuid4()),
        "version_id": str(uuid.uuid4()),
    }
    return video_data    


def write_to_mongodb(data, title):
    video_data = get_video_data(data, title)
    mongo_add_video(video_data)     


def mongo_get_videos():
    """Retrieve all documents from the db"""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        cursor = db[COLLECTION_VIDEOS].find({})
        documents = get_list_from_cursor(cursor)
    pprint(documents)  


def mongo_add_video(video_data):
    """Retrieve all documents from the db"""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        video_id = db[COLLECTION_VIDEOS].insert_one(video_data).inserted_id
        if video_id:
            print(f"video has been successfully added at {video_id}")          


def get_list_from_cursor(cursor):
    document_list = []
    for document in cursor:
        document_list.append(document)
    return document_list


def get_subtitles(data):
    subtitles = [{
        "index": subtitle["index"],
        "start": subtitle["start"],
        "end": subtitle["end"],
        "content": subtitle["content"],
        "segment_nr": subtitle["segment_nr"],
    } for subtitle in data]  
    return subtitles


def get_speakers(data):
    speaker_ids = {subtitle["speaker_id"] for subtitle in data}
    speakers = [{
        "speaker_id": speaker_id,
        "name": "",
        "country": "",
    } for speaker_id in speaker_ids]  
    return speakers       


def get_segments(data):
    segment_nrs = {subtitle["segment_nr"] for subtitle in data}
    segments = []
    for i, segment_nr in enumerate(segment_nrs):
        segment = get_segment(data, segment_nr)
        segments.append(segment)
    return segments

def get_segment(data, segment_nr):
    subtitles_in_segment = [
        subtitle for subtitle in data if subtitle["segment_nr"] == segment_nr
    ]
    speaker_id = subtitles_in_segment[0]["speaker_id"]
    segment_nr = subtitles_in_segment[0]["segment_nr"]
    start = min([subtitle["start"] for subtitle in subtitles_in_segment])   
    end = max([subtitle["end"] for subtitle in subtitles_in_segment]) 
    start_index = min([subtitle["index"] for subtitle in subtitles_in_segment]) 
    end_index = max([subtitle["index"] for subtitle in subtitles_in_segment]) 
    segment = {
        "speaker_id": speaker_id,
        "start": start,
        "end": end,
        "first_index": start_index,
        "last_index": end_index,
        "segment_nr": segment_nr,
    }
    return segment
