import os

# python just treats ** expansion as a regular non-recursive glob, so
# it doesn't work the way we'd like. script must handle it.
os.system("python trimfiles.py 'testFiles/**/*.txt'")
# os.system("python trimfiles.py 'testFiles/a.txt'")

# os.system("python trimfiles.py \"testFiles/**/*.txt\"")
