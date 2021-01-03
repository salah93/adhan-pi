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

Add this to your cronjob (with your user) (crontab -e)

    0 23 * * * /opt/adhan-pi/env/bin/schedule_prayer_cron --query "New York, NY" --user salah
