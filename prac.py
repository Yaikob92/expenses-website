import datetime

todays = datetime.date.today()
six_month_ago = todays - datetime.timedelta(days=30*6)
print(six_month_ago)
print(todays)
