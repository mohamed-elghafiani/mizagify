"""Generate the availability time slots"""
import json


def get_time(min, type="time"):
    """Create a time slot from a provided hour and min"""
    if min < 0:
        return None

    hour = min // 60
    if hour == 24:
        hour = 0
    if hour > 24:
        hour = hour % 24

    min = min % 60
    if type == "dispaly":
        return f"{hour:02d}:{min:02d}"
    return f"{hour:02d}:{min:02d}:00.000Z"

data = []
for min in range(60, 1470, 30):
    d = {
        "display_time": get_time(min, type="dispaly"),
        "time": get_time(min),
        "search_times": [get_time(time) for time in range(min - 60, min + 90, 30) if get_time(time)]
    }
    data.append(d)

with open("times.json", "w") as f:
    json.dump(data, f)