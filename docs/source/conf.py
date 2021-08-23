# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from importlib.metadata import metadata

# -- Project information

_metadata = metadata("python-idealista")

project = _metadata["Name"]
author = _metadata["Author-email"].split("<", 1)[0].strip()
copyright = f"2021, {author}"

# The full version, including alpha/beta/rc tags
version = _metadata["Version"]
release = ".".join(version.split(".")[:2])

# -- General configuration

extensions = [
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "furo"
html_static_path = ["_static"]
