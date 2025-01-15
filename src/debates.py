import typer
import sys
import traceback
import uvicorn
import os
from pprint import pprint
import dataloader.srt_parser as dl_parse_srt
import dataloader.yml_parser as dl_parse_yml
import dataloader.mongodb as dl_mongo
import dataloader.file as dl_file
import dataloader.solr as dl_solr
from typing_extensions import Annotated
from dataloader.s3 import s3Manager
from dataloader.api import api
from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv("API_HOST")
SUFFIX_SRT_ORIG = os.getenv("SUFFIX_SRT_ORIG")
SUFFIX_SRT_EN = os.getenv("SUFFIX_SRT_EN")
SUFFIX_METADATA = os.getenv("SUFFIX_METADATA")


cli = typer.Typer()


@cli.command()
def s3_to_mongo_solr(
    s3_prefix: Annotated[str, typer.Argument(help="s3 prefix")],
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """Get data and metadata for s3_path from S3 and add it to the Mongo DB"""
    try:
        s3 = s3Manager()
        s3_srt_path_orig = f"{s3_prefix}/{s3_prefix}-{SUFFIX_SRT_ORIG}"
        print(f"expected s3 path for original transcript {s3_srt_path_orig}")
        s3_srt_path_en = f"{s3_prefix}/{s3_prefix}-{SUFFIX_SRT_EN}"
        print(f"expected s3 path for english translation {s3_srt_path_en}")
        s3_metadata_path = f"{s3_prefix}/{s3_prefix}-{SUFFIX_METADATA}"
        print(f"expected s3 path for metadata {s3_metadata_path}")
        raw_data_en = s3.get_s3_data(s3_srt_path_en)
        raw_data_orig = s3.get_s3_data(s3_srt_path_orig)
        parsed_data_orig = dl_parse_srt.parse_subtitles(raw_data_orig)
        parsed_data_en = dl_parse_srt.parse_subtitles(raw_data_en)
        raw_metadata = s3.get_s3_data(s3_metadata_path)
        parsed_metadata = dl_parse_yml.parse_metadata(raw_metadata)
        debate_data_db = dl_mongo.mongodb_insert_debate(
            metadata=parsed_metadata, data_orig=parsed_data_orig, data_en=parsed_data_en)
        dl_solr.update_solr(debate_data_db)
    except Exception as e:
        print(f"S3 data could not be loaded into secondary databases. An exception occurred: {e}")
        _print_traceback(debug)


@cli.command()
def mongo_to_solr(
    s3_prefix: Annotated[str, typer.Argument(help="s3 prefix of a debate")],
    version_id: Annotated[str, typer.Argument(help="version_id of a debate")],
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """Get document from mongodb and add it to Solr"""
    try:
        debate_data = dl_mongo.mongodb_find_one_debate(s3_prefix, version_id)
        dl_solr.update_solr(debate_data)
    except Exception as e:
        print(f"An error occurred during mongo to solr: {e}")
        _print_traceback(debug)


@cli.command()
def parse(
    srt_file: Annotated[str, typer.Argument(help="SRT file as transcription of a debate")],
    output: Annotated[str, typer.Option(
        help="Output path: when provide the output will be written to a file"
    )],
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """parses SRT file to json output file"""
    try:
        with open(srt_file, 'r') as f:
            data = f.read()
        parsed_data = dl_parse_srt.parse_subtitles(data)
        dl_file.write_parsed_data_to_file(parsed_data, output)
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        _print_traceback(debug)


@cli.command()
def mongo_get(
    version_id: Annotated[str, typer.Option(help="version_id of debate data")] = None,
    s3_prefix: Annotated[str, typer.Option(help="s3 prefix of debate data")] = None,
    all: Annotated[bool, typer.Option(help="List all debates in the debate collection")] = False,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """Find data in Mongodb: you may use s3_prefix and version_id to filter"""
    try:
        if all:
            debate_data = dl_mongo.mongodb_find_debates()
            if debate_data:
                pprint(debate_data)
            else:
                print(f"No debate item has not been found.")
        if s3_prefix and version_id:
            debate_data = dl_mongo.mongodb_find_one_debate(s3_prefix, version_id)
            if debate_data:
                print(f"Found debate for s3_prefix {debate_data['s3_prefix']} and version_id {debate_data['version_id']}")
            else:
                print(f"No debate has not been found for s3_prefix {debate_data['s3_prefix']} and version_id {debate_data['version_id']}.")
    except Exception as e:
        print(f"An error occurred for mongodb find: {e}")
        _print_traceback(debug)


@cli.command()
def mongo_admin(
    test: Annotated[bool, typer.Option(help="Test Mongodb Connection")] = False,
    create: Annotated[bool, typer.Option(help="Create Mongodb collection with validation schema")] = False,
    delete: Annotated[bool, typer.Option(help="Delete all documents from Mongodb collection")] = False,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """Test Mongodb connection, Delete all data from Mongodb, Create Collection with Schema"""
    if test:
        try:
            dl_mongo.mongodb_test_connection()
            print
        except Exception as e:
            print(f"An error occurred for mongodb connection: {e}")
            _print_traceback(debug)
    if delete:
        try:
            dl_mongo.mongodb_delete_debates()
        except Exception as e:
            print(f"An error for deleting debates from mongodb: {e}")
            _print_traceback(debug)
    if create:
        try:
            dl_mongo.mongodb_create_debate_collection_with_schema()
        except Exception as e:
            print(f"An error occurred when creating collection with schema validation on mongodb: {e}")
            _print_traceback(debug)


@cli.command()
def solr_admin(
    test: Annotated[bool, typer.Option(help="Test Solr Connection")] = False,
    delete: Annotated[bool, typer.Option(help="Delete all documents from Solr")] = False,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """Test Solr Connection, Delete all data from Solr"""
    if test:
        try:
            dl_solr.test_solr_connection()
        except Exception as e:
                    print(f"An error occurred for solr connection: {e}")
                    _print_traceback(debug)
    if delete:
        try:
            dl_solr.delete_all_documents_in_solr()
        except Exception as e:
                    print(f"An error occurred when deleting documents from solr: {e}")
                    _print_traceback(debug)


@cli.command()
def s3_admin(
    test: Annotated[bool, typer.Option(help="Test S3 Connection")] = False,
    list: Annotated[bool, typer.Option(help="List S3 objects")] = False,
    prefix: Annotated[str, typer.Option(help="List Objects for a prefix")] = "",
    path: Annotated[str, typer.Option(help="Get data for a path")] = "",
    download: Annotated[str, typer.Option(help="Download for a path")] = "",
    prod: Annotated[bool, typer.Option(help="Use production S3")] = False,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
    file: Annotated[str, typer.Option(help="Output file")] = False,
):
    """Test S3 connection, list data on S3, get data by s3_path
    """
    if test:
        try:
            s3 = s3Manager(prod)
            s3.test_connection()
        except Exception as e:
            print(f"S3 connection could not be established. An exception occurred: {e}")
            _print_traceback(debug)
    if list:
        try:
            s3 = s3Manager(prod)
            s3.list_bucket_content(prefix)
        except Exception as e:
            print(f"The S3 objects could not be listed. An exception occurred: {e}")
            _print_traceback(debug)
    if path:
        try:
            s3 = s3Manager(prod)
            data = s3.get_s3_data(path)
            print(data)
        except Exception as e:
            print(f"The data for s3 path {path} could not be retrieved. An exception occurred: {e}")
            _print_traceback(debug)
    if download:
        if not file:
            print(f"please provide output file name with --file")
        try:
            s3 = s3Manager(prod)
            s3.download_s3_data(download, file)
        except Exception as e:
            print(f"The data for s3 path {download} could not be downloaded. An exception occurred: {e}")
            _print_traceback(debug)

def _print_traceback(debug):
    if debug:
        traceback.print_exc()


@cli.command()
def serve():
    """
    Start the FastAPI server.
    """
    uvicorn.run(api, host=API_HOST, port=8000)


if __name__ == "__main__":
    cli()
