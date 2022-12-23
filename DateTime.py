import datetime

def daymonthyear(day):
    return "{:02d}".format(day.day) + "." + "{:02d}".format(day.month) + "." + "{:04d}".format(day.year)

def daymonth(day):
    return "{:02d}".format(day.day) + "." + "{:02d}".format(day.month)