import typer
from dataloader.parser import parse_srt_file
from dataloader.mongodb import mongodb_insert_video, mongodb_find_videos
from dataloader.file import write_output_to_file
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def mongo_get():
    mongodb_find_videos()


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
