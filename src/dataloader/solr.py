import os
import json
from pysolr import Solr
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import dataloader.merge as merge

load_dotenv()


SOLR_URL = os.getenv("SOLR_URL")
SOLR_SELECT_URL = f"{SOLR_URL}select"

class FacetFilter(BaseModel):
    facetField: str
    facetValue: str


class SolrRequest(BaseModel):
    queryTerm: str
    sortBy: str
    facetFields: List[str]
    facetFilters: List[FacetFilter]


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


def update_speakers(s3_prefix, speakers):
    for speaker in speakers:
        speaker_id = speaker["speaker_id"]
        speaker_name = speaker.get("name", None)
        speaker_role_tag = speaker.get("role_tag", None)

        # Find the document using the composite query
        query = f'speaker_id:{speaker_id} AND s3_prefix:{s3_prefix}'
        solr = Solr(SOLR_URL, always_commit=True)
        results = solr.search(query)
        if results.hits > 0:
            # Prepare the update payload
            for doc in results:
                updated_doc = {
                    "id": doc["id"],
                    "speaker_name": {"set": speaker_name},
                    "speaker_role_tag": {"set": speaker_role_tag}
                }
                solr.add([updated_doc])


def update_segment(s3_prefix, segment_nr, subtitles, subtitle_type):
    statement = _get_statement_from_subtitles(segment_nr, subtitles)
    # Find the document using the composite query
    query = f'statement_type:{subtitle_type} AND s3_prefix:{s3_prefix} AND segment_nr:{segment_nr}'
    solr = Solr(SOLR_URL, always_commit=True)
    results = solr.search(query)
    if results.hits > 0:
        # Prepare the update payload
        for doc in results:
            updated_doc = {
                "id": doc["id"],
                "statement": {"set": statement},
            }
            result = solr.add([updated_doc])


def search_solr(solr_request: SolrRequest):
    """Fetch search results from Solr"""
    solr = Solr(SOLR_URL, timeout=10)

    params = {
        "wt": "json",
        "indent": "true",
        "df": "statement",
        "hl": "true" if solr_request.queryTerm else "false",
        "hl.snippets": 10,
        "rows": 100,
        "start": 0,
    }

    # Add facet fields if provided
    if solr_request.facetFields:
        params["facet"] = "true"
        params["facet.field"] = solr_request.facetFields  # List of facet fields

    # Add facet filters (fq) if provided
    if solr_request.facetFilters:
        params["fq"] = [
            f'{filter.facetField}:"{filter.facetValue}"' for filter in solr_request.facetFilters
        ]

    # Add sorting if provided
    if solr_request.sortBy:
        params["sort"] = solr_request.sortBy

    # Pass `queryTerm` as the first argument
    result = solr.search(solr_request.queryTerm if solr_request.queryTerm else "*:*", **params)

    return result


def _get_statement_from_subtitles(segment_nr, subtitles):
    subtitles_for_segment = [
        subtitle["content"]
        for subtitle in subtitles
        if subtitle["segment_nr"] == segment_nr
        and subtitle.get("content")
    ]
    return subtitles_for_segment


def _map_debate_data(debate_data):
    subtitles = debate_data.get("subtitles")
    subtitles_en = debate_data.get("subtitles_en")
    segments = debate_data.get("segments")
    debate_extras = {
        "s3_prefix": debate_data["debate"]["s3_prefix"],
        "debate_type": debate_data["debate"]["type"],
        "debate_session": debate_data["debate"]["session"],
        "debate_public": debate_data["debate"]["public"],
        "debate_schedule": _map_to_solr_date(debate_data["debate"]["schedule"]),
    }
    documents = []
    for segment in segments:
        document_orig = _map_segment(
            segment=segment,
            subtitles=subtitles,
            debate_extras=debate_extras,
            segment_type=merge.SUBTITLE_TYPE_TRANSCRIPT
        )
        if document_orig:
            documents.append(document_orig)
        document_en = _map_segment(
            segment=segment,
            subtitles=subtitles_en,
            debate_extras=debate_extras,
            segment_type=merge.SUBTITLE_TYPE_TRANSLATION
        )
        if document_en:
            documents.append(document_en)
    return documents


def _map_segment(segment, subtitles, debate_extras, segment_type):
    document = {}
    document["statement"] = [
        subtitle["content"]
        for subtitle in subtitles if subtitle["segment_nr"] == segment["segment_nr"]]
    if not document["statement"]:
        return None
    document ["statement_type"] = segment_type
    if segment_type == merge.SUBTITLE_TYPE_TRANSLATION:
        document["statement_language"] = "en"
    else:
        document["statement_language"] = ""
    for key in segment.keys():
        document[key] = segment[key]
    for key in debate_extras.keys():
        document[key] = debate_extras[key]
    return document

def _map_to_solr_date(debate_date):
    isodate_utc = debate_date
    return isodate_utc
