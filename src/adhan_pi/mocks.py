from unittest.mock import Mock

import automock
from geopy.location import Location


def geocode_mock(failed_lookup: bool = False) -> Location:
    m = Mock()
    if failed_lookup:
        m.return_value.geocode.return_value = None
    else:
        m.return_value.geocode.return_value = Location(
            "nyc", (0, 0), {"address": "nyc", "longitude": 0, "latitude": 0}
        )
    return m


def cron_mock(previous_jobs: bool = False) -> Mock:
    m = Mock()
    if not previous_jobs:
        m.CronTab().__enter__().find_comment.return_value = []
    else:
        m.CronTab().__enter__().find_comment.return_value = [0, 1, 2, 3, 4]
    import crontab

    def new_job(command, comment):
        job = crontab.CronItem(
            command=command,
            comment=comment,
            user=None,
            cron=None,
            pre_comment=False,
        )
        m.crons.append(job)
        return job

    m.CronTab().__enter__().new.side_effect = new_job
    return m


automock.register("adhan_pi.utils.Nominatim", geocode_mock)
automock.register("adhan_pi.cli.crontab", cron_mock)
automock.register("adhan_pi.cli.AudioSegment")
automock.register("adhan_pi.cli.play")
