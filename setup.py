"""
Setuptools based setup module
"""
from setuptools import setup, find_packages
import versioneer


setup(
    name='pycronserver',
    version=versioneer.get_version(),
    description='Cron server for python functions',
    url='https://github.com/pyscioffice/pycronserver',
    author='Jan Janssen',
    author_email='jan.janssen@outlook.com',
    license='BSD',
    packages=find_packages(exclude=["*tests*"]),
    install_requires=[
        'sqlalchemy==2.0.19',
        'python-crontab==3.0.0',
    ],
    cmdclass=versioneer.get_cmdclass(),
    entry_points={
        "console_scripts": [
            'pycronserver=pycronserver.__main__:command_line_parser'
        ]
    }
)
