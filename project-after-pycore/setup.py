"""Setup configuration for assistant-bot package."""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="assistant-bot-froii",
    version="1.0.1",
    author="Oleksa",
    author_email="lestyshchenko@gmail.com",
    description="Personal assistant bot for managing contacts with birthdays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/froii/goit_first_repo-9.2025/tree/main/project-after-pycore",
    py_modules=["main", "constants"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "assistant-bot=main:main",
        ],
    },
)
