import datetime as dt
import os
import pickle
import pwd
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import List, Optional

from .config import ADHAN_MP3_PATH, FAJR_ADHAN_MP3_PATH
from .dataclasses import Coordinates, PrayerTimes
from .utils import get_location_from_query, get_prayer_times_for_month

try:
    from crontab import CronTab
    from pydub import AudioSegment
    from pydub.playback import play

    CRON_SCRIPTS_IMPORTED = True
except ImportError:
    CRON_SCRIPTS_IMPORTED = False


def folder_type(v: str) -> str:
    os.makedirs(v, exist_ok=True)
    return v


def schedule_prayer_cron_runner() -> None:
    parser = ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument(
        "--cache-dir",
        default=os.path.expanduser(
            f"~/.cache/prayertimes/{dt.date.today().year}/"
        ),
        type=folder_type,
        required=True,
    )
    args = parser.parse_args()
    schedule_prayer_cron(args.user, args.query, args.cache_dir)


def schedule_prayer_cron(user: str, query: str, cache_dir: str) -> None:
    if not CRON_SCRIPTS_IMPORTED:
        raise ImportError

    user_id = pwd.getpwnam(user).pw_uid

    today = dt.date.today()
    coords = get_location_from_query(query)
    prayer_times = get_prayer_times_for_day(coords, today, cache_dir)
    with CronTab(user=user) as cron:
        for old_job in cron.find_comment("adhan_pi"):
            cron.remove(old_job)

        for prayer in prayer_times:
            job = cron.new(
                command="XDG_RUNTIME_DIR=/run/user/{user_id} /opt/adhan-pi/env/bin/alert_adhan --prayer {prayer} > /dev/null 2>&1".format(
                    user_id=user_id, prayer=prayer.name
                ),
                comment="adhan_pi",
            )
            job.day.every(1)
            job.hour.on(prayer.time.hour)
            job.minute.on(prayer.time.minute)


def get_prayer_times_for_day(
    coords: Coordinates, date: dt.date, cache_dir: str
) -> PrayerTimes:

    cache_file = os.path.join(
        cache_dir, f"{date.strftime('%B').lower()}.pickle"
    )

    prayer_times_all = _load_from_cached_file(cache_file)
    if prayer_times_all is None:
        prayer_times_all = get_prayer_times_for_month(
            coords, date.year, date.month
        )
        _cache_to_file(prayer_times_all, cache_file)
    return prayer_times_all[date.day - 1]


def _load_from_cached_file(cache_file: str) -> Optional[List[PrayerTimes]]:
    try:
        with open(cache_file, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, IndexError, AttributeError, KeyError):
        return None


def _cache_to_file(
    prayer_times_all: List[PrayerTimes], cache_file: str
) -> None:
    with open(cache_file, "wb") as f:
        pickle.dump(prayer_times_all, f)


class AdhanAlert(ABC):
    def __init__(self, prayer: str):
        self.prayer = prayer

    @abstractmethod
    def alert(self) -> None:
        pass


class AdhanAlertFFMPEG(AdhanAlert):
    """
    play adhan sound
    """

    def alert(self) -> None:
        if not CRON_SCRIPTS_IMPORTED:
            raise ImportError

        if self.prayer == "fajr":
            adhan = AudioSegment.from_mp3(FAJR_ADHAN_MP3_PATH)
        else:
            adhan = AudioSegment.from_mp3(ADHAN_MP3_PATH)
        play(adhan)


def alert_factory(prayer: str) -> AdhanAlert:
    return AdhanAlertFFMPEG(prayer)


def alert_adhan() -> None:
    parser = ArgumentParser()
    parser.add_argument("--prayer", required=True)
    args = parser.parse_args()
    alert_cls = alert_factory(args.prayer)
    alert_cls.alert()
