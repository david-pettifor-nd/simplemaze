import pathlib
from setuptools import setup

# The directory containing the current file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="simplemaze",
    version="0.1.1",
    description="A Python library for generating mazes",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/david-pettifor-nd/simplemaze",
    author="David W Pettifor",
    author_email="noctemowl@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    packages=["simplemaze"],
    include_package_data=True,
    install_requires=["Pillow"],
)