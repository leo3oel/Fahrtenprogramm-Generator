import datetime

def daymonthyear(day):
    if day:
        return "{:02d}".format(day.day) + "." + "{:02d}".format(day.month) + "." + "{:04d}".format(day.year)
    return ""

def daymonth(day):
    if day:
        return "{:02d}".format(day.day) + "." + "{:02d}".format(day.month)
    return ""