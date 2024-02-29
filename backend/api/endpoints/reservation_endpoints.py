from flask_restx import Resource, Namespace, fields
from flask import request, Response
from http import HTTPStatus
from ..models.restaurant import Restaurant, Table
from ..models.booking import Booking
import json
from datetime import datetime, timezone
from ..services.restaurant.find_available_tables import find_available_tables


reservation_ns = Namespace("Reservation")
booker_model = reservation_ns.model("Booker", {
    "id": fields.String(),
    "booking_time": fields.String(required=True),
    "booker_email": fields.String(required=True),
    "booker_phone": fields.String(required=True),
    "booker_first_name": fields.String(required=True),
    "booker_last_name": fields.String(required=True),
    "num_of_people": fields.String(required=True),
    "booker_occasion": fields.String(required=False),
    "booker_request": fields.String(required=False),
})


@reservation_ns.route("/<slug>/reserve")
class Reserve(Resource):
    """Reserve a booking"""
    @reservation_ns.expect(booker_model)
    @reservation_ns.marshal_with(booker_model)
    def post(self, slug):
        """Reserve a booking"""
        data = request.args
        booker_data = reservation_ns.payload

        restaurant = Restaurant.query.filter_by(slug=slug).first()
        if not restaurant:
            return Response(json.dumps({"msg": "Restaurant not found!"}), status=400, mimetype='application/json')

        is_before_opening = datetime.fromisoformat(f"{data['date']} {data['time']}") < datetime.fromisoformat(f"{data['date']} {str(restaurant.open_time.replace(tzinfo=timezone.utc))}") 
        is_after_closing = datetime.fromisoformat(f"{data['date']} {data['time']}") > datetime.fromisoformat(f"{data['date']} {str(restaurant.close_time.replace(tzinfo=timezone.utc))}") 
        if is_after_closing or is_before_opening:
            return Response(json.dumps({"msg": "Restaurant is not open at that time!"}), status=400, mimetype='application/json')
        
        search_times_with_tables = find_available_tables(data, restaurant)
        if not search_times_with_tables:
            return Response(json.dumps({"msg": "Can't find search times with tables!"}), status=400, mimetype='application/json')
        
        search_time_with_tables = [search_time for search_time in search_times_with_tables if datetime.fromisoformat(search_time['date']) == datetime.fromisoformat(f"{data['date']} {data['time']}")]
        if not search_time_with_tables:
            return Response(json.dumps({"msg": "No availability at this time!"}), status=400, mimetype='application/json')

        tables_counts = {2: [], 4: []}
        for table in search_time_with_tables[0]['tables']:
            if table['seats'] == 2:
                tables_counts[2].append(table['id'])
            else:
                tables_counts[4].append(table['id'])

        tables_to_book = []
        seats_remaining = int(data['party_size'])
        while seats_remaining > 0:
            if seats_remaining >= 3:
                if len(tables_counts[4]):
                    tables_to_book.append(tables_counts[4][0])
                    tables_counts[4].pop(0)
                    seats_remaining -= 4
                else:
                    tables_to_book.append(tables_counts[2][0])
                    tables_counts[2].pop(0)
                    seats_remaining -= 2
            else:
                if len(tables_counts[2]):
                    tables_to_book.append(tables_counts[2][0])
                    tables_counts[2].pop(0)
                    seats_remaining -= 2
                else:
                    tables_to_book.append(tables_counts[4][0])
                    tables_counts[4].pop(0)
                    seats_remaining -= 4

        new_booking = Booking(
            num_of_people=data['party_size'],
            booking_time=datetime.fromisoformat(f"{data['date']} {data['time']}"),
            booker_email=booker_data['booker_email'],
            booker_phone=booker_data['booker_phone'],
            booker_first_name=booker_data['booker_first_name'],
            booker_last_name=booker_data['booker_last_name'],
            booker_occasion=booker_data['booker_occasion'],
            booker_request=booker_data['booker_request'],
            restaurant_id=restaurant.id
        )
        tables_obj = [Table.query.filter_by(id=table_id).first() for table_id in tables_to_book]
        new_booking.tables.extend(tables_obj)

        new_booking.save()

        return new_booking, HTTPStatus.OK
