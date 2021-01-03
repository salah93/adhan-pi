import datetime as dt

from argparse import ArgumentParser

from adhan_pi.utils import get_location_from_query, PrayertimesAPI


def schedule_prayer_cron():

    parser = ArgumentParser()
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    prayer_times = PrayertimesAPI().get_prayer_times(
        get_location_from_query(args.query), dt.date.today()
    )

    import crontab

    with crontab.CronTab(user="salah") as cron:
        for old_job in cron.find_comment("adhan_pi"):
            cron.remove(old_job)

        for prayer in prayer_times:
            job = cron.new(
                command="/opt/adhan-pi/env/bin/alert_adhan --prayer {}".format(
                    prayer.name
                ),
                comment="adhan_pi",
            )
            job.day.every(1)
            job.hour.on(prayer.time.hour)
            job.minute.on(prayer.time.minute)


def alert_adhan():
    parser = ArgumentParser()
    parser.add_argument("--prayer", required=True)
    args = parser.parse_args()

    with open("/tmp/prayers.txt", "a") as f:
        f.write("{}\n".format(args.prayer))
