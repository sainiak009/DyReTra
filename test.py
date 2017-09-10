from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import JobExecutionEvent
from datetime import datetime, timedelta
from random import randint
import time

scheduler = BackgroundScheduler()

def hi():
    print("HOLA")

def my_listener(event):
    print(dir(event))
    print(event.__class__)
    print(isinstance(event, JobExecutionEvent))
    # if event.exception:
    #     print('The job crashed :(')
    # else:
    #     print('The job worked :)')

    print("\n\n\n")

if __name__ == "__main__":
    run_time = (datetime.now() + timedelta(seconds=randint(1,3) + 1))
    run_time = run_time.strftime("%Y-%m-%d %H:%M:%S")
    scheduler.add_listener(my_listener)
    scheduler.add_job(hi, 'date', run_date=run_time)

    scheduler.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
