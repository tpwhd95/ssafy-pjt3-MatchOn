import threading
import check_play_time
import datetime
import sys

print('==================== START', datetime.datetime.now(), '=====================')
print()


def execute_per_minute(second, num):
    print(f'시간: {datetime.datetime.now()} {num} 번째 실행')
    num += 1
    now_date = datetime.datetime.today().strftime("%Y-%m-%d")
    now_time = str(datetime.datetime.today().hour)+":10:00.000000"
    print(now_time)
    check_play_time.time_check(now_date, now_time)
    
    print()
    threading.Timer(second, execute_per_minute, [second, num]).start()

def on_time(sec, num):
    second = datetime.datetime.now().strftime("%S")
    minute = datetime.datetime.now().strftime("%M")
    print(f'시간: {datetime.datetime.now()} {num} 번째 정각맞추기')
    num += 1
    if int(second) == 0 and int(minute) == 0:
        return
    threading.Timer(sec, on_time, [sec, num]).start()
on_time(1, 1)
