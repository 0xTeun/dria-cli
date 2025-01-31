import click
from terminal import DriaTerminal

@click.command()
def main():
    """Entry point for smol-dria-terminal"""
    terminal = DriaTerminal()
    terminal.run()

if __name__ == "__main__":
    main()