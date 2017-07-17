# coding:utf-8


from datetime import datetime, timedelta


def after_day(dt, days):
    return dt + timedelta(days)


def datetime_from_str(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.000Z')


def today_str():
    return datetime.now().strftime('%Y%m%d')


def now_time():
    return datetime.now()