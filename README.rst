adhan-pi
=======================


Developing
---------

.. -code-begin-

.. code-block:: bash

   >>> sudo dnf install ffmpeg
   >>> pip install -e '.[dev]'
   >>> tox -e lint && tox
