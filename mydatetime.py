import datetime,pytz,re
import pandas as pd

def get_strtype(string):
    """

    Detect the type of time str format used in kabusapi or whatever.
     - 2000-00-00
     - 2000-00-00T00:00:00
     - 2000-00-00T00:00:00+00:00
    """
    pattern1=re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if pattern1.fullmatch(string): return 1
    pattern2=re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')
    if pattern2.fullmatch(string): return 2
    pattern3=re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
    if pattern3.fullmatch(string): return 3
    raise Exception



def get_today(type=None,country=None):
    if type=='datetime' or type is None:
        if not country:
            return datetime.date.today()
        elif country.lower() == 'japan':
            return datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).date()

    elif type=='str':
        return str(get_today('datetime',country))
    elif type=='pd':
        return pd.Timestamp(get_today('str',country)) # It does not contain tz info but date might be different, so country is necessary arg. 
    raise TypeError

def str_todate(string):
    type_=get_strtype(string)
    if type_==1:
        a,b,c=[int(i) for i in string.split('-')]
        return datetime.date(a,b,c)
    elif type_==2 or type_==3:
        return str_todate(string.split('T')[0])
    raise KeyError

def str_todatetime(string): 
    type_=get_strtype(string)
    if type_==1:
        a,b,c=[int(i) for i in string.split('-')]
        return datetime.datetime(a,b,c,0,0,0,0)
    elif type_==2:
        abc,def_=string.split('T')
        a,b,c=[int(i) for i in abc.split('-')]
        d,e,f=[int(i) for i in def_.split(':')]
        return datetime.datetime(a,b,c,d,e,f,0)
    elif type_==3:
        naive=str_todatetime(string[:-6])
        aware=pytz.utc.localize(naive)
        if string[-6]=='+':
            return aware - datetime.timedelta(hours=int(string[-5:-3]))
        elif string[-6]=='-':
            return aware + datetime.timedelta(hours=int(string[-5:-3]))
    raise Exception


def str_plusNday(string,n):
    type_=get_strtype(string)
    if type_==1:
        dt = str_todate(string) + datetime.timedelta(days=n)
        return str(dt)
    elif type_==2:
        dt = str_todatetime(string) + datetime.timedelta(days=n)
        return str(dt)
    raise Exception

def str_topd(string):
    type_=get_strtype(string)
    if type_==1 or type_==2:
        return pd.Timestamp(str_todatetime(string))
    raise Exception

def to_japantz(string):
    type_=get_strtype(string)
    if type_==3:
        utc_time=str_todatetime(string)
        return utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    raise Exception

