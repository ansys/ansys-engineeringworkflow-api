"""Sphinx documentation configuration file."""

from datetime import datetime
import os
from pathlib import Path

from ansys_sphinx_theme import (
    ansys_favicon,
    get_autoapi_templates_dir_relative_path,
    get_version_match,
    pyansys_logo_black,
)

# from ansys.engineeringworkflow.api import __version__
__version__ = "0.0.1"

# Project information
project = "ansys-engineeringworkflow-api"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", "<DEFAULT_CNAME>")
switcher_version = get_version_match(__version__)

# use the default pyansys logo
html_logo = pyansys_logo_black
html_favicon = ansys_favicon
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "Ansys Engineering Workflow API"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/ansys-engineeringworkflow-api",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "icon_links": [
        {
            "name": "Support",
            "url": "https://github.com/ansys/ansys-engineeringworkflow-api/discussions",
            "icon": "fa fa-comment fa-fw",
        },
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": switcher_version,
    },
}

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "ansys",
    "github_repo": "ansys-engineeringworkflow-api",
    "github_version": "main",
    "doc_path": "doc/source",
}

# Sphinx extensions
extensions = [
    "notfound.extension",  # for the not found page.
    "numpydoc",
    "autoapi.extension",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    # kept here as an example
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
numpydoc_xref_param_type = True
autosectionlabel_prefix_document = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    # "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}


# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Configuration for Sphinx autoapi
autoapi_type = "python"
autoapi_dirs = ["../../src/ansys"]
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
]
autoapi_template_dir = get_autoapi_templates_dir_relative_path(Path(__file__))
suppress_warnings = ["autoapi.python_import_resolution"]
autoapi_python_use_implicit_namespaces = True
autoapi_render_in_single_page = ["class", "enum", "exception"]


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "links.rst",
]

linkcheck_ignore = [
    "https://github.com/ansys/ansys-engineeringworkflow-api/*",  # this site is private
    "https://engineeringworkflow.docs.pyansys.com/*",  # this site is private
]

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog = ""
# Read link all targets from file
with open("links.rst") as f:
    rst_epilog += f.read()

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"{project}-Documentation-{__version__}.tex",
        f"{project} Documentation",
        author,
        "manual",
    ),
]
