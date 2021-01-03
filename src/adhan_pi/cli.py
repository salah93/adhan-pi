import datetime as dt

from argparse import ArgumentParser

from adhan_pi.utils import get_location_from_city, PrayertimesAPI


def schedule_cron():

    parser = ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--state", required=True, help="abbreviation of state")
    args = parser.parse_args()

    prayer_schedule = PrayertimesAPI().get_prayer_times(
        get_location_from_city(args.city, args.state), dt.date.today()
    )
    prayer_times = [
        ("fajr", prayer_schedule.fajr),
        ("dhuhr", prayer_schedule.dhuhr),
        ("asr", prayer_schedule.asr),
        ("maghrib", prayer_schedule.maghrib),
        ("isha", prayer_schedule.isha),
    ]

    import crontab

    with crontab.CronTab(user="salah") as cron:
        for old_job in cron.find_comment("adhan_pi"):
            cron.remove(old_job)

        for prayer, time in prayer_times:
            job = cron.new(
                command="/opt/adhan-pi/env/bin/alert_adhan --prayer {}".format(
                    prayer
                ),
                comment="adhan_pi",
            )
            job.day.every(1)
            job.hour.on(time.hour)
            job.minute.on(time.minute)


def alert_adhan():
    parser = ArgumentParser()
    parser.add_argument("--prayer", required=True)
    args = parser.parse_args()

    with open("/tmp/prayers.txt", "a") as f:
        f.write("{}\n".format(args.prayer))
