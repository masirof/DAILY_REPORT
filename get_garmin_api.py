import garminconnect
from dotenv import load_dotenv
import os
from icecream import ic
from datetime import datetime, date, timedelta, timezone
import json

# .envファイルで環境変数を上書き
load_dotenv()

GARMIN_EMAIL = os.environ.get("GARMIN_EMAIL")
GARMIN_PASS = os.environ.get("GARMIN_PASS")

garmin = garminconnect.Garmin(GARMIN_EMAIL, GARMIN_PASS)
garmin.login()
ic(garmin.display_name)

yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.isoformat()
yesterday



sleep = garmin.get_sleep_data('2025-02-20')
# ic(sleep['dailySleepDTO'])
sleep_start_gmt = sleep['dailySleepDTO']['sleepStartTimestampGMT']
ic(sleep['dailySleepDTO']['sleepStartTimestampGMT'])
# json_reader = json.load(sleep)
# print(json_reader)
# print(sleep)

# GMT(ほぼUTC)からJSTに変換
def GMT_to_JST(GMT_time):
    GMT_time_s = GMT_time/1000
    utc_time = datetime.fromtimestamp(GMT_time_s, tz=timezone.utc)

    jst = timezone(timedelta(hours=9))
    jst_time = utc_time.astimezone(jst)
    jst_time = jst_time.replace(tzinfo=None)
    return jst_time

print("JST:", GMT_to_JST(sleep_start_gmt))
ic(yesterday)


# sleepMovement