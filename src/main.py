import typer
from dataloader import srt_parser


def main(srt_file: str):
    with open('input/input.srt', 'r') as f:
        data = f.read()
    output = srt_parser.process_data(data)


if __name__ == "__main__":
    typer.run(main)
