import typer
from datetime import datetime
from dataloader.parser import parse_srt_file
from dataloader.mongodb import mongodb_insert_video, mongodb_find_video
from dataloader.file import write_output_to_file, extract_iso_date_from_filename
from dataloader.solr import test_solr_connection, update_solr, delete_all_documents_in_solr
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def mongo_find_one(
    version_id: Annotated[str, typer.Argument(help="version_id of a video")]
):
    """find a video by its version_id in the mongo db"""
    mongodb_find_video(version_id)


@app.command()
def mongo_add(
    srt_file: Annotated[str, typer.Argument(help="SRT file as transcription of a video")],
):
    """An srt file is parsed and then added to the mongo db as a single document.
    The video_id that the mongodb generated when inserting the video is returned."""
    with open(srt_file, 'r') as f:
        data = f.read()
    date = extract_iso_date_from_filename(srt_file)
    if not date:
        print(
            f"The date for the video could not be derived from the filename {srt_file}.\n",
            "- It is expected as YYYYMMDD in the name of the file, such as HRC_20220328.srt.\n",
            "- Fix this and run the command again."
        )
        raise typer.Exit()
    processed_data = parse_srt_file(data)
    video_id = mongodb_insert_video(processed_data, date)
    print(f"video has been successfully added at {video_id}")


@app.command()
def solr_add(
    version_id: Annotated[str, typer.Argument(help="version_id of a video")],
):
    update_solr(version_id)


@app.command()
def solr_admin(
    test: Annotated[bool, typer.Option(help="Test Solr Connection")] = False,
    delete: Annotated[bool, typer.Option(help="Delete all documents from Solr")] = False,
):
    if test:
        test_solr_connection()
    if delete:
        delete_all_documents_in_solr()


@app.command()
def parse(
    srt_file: Annotated[str, typer.Argument(help="SRT file as transcription of a video")],
    output: Annotated[str, typer.Option(
        help="Output path: when provide the output will be written to a file"
    )],
):
    """parses SRT file to json output"""
    with open(srt_file, 'r') as f:
        data = f.read()
    processed_data = parse_srt_file(data)
    write_output_to_file(processed_data, output)


if __name__ == "__main__":
    app()
