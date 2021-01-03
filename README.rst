adhan-pi
=======================


Developing
---------

.. -code-begin-

.. code-block:: bash

   >>> sudo dnf install ffmpeg
   >>> python3 -m venv /opt/adhan-pi/env
   >>> source /opt/adhan-pi/env/bin/activate
   >>> pip install -e '.[dev]'
   >>> tox -e lint && tox
   >>> sudo ln -s ~/adhan-pi /opt/adhan-pi


Setting up Cron env
-------------------

   >>> source /opt/adhan-pi/env/bin/activate
   >>> pip install -e '.[cron]'


Setting up Cron
---------------

Add this to your cronjob (with your user) (crontab -e)

    0 23 * * * /opt/adhan-pi/env/bin/schedule_prayer_cron --query "New York, NY" --user salah

set up crons manually

   >>> source /opt/adhan-pi/env/bin/activate
   >>> /opt/adhan-pi/env/bin/schedule_prayer_cron --query "New York, NY" --user salah
