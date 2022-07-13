from setuptools import setup


setup(
    name ='harrihelper',
    version='0.0.1',
    py_modules=[main_again.py],
    install_requires=[
        'click',
        'selenium',
        'pandas'
        ],
    entry_points='''
        [console_scripts]
        harrihelper=harrihelper:cli
        ''',
        )

