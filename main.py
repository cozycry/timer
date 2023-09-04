# github.com/cozycry
# CLI timer that uses notify-send to send desktop notifications, accepts inputs in seconds, minutes, or hours (5s, 5m, 5h)
# if no time unit is provided assumes seconds
import os
import threading as th
import time
import sys

time_units = {'s':1,'m':60,'h':3600}

def get_seconds(input):
    unit = input[-1]
    if unit in time_units:
        time_value = int(input[:-1])
        return time_value * time_units[unit]
    else:
        return int(input)

def format_time(seconds):
    if seconds >= time_units['h']:
        return f"{seconds // time_units['h']} hour(s)"
    elif seconds >= time_units['m']:
        return f"{seconds // time_units['m']} minute(s)"
    else:
        return f"{seconds} second(s)"

def send_notification(message):
    os.system("notify-send --expire-time=30000 'Timer' '%s'" % message)

# i dont know how i feel about this lol
def halfway_notification(total_time):
    half_time = total_time / 2
    time.sleep(half_time)
    send_notification(f'your {format_time(total_time)} timer is halfway done.')

def countdown(total_time):
    for remaining_time in range(total_time, 0, -1):
        if remaining_time >= time_units['h']:
            hours_remaining = remaining_time // time_units['h']
            minutes_remaining = (remaining_time % time_units['h']) // time_units['m']
            seconds_remaining = remaining_time % time_units['m']
            sys.stdout.write("\ryour timer: %02d:%02d:%02d remaining " % (hours_remaining, minutes_remaining, seconds_remaining))
        elif remaining_time >= time_units['m']:
            sys.stdout.write("\ryour timer: %02d:%02d remaining " % (remaining_time // time_units['m'], remaining_time % time_units['m']))
        else:
            sys.stdout.write("\ryour timer: %s remaining " % format_time(remaining_time))
        
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write("\r" + " " * 80 + "\n")
    sys.stdout.flush()

    send_notification(f'your {format_time(total_time)} timer is up!')

def validate_input(input_length):
    try:
        if input_length.isdigit() or (input_length[-1] in time_units and input_length[:-1].isdigit()):
            return True
        else:
            return False
    except ValueError:
        return False

def main():
    input_length = input("enter timer length: ")
    while not validate_input(input_length):
        print("invalid input. please enter a valid timer length (e.g., 5s, 10m, 1h).")
        input_length = input("enter timer length: ")

    total_time = get_seconds(input_length)

    try:
        if total_time >= 60:
            halfway_thread = th.Thread(target=halfway_notification, args=(total_time,))
            halfway_thread.start()

        countdown_thread = th.Thread(target=countdown, args=(total_time,))
        countdown_thread.start()

        countdown_thread.join()
        print(f"\nyour {format_time(total_time)} timer is up!")

    except KeyboardInterrupt:
        print("\ntimer stopped.")

if __name__ == "__main__":
    main()
