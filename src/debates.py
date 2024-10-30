import typer
import traceback
from pprint import pprint
from datetime import datetime
import dataloader.srt_parser as dl_parse_srt
import dataloader.yml_parser as dl_parse_yml
import dataloader.mongodb as dl_mongo
import dataloader.file as dl_file
import dataloader.solr as dl_solr
from typing_extensions import Annotated
from dataloader.s3 import s3Manager


app = typer.Typer()


@app.command()
def s3_to_mongo(
    srt_path: Annotated[str, typer.Argument(help="s3 srt file path")],
    metadata_path: Annotated[str, typer.Argument(help="s3 metadata path")],
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
    dev: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """get video srt file from S3 and add it to the Mongo DB after parsing it"""
    try:
        s3 = s3Manager(dev)
        raw_data = s3.get_s3_data(srt_path)
        parsed_data = dl_parse_srt.parse_subtitles(raw_data)
        raw_metadata = s3.get_s3_data(metadata_path)
        parsed_metadata = dl_parse_yml.parse_metadata(raw_metadata)
        video_id = dl_mongo.mongodb_insert_video(parsed_data, parsed_metadata)
        print(f"video has been successfully added at {video_id}")
    except Exception as e:
        print(f"S3 data could not be loaded to mongodb. An exception occurred: {e}")
        _print_traceback(debug)


@app.command()
def parse(
    srt_file: Annotated[str, typer.Argument(help="SRT file as transcription of a video")],
    output: Annotated[str, typer.Option(
        help="Output path: when provide the output will be written to a file"
    )],
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """parses SRT file to json output"""
    try:
        with open(srt_file, 'r') as f:
            data = f.read()
        parsed_data = dl_parse_srt.parse_subtitles(data)
        dl_file.write_parsed_data_to_file(parsed_data, output)
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        _print_traceback(debug)


@app.command()
def mongo_get(
    version_id: Annotated[str, typer.Argument(help="version_id of a video")] = None,
    s3_prefix: Annotated[str, typer.Argument(help="s3 prefix of a video without the dash")] = None,
    output: Annotated[str, typer.Option(
        help="Output path: when provide the output will be written to a file"
    )] = None,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """find a video by its version_id in the mongo db"""
    try:
        video_data = dl_mongo.mongodb_find(version_id, s3_prefix)
        if video_data:
            dl_file.write_output_to_file(video_data, output)
        else:
            print(f"No video has not been found.")
    except Exception as e:
        print(f"An error occurred for mongodb find: {e}")
        _print_traceback(debug)


@app.command()
def mongo_admin(
    delete: Annotated[bool, typer.Option(help="Delete all documents from Solr")] = False,
    create: Annotated[bool, typer.Option(help="Delete all documents from Solr")] = False,
    test: Annotated[bool, typer.Option(help="Test Mongodb Connection")] = False,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """admin tasks on the Solr Db: delete all video instances or test connection"""
    if delete:
        try:
            dl_mongo.mongodb_delete_videos()
        except Exception as e:
            print(f"An error for deleting videos from mongodb: {e}")
            _print_traceback(debug)
    if test:
        try:
            dl_mongo.mongodb_test_connection()
        except Exception as e:
            print(f"An error occurred for mongodb connection: {e}")
            _print_traceback(debug)
    if list:
        try:
            dl_mongo.mongodb_find_videos()
        except Exception as e:
            print(f"An error occurred when listing videos from mongodb: {e}")
            _print_traceback(debug)
    if create:
        try:
            dl_mongo.mongodb_create_video_collection_with_schema()
        except Exception as e:
            print(f"An error occurred when listing videos from mongodb: {e}")
            _print_traceback(debug)


@app.command()
def solr_admin(
    test: Annotated[bool, typer.Option(help="Test Solr Connection")] = False,
    delete: Annotated[bool, typer.Option(help="Delete all documents from Solr")] = False,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    """admin tasks on the Solr Db: delete all instances or test connection"""
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


@app.command()
def s3_admin(
    test: Annotated[bool, typer.Option(help="Test S3 Connection")] = False,
    list: Annotated[bool, typer.Option(help="List S3 Objects")] = False,
    prefix: Annotated[str, typer.Option(help="List Objects for a prefix")] = "",
    path: Annotated[str, typer.Option(help="Get data for a path")] = "",
    dev: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
    print: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
    debug: Annotated[bool, typer.Option(help="Print traceback on exception")] = False,
):
    if test:
        try:
            s3 = s3Manager(dev)
            s3.test_connection()
        except Exception as e:
            print(f"S3 connection could not be established. An exception occurred: {e}")
            _print_traceback(debug)
    if list:
        try:
            s3 = s3Manager(dev)
            s3.list_bucket_content(prefix)
        except Exception as e:
            print(f"S3 video objects could not be listed. An exception occurred: {e}")
            _print_traceback(debug)
    if path:
        try:
            s3 = s3Manager(dev)
            data = s3.get_s3_data(path)
            if print:
                print(data)
        except Exception as e:
            print(f"S3 video objects could not be listed. An exception occurred: {e}")
            _print_traceback(debug)

def _print_traceback(debug):
    if debug:
        traceback.print_exc()


if __name__ == "__main__":
    app()
