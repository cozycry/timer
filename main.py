import os
import threading as th

types = {'s':1,'m': 60,'h':3600}

def get_seconds(t):
    unit = t[-1]
    time_value = int(t[:-1])
    return time_value * types[unit]

def format_time(t):
    if t >= types['h']:
        return "%d hour(s)" % (t // types['h'])
    elif t >= types['m']:
        return "%d minute(s)" % (t // types['m'])
    else:
        return "%d second(s)" % t

def send_notify(t, message, expire_time=30000):
    os.system("notify-send --expire-time=%d 'Timer' '%s'" % (expire_time, message))

def create_and_start_timer(t):
    print("Okay! reminding you in %s" % format_time(t))
    try:
        if t >= 60:
            half_time = t / 2
            timer_halfway = th.Timer(half_time, send_notify, [t, 'Your %s timer has %s left' % (format_time(t), format_time(t - half_time)), 1000])
            timer_halfway.start()
            timer_halfway.join()
            print("Your %s timer has %s left!" % (format_time(t), format_time(t - half_time)))

        timer_end = th.Timer(t, send_notify, [t, 'Your %s timer is up!' % format_time(t)])
        timer_end.start()
        timer_end.join()

        print("Your %s timer has finished!" % format_time(t))
    except KeyboardInterrupt:
        print("\nTimer stopped.")

length = input("Timer length? ")
t = None

for unit in types:
    if unit in length:
        t = get_seconds(length)
        create_and_start_timer(t)
        break

if t is None:
    t = int(length)
    create_and_start_timer(t)
