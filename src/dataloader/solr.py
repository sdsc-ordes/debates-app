import os
import json
from pysolr import Solr
from dotenv import load_dotenv

load_dotenv()


SOLR_URL = os.getenv("SOLR_URL")
SEGMENT_TYPE_TRANSLATION = "translation"
SEGMENT_TYPE_ORIGINAL = "transcript"
SEGMENT_LANGUAGE_ENGLISH = "en"


class DataloaderSolrException(Exception):
    pass


def test_solr_connection():
    solr = Solr(SOLR_URL)
    try:
        r = solr.ping()
        status = json.loads(r).get("status")
        print(f"Connection to Solr got status {status}")
    except Exception as e:
        print(f"Could not connect to Solr. An error occurred: {e}")


def update_solr(debate_data):
    solr = Solr(SOLR_URL, always_commit=True)
    documents = _map_debate_data(debate_data)
    solr.add(documents)
    print(f"Successfully inserted {len(documents)} documents into solr")


def delete_all_documents_in_solr():
    solr = Solr(SOLR_URL, always_commit=True)
    solr.delete(q='*:*')


def _map_debate_data(debate_data):
    subtitles = debate_data.get("subtitles")
    subtitles_en = debate_data.get("subtitles_en")
    debate_extras = {
        "s3_prefix": debate_data["s3_prefix"],
        "version_id": debate_data["version"]["version_id"],
        "version_original": debate_data["version"]["original"],
        "debate_type": debate_data["debate"]["type"],
        "debate_session": debate_data["debate"]["session"],
        "debate_public": debate_data["debate"]["public"],
        "debate_schedule": _map_to_solr_date(debate_data["debate"]["schedule"]),
    }
    documents = []
    for segment in debate_data["segments"]:
        document_orig = _map_segment(segment, subtitles, debate_extras, SEGMENT_TYPE_ORIGINAL)
        document_en = _map_segment(segment, subtitles_en, debate_extras, SEGMENT_TYPE_TRANSLATION)
        documents.append(document_orig)
        documents.append(document_en)
    return documents


def _map_segment(segment, subtitles, debate_extras, segment_type):
    document = {}
    document["statement"] = [
        subtitle["content"]
        for subtitle in subtitles if subtitle["segment_nr"] == segment["segment_nr"]]
    document ["statement_type"] = segment_type
    if segment_type == SEGMENT_TYPE_TRANSLATION:
        document["statement_language"] = SEGMENT_LANGUAGE_ENGLISH
    for key in segment.keys():
        document[key] = segment[key]
    for key in debate_extras.keys():
        document[key] = debate_extras[key]
    return document

def _map_to_solr_date(debate_date):
    isodate_utc = debate_date
    return isodate_utc
