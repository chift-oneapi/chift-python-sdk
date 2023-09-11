from os.path import abspath, dirname, join

from setuptools import find_packages, setup

NAME = "chift"

DIR_PATH = dirname(abspath(__file__))

version_contents = {}
with open(join(DIR_PATH, "chift", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

with open(DIR_PATH + "/README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    description="Chift API client",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=version_contents["VERSION"],
    packages=find_packages(),
    install_requires=[
        "pydantic >= 1.10, <2",
        "requests >= 2.20",
    ],
    python_requires=">=3.9",
    extras_require={
        "dev": [
            "pytest-cov",
            "black",
            "isort",
            "autoflake",
            "coverage==6.5.0",
            "build",
            "twine",
        ]
    },
    include_package_data=True,
)
