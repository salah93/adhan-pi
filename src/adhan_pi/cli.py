import datetime as dt

import adhan_pi

from argparse import ArgumentParser
from abc import abstractmethod, ABC

from adhan_pi.utils import get_location_from_query


def schedule_prayer_cron():

    parser = ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    prayer_times = adhan_pi.p.get_prayer_times(
        get_location_from_query(args.query), dt.date.today()
    )

    import crontab

    with crontab.CronTab(user=args.user) as cron:
        for old_job in cron.find_comment("adhan_pi"):
            cron.remove(old_job)

        for prayer in prayer_times:
            job = cron.new(
                command="/opt/adhan-pi/env/bin/alert_adhan --prayer {} > /dev/null 2>&1".format(
                    prayer.name
                ),
                comment="adhan_pi",
            )
            job.day.every(1)
            job.hour.on(prayer.time.hour)
            job.minute.on(prayer.time.minute)


class AdhanAlert(ABC):
    def __init__(self, prayer: str):
        self.prayer = prayer

    @abstractmethod
    def alert(self):
        pass


class AdhanAlertFFMPEG(AdhanAlert):
    """
    play adhan sound
    """

    def alert(self):
        from pydub import AudioSegment
        from pydub.playback import play

        if self.prayer == "fajr":
            adhan = AudioSegment.from_mp3("/opt/adhan-pi/static/azan-fajr.mp3")
        else:
            adhan = AudioSegment.from_mp3("/opt/adhan-pi/static/azan2.mp3")
        play(adhan)


def alert_factory(prayer: str):
    return AdhanAlertFFMPEG(prayer)


def alert_adhan():
    parser = ArgumentParser()
    parser.add_argument("--prayer", required=True)
    args = parser.parse_args()
    alert_cls = alert_factory(args.prayer)
    alert_cls.alert()
