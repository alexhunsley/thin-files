import sys
import colorama
import click
from glob import glob
import os
import time
from datetime import datetime
from datetime import date
from collections import defaultdict, namedtuple
import pprint

# print('\033[31m' + 'some red text')
# sys.exit(1)

def generateFilesPerDayForHalvingPattern(k, extend=False):
    if k < 1:
        return []

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

Filetime = namedtuple('Filetime', 'filename mod_time local_mod_time formatted_time delta_days')

# print(generateFilesPerDayForHalvingPattern(8))
# print(generateFilesPerDayForHalvingPattern(7, extend=True))
# print(generateFilesPerDayForHalvingPattern(6, extend=True))
# print(generateFilesPerDayForHalvingPattern(5, extend=True))
# print(generateFilesPerDayForHalvingPattern(1, extend=True))
# sys.exit(1)

# TOMORROW: why is halving start count going in as extend param?!

# raise a UsageError if given options are not valid
def validateOptions(halving_start_count, extended_halving_start_count, max_file_counts, filepattern):
    modesSpecifiedCount = 0
    if max_file_counts != None:
        modesSpecifiedCount += 1
    
    if halving_start_count != None:
        modesSpecifiedCount += 1

    if extended_halving_start_count != None:
        modesSpecifiedCount += 1

    if modesSpecifiedCount > 1:
        raise click.UsageError(f"You must specify only one of --max-file-counts, --halving-start-count, or --extended-halving-start-count.")

    # we must if max_file_counts != None' in first condition below, and not just 'if max_file_counts',
    # since the latter is false when it is an empty string.
    if max_file_counts != None and len(max_file_counts) == 0:
        raise click.UsageError(f"Empty string given for --max-file-counts. It be should a comma separated list of integers > 0, for example '4,2,1'.")


# raises a UsageError if given params not valid
def parse_max_file_counts(max_file_counts):
    file_counts = max_file_counts.split(',')

    if not file_counts:
        raise click.UsageError(f"Bad value given for --max-file-counts. It be should a comma separated list of integers > 0, for example '4,2,1'.")

    try:
        file_counts = [int(x) for x in file_counts]
    except:
        raise click.UsageError(f"Bad value '{max_file_counts}' given for --max-file-counts. It be should a comma separated list of integers > 0, for example '4,2,1'.")

    for c in file_counts:
        if c < 1:
            raise click.UsageError(f"Bad value '{max_file_counts}' given in --max-file-counts. It be should a comma separated list of integers > 0, for example '4,2,1'.")

    print(f"Got max file counts: {file_counts}")
    return file_counts

def parse_starting_count(starting_count_str, option_name):
    raiseError = False

    try:
        starting_count = int(starting_count_str)
        assert(starting_count > 0)
    except:
        raiseError = True

    # if starting_count < 1:
    #     raiseError = True

    if raiseError:
        raise click.UsageError(f"Bad starting count value '{starting_count_str}' given for {option_name}. It be should an integer > 0.")


    return starting_count

@click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
# @click.option("--filepattern", required=True, help="File glob for target files, e.g. backup*.tar")
@click.option("--deletefiles", default=False)
@click.option("--halving-start-count")
@click.option("--extended-halving-start-count")
@click.option("--max-file-counts")
@click.argument("filepattern")
def hello(deletefiles, halving_start_count, extended_halving_start_count, max_file_counts, filepattern):
    """Thin out target files by maximum files per day. Typically used for backup or save files."""

    print("Halving:", halving_start_count, " ext halving:", extended_halving_start_count)

    print("MFC:", max_file_counts, "end isNone:", max_file_counts == None)

    validateOptions(halving_start_count, extended_halving_start_count, max_file_counts, filepattern)


    # print(f"qwqw: {max_file_counts}X {len(max_file_counts)}")

    file_counts_per_day = None

    if max_file_counts:
        file_counts_per_day = parse_max_file_counts(max_file_counts)
    elif halving_start_count:
        start_files_per_day_value = parse_starting_count(halving_start_count, "--halving-start-count")
        file_counts_per_day = generateFilesPerDayForHalvingPattern(start_files_per_day_value)
    else:
        start_files_per_day_value = parse_starting_count(extended_halving_start_count, "--extended-halving-start-count")
        file_counts_per_day = generateFilesPerDayForHalvingPattern(start_files_per_day_value, extend=True)

    print(f"File counts per day: {file_counts_per_day}")

    sys.exit(0)

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

    # UsageException("asdasd")

    print("Del files:", deletefiles)

    found_files = glob(filepattern, recursive=True)

    found_files.sort(key=os.path.getmtime, reverse=True)

    dayAgeToFilepath = defaultdict(list)

    for fname in found_files:
        # floating point time since epoch

        file_mod_time = os.path.getmtime(fname)
        file_mod_local_time = time.localtime(file_mod_time)
        file_formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', file_mod_local_time)

        file_date = date.fromtimestamp(file_mod_time)

        delta_days = now_date - file_date

        ft = Filetime(fname, file_mod_time, file_mod_local_time, file_formatted_time, delta_days)

        # print(f"Found file: {ft}")

        dayAgeToFilepath[delta_days].append(ft)

    pp = pprint.PrettyPrinter(indent=4)
    strr = pp.pformat(dayAgeToFilepath)
    
    # click.secho(f"Found map: {strr}", fg='yellow')

        # with open(fname, "r") as f:

if __name__ == '__main__':
    # hack to call ourselves with some test arguments when run directly from sublime text without args
    if len(sys.argv) == 1:
        # os.system("python thinfiles.py 'testFiles/**/*.txt'")
        # os.system("python thinfiles.py --max-file-counts '8,4,2,1' '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        # os.system("python thinfiles.py --max-file-counts '8,4,2,1' --halving-start-count 4 '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        # os.system("python thinfiles.py --halving-start-count 4 --extended-halving-start-count 4 '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        # os.system("python thinfiles.py --halving-start-count 10 '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        os.system("python thinfiles.py --extended-halving-start-count 1 '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        # os.system("python thinfiles.py --max-file-counts '-1' '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        # os.system("python thinfiles.py --max-file-counts '1x,y' '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        # os.system("python thinfiles.py --max-file-counts '' '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
        # os.system("python thinfiles.py '/Users/alexhunsley/Dropbox/Apps/Quine/main/main.html_backup/*.html'")
    else:
        hello()
    # invoke(hello, args=['--filepattern', 'grimp'])
