import typer
from dataloader import srt_parser
from dataloader import mongo_output
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def mongo_get():
    try:
        mongo_output.mongo_get_videos()
    except Exception as e:
        print(f"An error {e} occurred")
        raise typer.Exit()


@app.command()
def mongo_post(
    srt_file: str,
    title: str,
):
    try:
        with open('input/input.srt', 'r') as f:
            data = f.read()
        processed_data = srt_parser.process_data(data) 
        mongo_output.write_to_mongodb(processed_data, title)    
    except Exception as e:
        print(f"An error {e} occurred")
        raise typer.Exit()


@app.command()
def parse_srt(
    srt_file: str,
    file: str,
    title: str,
):
    try:
        mongo_output.mongo_get_videos()
        with open('input/input.srt', 'r') as f:
            data = f.read()
        processed_data = srt_parser.process_data(data)
        mongo_output.write_to_file(processed_data, file, title)   
    except Exception as e:
        print(f"An error {e} occurred")
        raise typer.Exit()    


if __name__ == "__main__":
    app()


app = typer.Typer()


@app.command()
def create():
    print("Creating user: Hiro Hamada")


@app.command()
def delete():
    print("Deleting user: Hiro Hamada")


if __name__ == "__main__":
    app()    

