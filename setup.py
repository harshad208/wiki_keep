from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

# Get the directory of setup.py
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to req.txt
requirements_file = os.path.join(base_dir, "req.txt")

with open(requirements_file, "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="wiki_keep",
    version="0.1.0",
    author="harshad yadav",
    author_email="harshadyadav20@gmail.com",
    description="A Python module for managing and saving Wikipedia articles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    package_data={'wiki_keep': ['data/config.ini']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
