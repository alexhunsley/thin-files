import sys
import colorama
import click
from glob import glob

@click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
# @click.option("--filepattern", required=True, help="File glob for target files, e.g. backup*.tar")
@click.option("--deletefiles", default=False)
@click.argument("filepattern")
def hello(deletefiles, filepattern):
    """Simple program that greets NAME for a total of COUNT times.

    It features cheese. and niceness. and kits."""

    if not "*" in filepattern:
        raise click.UsageError("File pattern must contain wildcard '*'")

    click.secho("")

    if not deletefiles:
        click.secho("Since '--deletefiles true' was not given, I will show which files would normally be deleted, but take no action.\n", fg='green')

    for _ in range(3):
        click.echo(f"😄 Hello, {filepattern}!")

    # UsageException("asdasd")

    print("Del files:", deletefiles)

    found_files = glob(filepattern, recursive=True)
    for fname in found_files:
        print("A file:", fname)
        # with open(fname, "r") as f:

if __name__ == '__main__':
    # hello(filepattern="Sadfsdfds")
    hello()
    # invoke(hello, args=['--filepattern', 'grimp'])
