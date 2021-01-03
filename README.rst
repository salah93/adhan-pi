adhan-pi
=======================


Developing
---------

.. -code-begin-

.. code-block:: bash

   >>> sudo dnf install ffmpeg
   >>> pip install -e '.[dev]'
   >>> tox -e lint && tox
   >>> sudo ln -s ~/adhan-pi /opt/adhan-pi

Add this to your cronjob (with your user)

    0 1 * * * /opt/adhan-pi/env/bin/schedule_prayer_cron --query "New York, NY" --user salah
