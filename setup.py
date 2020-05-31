from setuptools import setup

setup(
    name='thinfiles',
    version='0.0.1',
    py_modules=['thinfiles'],
    install_requires=[
        'Click',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        thinfiles=thinfiles:hello
    ''',
)
