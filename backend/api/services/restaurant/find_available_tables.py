from flask import Response
from datetime import datetime, timezone
from ...models.booking import Booking
import json
import os
import copy


times_path = os.path.realpath(os.path.join(os.getcwd(), "times.json"))

def find_available_tables(data, restaurant):
    # data = avail_namespace.payload
    with open(times_path) as f:
        times = json.load(f)

    search_times = [item for item in times if datetime.fromisoformat(f"{data['date']}T{item['time']}") == datetime.fromisoformat(f"{data['date']}T{data['time']}").replace(tzinfo=timezone.utc)]
    if not search_times:
        response = Response(json.dumps({"msg": "Invalid data provided!"}), status=400, mimetype='application/json')
        return response

    times = search_times[0]['search_times']
    start_time = datetime.fromisoformat(f"{data['date']} {times[0]}")
    end_time = datetime.fromisoformat(f"{data['date']} {times[len(times) - 1]}")
    bookings = Booking.query.filter(Booking.booking_time >= start_time, Booking.booking_time <= end_time).all()
    response = {
        **search_times[0],
        "bookings": [{
            "id": booking.id,
            "num_people": booking.num_of_people,
            "booking_time": str(booking.booking_time),
            "booker_email": booking.booker_email,
            "tables": [
                {
                    "booking_id": booking.tables[0].bookings[0].id,
                    "table_id": booking.tables[0].id,
                    "seats": booking.tables[0].seats,
                }
            ]
        } for booking in bookings]
    }

    bookingTablesObj = {}
    for booking in bookings:
        bookingTablesObj[str(booking.booking_time) + '+00:00'] = {table.id: True for table in booking.tables}

    tables = [{
        "id": table.id,
        "seats": table.seats,
        "restaurant_id": restaurant.id
    } for table in restaurant.tables]

    search_times_with_tables = []
    for time in search_times[0]['search_times']:
        search_times_with_tables.append({
            "date": str(datetime.fromisoformat(f"{data['date']} {time}")),
            "time": time,
            "tables": copy.deepcopy(tables)
        })
    
    for item in search_times_with_tables:
        if item['date'] in bookingTablesObj.keys():
            for i, table in enumerate(item['tables']):
                if table['id'] in bookingTablesObj[item['date']].keys():
                    del item['tables'][i]

    return search_times_with_tables