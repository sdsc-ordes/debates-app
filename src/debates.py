import typer
from dataloader.parser import parse_srt_file
from dataloader.mongodb import mongodb_insert_video, mongodb_find_video
from dataloader.file import write_output_to_file
from dataloader.solr import test_solr_connection, update_solr
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def mongo_find_one(
    version_id: Annotated[str, typer.Argument(help="version_id of a video")]
):
    """find a video by its version_id in the mongo db"""
    mongodb_find_video(version_id)


@app.command()
def mongo_post(
    srt_file: str,
    title: str,
):
    with open('input/input.srt', 'r') as f:
        data = f.read()
    processed_data = parse_srt_file(data)
    mongodb_insert_video(processed_data, title)


@app.command()
def solr_add(
    version_id: Annotated[str, typer.Argument(help="version_id of a video")],
):
    update_solr(version_id)


@app.command()
def solr_admin(
    testconn: Annotated[bool, typer.Option(help="Test Solr Connection.")] = False,
):
    if testconn: 
        test_solr_connection()


@app.command()
def parse_srt(
    srt_file: str,
    file: str,
    title: str,
):
    with open('input/input.srt', 'r') as f:
        data = f.read()
    processed_data = parse_srt_file(data)
    write_output_to_file(processed_data, file, title)


if __name__ == "__main__":
    app()
