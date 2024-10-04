import typer
from dataloader import srt_parser
from dataloader import mongo_output
from logging import log


def main(srt_file: str, output: str, title: str):
    try:
        with open('input/input.srt', 'r') as f:
            data = f.read()
        processed_data = srt_parser.process_data(data)
        mongo_output.write_to_file(processed_data, output, title)    
    except Exception as e:
        print(f"An error {e} occurred")
        raise typer.Exit()


if __name__ == "__main__":
    typer.run(main)
