.. image:: https://travis-ci.org/wind-python/windpowerlib.svg?branch=dev
    :target: https://travis-ci.org/wind-python/windpowerlib
.. image:: https://coveralls.io/repos/github/wind-python/windpowerlib/badge.svg?branch=dev
    :target: https://coveralls.io/github/wind-python/windpowerlib?branch=dev

Introduction
=============

The windpowerlib is a library that provides a set of functions and classes to calculate the power output of wind turbines. It was originally part of the 
`feedinlib <https://github.com/oemof/feedinlib>`_ (windpower and pv) but was taken out to build up a community concentrating on wind power models.

For a quick start see the `Examples and basic usage <http://windpowerlib.readthedocs.io/en/stable/getting_started.html#examplereference-label>`_ section.


Documentation
==============

Full documentation can be found at `readthedocs <https://windpowerlib.readthedocs.io/en/stable/>`_.

Use the `project site <http://readthedocs.org/projects/windpowerlib>`_ of readthedocs to choose the version of the documentation. 
Go to the `download page <http://readthedocs.org/projects/windpowerlib/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.


Installation
============

If you have a working Python 3 environment, use pypi to install the latest windpowerlib version. We highly recommend to use virtual environments.

::

    pip install windpowerlib

The windpowerlib is designed for Python 3 and tested on Python >= 3.5.
Please see the `installation page <http://oemof.readthedocs.io/en/stable/installation_and_setup.html>`_ of the oemof documentation for complete instructions on how to install python and a virtual environment on your operating system.

Optional Packages
~~~~~~~~~~~~~~~~~

To see the plots of the windpowerlib example in the `Examples and basic usage <http://windpowerlib.readthedocs.io/en/stable/getting_started.html#examplereference-label>`_ section you should `install the matplotlib package <http://matplotlib.org/users/installing.html>`_.
Matplotlib can be installed using pip3 though some Linux users reported that it is easier and more stable to use the pre-built packages of your Linux distribution.


.. _examplereference-label:

Examples and basic usage
=========================

The basic usage of the windpowerlib is shown `here <http://windpowerlib.readthedocs.io/en/stable/basic_example_notebook.html>`_. The presented example is available as jupyter notebook and python script. You can download them along with example weather data:

 * `Basic example (Python script) <https://raw.githubusercontent.com/wind-python/windpowerlib/master/example/basic_example.py>`_
 * `Basic example (Jupyter notebook) <https://raw.githubusercontent.com/wind-python/windpowerlib/features/revise_example/example/basic_example.ipynb>`_
 * `Example data file <https://raw.githubusercontent.com/wind-python/windpowerlib/master/example/weather.csv>`_


To run the examples you first have to install the windpowerlib. To run the notebook you also need to install notebook using pip3. To launch jupyter notebook type ``jupyter notebook`` in terminal.
This will open a browser window. Navigate to the directory containing the notebook to open it. See the jupyter notebook quick start guide for more information on `how to install <http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/install.html>`_ and
`how to run <http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html>`_ jupyter notebooks.

The usage of further functions are shown in a second example. As the basic usage example it is available as jupyter notebook and as python script. The weather data in this example is the same as in the example above.

 * `Further example (Python script) <https://raw.githubusercontent.com/wind-python/windpowerlib/release_preparation/example/further_example.py>`_
 * `Further example (Jupyter notebook) <https://raw.githubusercontent.com/wind-python/windpowerlib/release_preparation/example/basic_example.ipynb>`_
 * `Example data file <https://raw.githubusercontent.com/wind-python/windpowerlib/master/example/weather.csv>`_


Contributing
==============

Clone/Fork: https://github.com/wind-python/windpowerlib

If you are interested in wind models and want to help improve the existing model do not hesitate to contact us.
As the windpowerlib started with contributors from the `oemof developer group <https://github.com/orgs/oemof/teams/oemof-developer-group>`_ we use the same 
`developer rules <http://oemof.readthedocs.io/en/stable/developing_oemof.html>`_.

Citing the windpowerlib
========================

We use the zenodo project to get a DOI for each version. `Search zenodo for the right citation of your windpowerlib version <https://zenodo.org/search?page=1&size=20&q=windpowerlib>`_.

License
============

Copyright (C) 2017 oemof developing group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.