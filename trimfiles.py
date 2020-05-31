import sys
import colorama
import click
from glob import glob
import os
import time
from datetime import datetime
from datetime import date
from collections import defaultdict

def generateFilesPerDayForHalvingPattern(k, extend=False):
    filesPerDay = []

    multiple = 1

    while True:
        filesPerDay += [k] * multiple

        if extend:
            multiple *= 2

        k //= 2
        if k == 0:
            break

    return filesPerDay

print(generateFilesPerDayForHalvingPattern(8))
print(generateFilesPerDayForHalvingPattern(7, extend=True))
print(generateFilesPerDayForHalvingPattern(6, extend=True))
print(generateFilesPerDayForHalvingPattern(5, extend=True))
print(generateFilesPerDayForHalvingPattern(1, extend=True))
sys.exit(1)

@click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
# @click.option("--filepattern", required=True, help="File glob for target files, e.g. backup*.tar")
@click.option("--deletefiles", default=False)
@click.argument("filepattern")
def hello(deletefiles, filepattern):
    """Simple program that greets NAME for a total of COUNT times.

    It features cheese. and niceness. and kits."""

    tm = time.time()
    now_date = date.fromtimestamp(tm)
    click.secho(f"now date:{now_date}")

    localTime = time.localtime(tm)
    formatTime = time.strftime('%Y-%m-%d %H:%M:%S', localTime)
    click.secho(f"curr time: {tm} {localTime} {formatTime}")

    if not "*" in filepattern:
        raise click.UsageError("File pattern must contain wildcard '*'")

    click.secho("")

    if not deletefiles:
        click.secho("Since '--deletefiles true' was not given, I will show which files would normally be deleted, but take no action.\n", fg='green')

    for _ in range(3):
        click.echo(f"😄 Hello, {filepattern}")

    # UsageException("asdasd")

    print("Del files:", deletefiles)

    found_files = glob(filepattern, recursive=True)

    found_files.sort(key=os.path.getmtime, reverse=True)

    dayAgeToFilepath = defaultdict(list)

    for fname in found_files:
        file_mod_time = os.path.getmtime(fname)
        file_mod_local_time = time.localtime(file_mod_time)
        file_format_time = time.strftime('%Y-%m-%d %H:%M:%S', file_mod_local_time)

        file_date = date.fromtimestamp(file_mod_time)

        delta_days = now_date - file_date

        print(f"A file:{fname}  time: {file_format_time} age in days: {delta_days.days}")

        dayAgeToFilepath[delta_days].append(fname)

    click.secho(f"Found map: {dayAgeToFilepath}", fg='yellow')

        # with open(fname, "r") as f:

if __name__ == '__main__':
    # hello(filepattern="Sadfsdfds")
    hello()
    # invoke(hello, args=['--filepattern', 'grimp'])
