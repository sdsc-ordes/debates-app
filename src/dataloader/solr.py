import os
import json
from datetime import timezone
from pysolr import Solr
from dotenv import load_dotenv

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


def update_solr(video_data):
    solr = Solr(SOLR_URL, always_commit=True)
    documents = _map_video_data(video_data)
    solr.add(documents)


def delete_all_documents_in_solr():
    solr = Solr(SOLR_URL, always_commit=True)
    solr.delete(q='*:*')


def _map_video_data(video_data):
    subtitles = video_data.get("subtitles")
    video_date = _map_to_solr_date(video_data["debate"]["schedule"])
    segments = [_map_segment(segment, subtitles, video_date)
                for segment in video_data["segments"]]
    return segments


def _map_segment(segment, subtitles, schedule):
    segment["statement"] = [
        subtitle["content"]
        for subtitle in subtitles if subtitle["segment_nr"] == segment["segment_nr"]]
    segment["date"] = schedule
    return segment

def _map_to_solr_date(video_date):
    isodate_utc = video_date.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    return isodate_utc
