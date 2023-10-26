"""OpenCAL

OpenCAL core library for Python

Note:

    This project is in beta stage.

Viewing documentation using IPython
-----------------------------------
To see which functions are available in `opencal`, type ``opencal.<TAB>`` (where
``<TAB>`` refers to the TAB key), or use ``opencal.*get_version*?<ENTER>`` (where
``<ENTER>`` refers to the ENTER key) to narrow down the list.  To view the
docstring for a function, use ``opencal.get_version?<ENTER>`` (to view the
docstring) and ``opencal.get_version??<ENTER>`` (to view the source code).
"""

import importlib.metadata

import opencal.config
import opencal.io.sqlitedb
import opencal.path

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
# X.Y
# X.Y.Z # For bugfix releases  
# 
# Admissible pre-release markers:
# X.YaN # Alpha release
# X.YbN # Beta release         
# X.YrcN # Release Candidate   
# X.Y # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = importlib.metadata.version("opencal")

def get_version():
    return __version__


cfg, config_path = opencal.config.get_config()


__all__ = []
