"""Builds the cvgui python package"""
import os
from setuptools import setup, find_packages

NAME = "cvgui"
DESCRIPTION = "A library for creating body-interactive guis using computer vision."
URL = "https://github.com/mitchellss/cvgui"
EMAIL = "stephen.mitchell2299@gmail.com"
AUTHOR = "Stephen Mitchell"
REQUIRES_PYTHON = ">=3.9"
VERSION = "0.3.1"

REQUIRED = [
    "mediapipe>=0.8.7.2",
    "numpy>=1.21.2",
    "opencv_python>=4.3.0.38",
    "typing_extensions>=4.3.0",
    "pygame>=2.0.0"
]

here = os.path.abspath(os.path.dirname(__file__))
about = {}
about["__version__"] = VERSION

setup(name=NAME,
      version=about["__version__"],
      license="MIT",
      description=DESCRIPTION,
      long_description=DESCRIPTION,
      author=AUTHOR,
      author_email=EMAIL,
      python_requires=REQUIRES_PYTHON,
      url=URL,
      packages=find_packages(
          exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
      install_requires=REQUIRED, include_package_data=True)
