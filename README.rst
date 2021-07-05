Alien Tracker
=============

Overview
--------

This is a simple command-line app that finds text patterns ("invaders", ASCII art) in another text ("screen", ASCII art).

All "screen" and "invaders" are text files whose paths are provided to the app as command-line options.

You also need to specify a threshold for similarity, e.g., "0.9", "0.8", "0.75", etc, due to the screen having noise (
matches are not necessarily perfect).

Here's a screenshot of the app in action:

.. image:: ./images/app_in_action.gif
  :alt: App in action

The purpose behind this project is to exercise the application of S.O.L.I.D. principles, but I also used this project
as an excuse to try `poetry <https://python-poetry.org>`_ for package management and
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ for documenting
this project (this very document).

Design
------

The app's class diagram follows below:

.. image:: ./images/app.png
  :alt: App's Class Diagram

The interface (abstract class in Python) ``Representation`` is used for both "screen" and "invader".

I don't see the point of creating different entities for "screen" and "invader" at this moment. There are no other
differences (other than shape) between these entities that would justify specific entities for each.

We may implement different representations for different resources, e.g., text, text file, image, etc.

For this app, both "screen" and "invader" are stored in text files, thus, we've created ``TextFileRepresentation``
and ``TextRepresentation`` (this one useful for unit tests).

Note that we are making use of the dependency inversion principle here: our app deals with representations, it doesn't
care if it's a representation for text, text file, image, etc.

    **NOTE:**

    If you look at the code, you will notice that `TextFileRepresentation` inherits from `TextRepresentation`.
    As a rule of thumb, I'll prefer composition, but one level of inheritance should not result in any major caveats.

The heart of the app is the class ``Tracker``, which actually detects "invaders" on the "screen".

We are using composition by making ``Tracker`` use components such as ``Representation``, ``Shingle``, and ``Detector``.

The class ``Shingle`` represents a piece of the "screen", a sliding window view the size of the "invader" we want to detect.
A shingle could have empty spaces (as we are sliding fixed size windows around the border outside the "screen").
The class holds the sliding window contents as well as information about its positioning on the "screen".

The interface ``Detector``  is responsible for checking if a shingle from the screen contains an invader. At the moment, we have a naive
detector: ``SimpleDetector``, which simply computes the percentage of matching between a shingle and an invader.
We may create different detectors, such as a `MinHash <https://en.wikipedia.org/wiki/MinHash>`_ detector, so our solution
could scale for larger screens.

Another important component of the app is the ``Renderer``, which is responsible for rendering the
detections. At the moment we only can render the detection results to the standard output using ``StandardOutputRenderer``.

We may also create different renderers, e.g., we could create a renderer that would render the detections to an image file.

Once again, our app is indifferent to the detectors or renderers we use, thanks to the use of the dependency inversion principle:
High-level code doesn't depend on low-level code, but the other way around.

In particular, the class ``Tracker`` use of ``Detector`` follows the "strategy pattern" (from `GoF <https://en.wikipedia.org/wiki/Design_Patterns>`_).

The same design pattern is also used by the class `App`, which uses ``Renderer``.

The use of the "strategy pattern" follows the open-close principle: If we decide to implement new detectors, representations, or renderers,
we can do that by adding new code with minor modifications to existent code.

Another uses of S.O.L.I.D. in this code:

- Single responsibility principle:  All my classes and methods are small. They do a single thing and well. All my methods are around six lines or smaller.

- Liskov substitution: I have two implementations of ``Representation``: ``TextRepresentation`` and ``TextFileRepresentation``. Note that the latter inherits from the first, but they are completely interchangeable. ``Tracker`` and ``App`` can work with both representations the same way without distinction.

- Interface segregation: My interfaces are pretty small, so I didn't have to break them into smaller interfaces, but my interfaces are indeed quite small.

TODO
----

- At the moment, ``Tracker`` does the shingling (extract ``Shingle`` objects from "screen"). I think that would make sense to define an interface ``Shingler`` and delegate this responsibility to another class. We possibly could have different "shinglers" that implement different algorithms (e.g., sliding the view window at different step lengths, etc).

- I've decided to treat `numpy <https://numpy.org/>`_ types as they were primitive types from Python. I could have used only primitives (and converted inside ``Tracker``), but I believe that convenience justifies this decision. At this point I, personally (don't hate on me, it's just my opinion!), see numpy as an extension of the Python language rather than simply a framework.

- The heart of the app is ``Tracker``, for which we could have defined an interface for and have different trackers for different purposes, e.g., a tracker for videos, but I believe that at this time, given the requirements, would be overkill.

Project Dependencies
--------------------

Interpreter
~~~~~~~~~~~

We are using Python 3.8.3. We recommend to create your own virtual environment for this project as following:

.. code-block:: bash

     $ cd <your project root>
     $ python3.8 -m venv .venv
     $ source .venv/bin/activate

Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

