import datetime

# date = datetime.date.today(),
start_time = (datetime.datetime.now() - datetime.timedelta(hours= 3)).strftime("%H:%M:%S"),
# end_time = datetime.datetime.now().time(),

# print(date)
print(start_time)
# print(end_time)


# strftime("%H:%M:%S")