import typer
from dataloader import srt_parser


def main(name: str):
    print(f"Hello {name}")
    srt_parser.process_data()


if __name__ == "__main__":
    typer.run(main)
