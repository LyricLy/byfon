import setuptools


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name = "byfon",
    packages = setuptools.find_packages(),
    version = "0.1.0",
    description = "A library for the easier writing of BF code.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = "LyricLy",
    author_email = "christinahansondesu@gmail.com",
    url = "https://github.com/LyricLy/byfon",
    keywords = ["bf", "esolang", "transpile"],
    install_requires = [x for x in requirements if "git+" not in x],
    dependency_links = [x.split("git+")[1] for x in requirements if "git+" in x],
    license = "MIT",
    entry_points = {
        "console_scripts": [
            "byfon = byfon:main"
        ]
    },
    classifiers = [
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities"
    ]
)
