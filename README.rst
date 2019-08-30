=======
OpenCAL
=======

Copyright (c) 2008-2019 Jérémie DECOCK (www.jdhp.org)

* Web site: http://www.jdhp.org/software_en.html#opencal
* Online documentation: https://jdhp.gitlab.io/opencal
* Examples: https://jdhp.gitlab.io/opencal/gallery/

* Notebooks: https://gitlab.com/jdhp/opencal-lib-python-notebooks
* Source code: https://gitlab.com/jdhp/opencal-lib-python
* Issue tracker: https://gitlab.com/jdhp/opencal-lib-python/issues
* OpenCal on PyPI: https://pypi.org/project/opencal


Description
===========

OpenCAL core library for Python

Note:

    This project is still in beta stage, so the API is not finalized yet.


Scientific references
=====================

Stanislas Dehaene (in french):

- https://www.college-de-france.fr/site/stanislas-dehaene/course-2015-02-17-09h30.htm (cours au Collège de France): very interesting references, e.g.:

  - Kang, S. H. K., Lindsey, R. V., Mozer, M. C., & Pashler, H. (2014). *Retrieval practice over the long term: should spacing be expanding or equal‐interval?* Psychonomic Bulletin & Review, 21(6), 1544–1550

- https://www.franceculture.fr/emissions/la-conversation-scientifique/apprendre-est-ce-que-cela-peut-sapprendre
- https://www.franceculture.fr/sciences/trois-conseils-pour-ameliorer-votre-memoire-par-stanislas-dehaene, https://www.youtube.com/watch?v=MMvzA5SfBGk and https://www.youtube.com/watch?v=-Fnwc_ORZFM (very short article and videos)


Dependencies
============

*  Python >= 3.0

.. _install:

Installation
============

Gnu/Linux
---------

You can install, upgrade, uninstall OpenCAL with these commands (in a
terminal)::

    pip install --pre opencal
    pip install --upgrade opencal
    pip uninstall opencal

Or, if you have downloaded the OpenCAL source code::

    python3 setup.py install

.. There's also a package for Debian/Ubuntu::
.. 
..     sudo apt-get install opencal

Windows
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.4 under Windows 7.
..     It should also work with recent Windows systems.

You can install, upgrade, uninstall OpenCAL with these commands (in a
`command prompt`_)::

    py -m pip install --pre opencal
    py -m pip install --upgrade opencal
    py -m pip uninstall opencal

Or, if you have downloaded the OpenCAL source code::

    py setup.py install

MacOSX
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.5 under MacOSX 10.9 (*Mavericks*).
..     It should also work with recent MacOSX systems.

You can install, upgrade, uninstall OpenCAL with these commands (in a
terminal)::

    pip install --pre opencal
    pip install --upgrade opencal
    pip uninstall opencal

Or, if you have downloaded the OpenCAL source code::

    python3 setup.py install


Documentation
=============

* Online documentation: https://jdhp.gitlab.io/opencal
* API documentation: https://jdhp.gitlab.io/opencal/api.html


Example usage
=============

TODO


Bug reports
===========

To search for bugs or report them, please use the OpenCAL Bug Tracker at:

    https://gitlab.com/jdhp/opencal-lib-python/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe
