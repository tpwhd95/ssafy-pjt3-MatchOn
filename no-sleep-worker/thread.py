import threading
import ./check_play_time
import datetime
import sys

print('==================== START', datetime.datetime.now(), '=====================')
print()


def execute_per_minute(second, num):
    print(f'시간: {datetime.datetime.now()} {num} 번째')
    num += 1
    check_play_time.time_check()
    print('루프 종료')
    print('잠깐 쉬기 10초')
    threading.Timer(second, execute_per_minute, [second, num]).start()


execute_per_minute(10, 1)
