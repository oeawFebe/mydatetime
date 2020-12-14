import datetime
import pandas as pd

def str_todate(string,sep="-"):
    a,b,c=string.split(sep)
    return datetime.date(int(a),int(b),int(c))

def str_todatetime(string,sep='-'): 
    a,b,c=string.split(sep)
    return datetime.datetime(int(a),int(b),int(c),0,0,0,0)

def str_plusNday(string,n):
    try:
        dt = str_todate(string) + datetime.timedelta(days=n)
    except:
        dt = str_todatetime(string) + datetime.timedelta(days=n)
    return str(dt)

def str_topd(string,sep="-"):
    return pd.Timestamp(str_todatetime(string,sep))
