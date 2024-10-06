import typer
from dataloader import srt_parser
from dataloader import mongo_output
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def mongo_get():
    mongo_output.mongo_get_videos()


@app.command()
def mongo_post(
    srt_file: str,
    title: str,
):
    with open('input/input.srt', 'r') as f:
        data = f.read()
    processed_data = srt_parser.process_data(data) 
    mongo_output.write_to_mongodb(processed_data, title)    


@app.command()
def parse_srt(
    srt_file: str,
    file: str,
    title: str,
):
    with open('input/input.srt', 'r') as f:
        data = f.read()
    processed_data = srt_parser.process_data(data)
    mongo_output.write_to_file(processed_data, file, title)     


if __name__ == "__main__":
    app()