We are using `poetry <https://python-poetry.org>`_. You may install poetry by executing the following command:

.. code-block:: bash

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

Once poetry is installed, you may install all the project's dependencies as following:

.. code-block:: bash

    poetry install

This should install all the dependencies listed in ``pyproject.toml``. Specific versions are listed in ``poetry.lock``.

Installing the App
------------------

.. code-block:: bash

    $ cd <your project root>
    $ python setup.py install

Now you should be able to call the app from anywhere:

.. code-block:: bash

    $ alien-tracker --help


Running the App
---------------

You may follow the instructions from the previous section to install the app or run it in development mode:

.. code-block:: bash

    $ python -m alien_tracker.cli --help
    Usage: python -m alien_tracker [OPTIONS]

    Options:
      -s, --screen TEXT      Path to a text file with the screen  [required]
      -t, --threshold FLOAT  Detection threshold in the interval (0.0, 1.0)
                             [required]
      -i, --invaders TEXT    Path to a text file with an invader. Multiple
                             invaders might be provided  [required]
      --help                 Show this message and exit.


If you are developing, this will spare you from the re-installing the app to run it in command-line after every change.

Examples of calling the app:

.. code-block:: bash

    $ python -m alien_tracker.cli -s ./tests/resources/screens/sample-screen.txt -t 0.75 -i ./tests/resources/invaders/squid.txt
    $ python -m alien_tracker.cli -s ./tests/resources/screens/sample-screen.txt -t 0.75 -i ./tests/resources/invaders/crab.txt
    $ python -m alien_tracker.cli -s ./tests/resources/screens/sample-screen.txt -t 0.75 -i ./tests/resources/invaders/squid.txt -i ./tests/resources/invaders/crab.txt
    $ python -m alien_tracker.cli -s ./tests/resources/screens/sample-screen.txt -t 0.8 -i ./tests/resources/invaders/squid.txt -i ./tests/resources/invaders/crab.txt

Running Tests
-------------

.. code-block:: bash

    $ pytest -s -vvv

You should get an output similar to this:

.. code-block:: text

    collected 16 items

    tests/test_cli.py::TestCLI::test_track_multiple_invaders PASSED
    tests/test_cli.py::TestCLI::test_track_multiple_invaders_higher_threshold PASSED
    tests/test_cli.py::TestCLI::test_track_single_invader PASSED
    tests/test_detectors.py::TestDetectors::test_simple_detector_detected PASSED
    tests/test_detectors.py::TestDetectors::test_simple_detector_detected_with_noise PASSED
    tests/test_detectors.py::TestDetectors::test_simple_detector_undetected PASSED
    tests/test_renderers.py::TestRenderers::test_standard_output_renderer PASSED
    tests/test_representations.py::TestRepresentations::test_text_file_invader_representation PASSED
    tests/test_shingle.py::TestShingle::test_create_first_inside_screen_shingle PASSED
    tests/test_shingle.py::TestShingle::test_create_first_outside_screen_shingle PASSED
    tests/test_shingle.py::TestShingle::test_create_next_inside_screen_shingle_down PASSED
    tests/test_shingle.py::TestShingle::test_create_next_inside_screen_shingle_to_the_left PASSED
    tests/test_shingle.py::TestShingle::test_create_next_outside_screen_shingle_down PASSED
    tests/test_shingle.py::TestShingle::test_create_next_outside_screen_shingle_to_the_left PASSED
    tests/test_tracker.py::TestTracker::test_get_detections PASSED
    tests/test_tracker.py::TestTracker::test_invader_larger_than_screen PASSED

    ========================================== 16 passed in 0.31s ==========================================

Coverage Reports
----------------

.. code-block:: bash

    $ coverage run --source=alien_tracker -m pytest
    $ coverage report

You should get an output similar to this:

.. code-block:: bash

    Name                               Stmts   Miss  Cover
    ------------------------------------------------------
    alien_tracker/__init__.py              1      0   100%
    alien_tracker/app.py                  16      0   100%
    alien_tracker/cli.py                   9      0   100%
    alien_tracker/detectors.py            14      0   100%
    alien_tracker/renderers.py            32      0   100%
    alien_tracker/representations.py      22      0   100%
    alien_tracker/shingle.py              20      0   100%
    alien_tracker/tracker.py              36      0   100%
    ------------------------------------------------------
    TOTAL                                150      0   100%


For a more detailed view of the coverage run the following command for HTML reports:

.. code-block:: bash

    $ coverage html

Reports will be made available in the folder ``./htmlcov``.

Developer's Hints
-----------------

Formatting
~~~~~~~~~~

You may format your code in the command-line using `black <https://github.com/psf/black>`_:

.. code-block:: bash

    black .

O.S. Dependencies
~~~~~~~~~~~~~~~~~

You may need to install ``libffi-dev``:

.. code-block:: bash

    sudo apt-get install libffi-dev
