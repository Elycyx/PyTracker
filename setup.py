#!/usr/bin/env python3
"""
PyTracker - A Python wrapper for OpenVR tracking systems
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pytracker",
    version="1.0.0",
    author="PyTracker Development Team",
    author_email="pytracker@example.com",
    description="A comprehensive Python wrapper for OpenVR tracking systems",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Elycyx/PyTracker",
    project_urls={
        "Bug Reports": "https://github.com/Elycyx/PyTracker/issues",
        "Source": "https://github.com/Elycyx/PyTracker",
        "Documentation": "https://pytracker.readthedocs.io/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openvr>=1.0.0",
        "matplotlib>=3.3.0",
        "numpy>=1.19.0",
        "pytest>=6.0.0",
        "pytest-cov>=2.0.0",
        "black>=21.0.0",
        "flake8>=3.8.0",
        "mypy>=0.800.0",
        "sphinx>=4.0.0",
        "sphinx-rtd-theme>=0.5.0",
        "myst-parser>=0.15.0",
    ],
    entry_points={
        "console_scripts": [
            "pytracker-visualize=pytracker.examples.visualizer:main",
            "pytracker-test=pytracker.examples.test_tracker:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pytracker": [
            "config/*.json",
            "examples/*.py",
        ],
    },
    zip_safe=False,
    keywords="openvr, vr, tracking, steamvr, virtual-reality, pose-tracking",
)
