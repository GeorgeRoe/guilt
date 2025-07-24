from datetime import timedelta

def parse_timedelta_string(time_str: str) -> timedelta:
    if '-' in time_str:
        days_part, time_part = time_str.split('-', 1)
        days = int(days_part)
    else:
        days = 0
        time_part = time_str

    parts = time_part.split(':')

    if len(parts) == 1:
        minutes = int(parts[0])
        hours = 0
        seconds = 0
    elif len(parts) == 2:
        if days > 0:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = 0
        else:
            minutes = int(parts[0])
            seconds = int(parts[1])
            hours = 0
    elif len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
    else:
        raise ValueError(f"Invalid time format: {time_str}")

    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)