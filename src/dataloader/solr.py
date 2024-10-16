import sys
import os
import json
import requests
from pysolr import Solr
from dotenv import load_dotenv
from dataloader.mongodb import  mongodb_find_video

load_dotenv()


SOLR_URL = os.getenv("SOLR_URL")


def test_solr_connection():
    solr = Solr(SOLR_URL)
    try:
        r = solr.ping()
        status = json.loads(r).get("status")
        print(f"Connection to Solr got status {status}")
    except Exception as e:
        print(f"Could not connect to Solr. An error occurred: {e}")


def update_solr(version_id):
    solr = Solr(SOLR_URL, always_commit=True)
    video_data = mongodb_find_video(version_id)
    documents = _map_video_data(video_data)
    print(documents[0])
    solr.add(documents)


def delete_all_documents_in_solr():
    solr = Solr(SOLR_URL, always_commit=True)
    solr.delete(q='*:*')


def _map_video_data(video_data):
    subtitles = video_data.get("subtitles")
    segments = [_map_segment(segment, subtitles)
                for segment in video_data["segments"]]
    return segments


def _map_segment(segment, subtitles):
    segment["statement"] = [
        subtitle["content"]
        for subtitle in subtitles[segment["first_index"]:segment["last_index"]]]
    return segment
