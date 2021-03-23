import pandas as pd
import datetime

## calculate days
def calculate_days(x):
    return (x.days + x.seconds/3600./24.)

## calculate days
def calculate_hours(x):
    return (x.days + x.seconds/3600.)

## transform date
def to_datetime(t):
    if t[4:5] == '/':
        return datetime.datetime.strptime(t,'%Y/%m/%d %H:%M:%S')
    else:
        return datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')

# get nowt
def get_nowtime():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def Reverse_Dictionary(dic):
    return {value:key for key, value in dic.items()}
