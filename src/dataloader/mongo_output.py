import json
import os
import uuid
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("DEBATES_MONGO_URL")
MONGO_DB = os.getenv("DEBATES_MONGO_DB")
COLLECTION_VIDEOS = os.getenv("DEBATES_COLLECTION_VIDEOS")


def write_to_file(data, output, title):
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(video_data(data, title), file, indent=4)


def video_data(data, title):
    video_data = {
        "video_title": title,
        "subtitles": data,
        "video_s3_id": str(uuid.uuid4()),
        "version_id": str(uuid.uuid4()),
        "original": True,
        "data_created": datetime.now(timezone.utc),
        "data_updated": datetime.now(timezone.utc),
    }
    return video_data    


def write_to_mongodb(data, title):
    mongo_add_video(video_data(data, title))     


def mongo_get_videos():
    """Retrieve all documents from the db"""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        cursor = db[COLLECTION_VIDEOS].find({})
        documents = get_list_from_cursor(cursor)
    print(documents)  


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
