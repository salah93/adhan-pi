import datetime as dt

import adhan_pi

from argparse import ArgumentParser
from abc import abstractmethod, ABC

from .config import ADHAN_MP3_PATH, FAJR_ADHAN_MP3_PATH
from .utils import get_location_from_query

try:
    import crontab
    from pydub import AudioSegment
    from pydub.playback import play

    CRON_SCRIPTS_IMPORTED = True
except ImportError:
    CRON_SCRIPTS_IMPORTED = False


def schedule_prayer_cron():
    if not CRON_SCRIPTS_IMPORTED:
        raise ImportError

    parser = ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    prayer_times = adhan_pi.p.get_prayer_times(
        get_location_from_query(args.query), dt.date.today()
    )

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
        if not CRON_SCRIPTS_IMPORTED:
            raise ImportError

        if self.prayer == "fajr":
            adhan = AudioSegment.from_mp3(FAJR_ADHAN_MP3_PATH)
        else:
            adhan = AudioSegment.from_mp3(ADHAN_MP3_PATH)
        play(adhan)


def alert_factory(prayer: str):
    return AdhanAlertFFMPEG(prayer)


def alert_adhan():
    parser = ArgumentParser()
    parser.add_argument("--prayer", required=True)
    args = parser.parse_args()
    alert_cls = alert_factory(args.prayer)
    alert_cls.alert()
