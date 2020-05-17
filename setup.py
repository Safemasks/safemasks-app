"""Setup file for safemasks web app
"""
__version__ = "0.1.0"
__author__ = "@ckoerber, @smkhassan"

from setuptools import setup

with open("requirements.txt", "r") as INP:
    REQUIREMENTS = INP.read()

with open("README.md", "r") as INP:
    LONE_DESCRIPTION = INP.read()

setup(
    name="safemasks",
    version=__version__,
    author=__author__,
    author_email="",
    description="Django web app and API interface for Safemasks project.",
    long_description=LONE_DESCRIPTION,
    url="https://github.com/Safemasks/safemasks-app",
    project_urls={
        "Bug Reports": "https://github.com/Safemasks/safemasks-app/issues",
        "Source": "https://github.com/Safemasks/safemasks-app",
    },
    packages=["safemasks"],
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords=[],
    entry_points={"console_scripts": ["safemasks=safemasks.manage:main"],},
)
