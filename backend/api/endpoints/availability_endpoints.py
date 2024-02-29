from flask_restx import Namespace, Resource
from flask import request, Response
from http import HTTPStatus
from ..models.restaurant import Restaurant
from datetime import datetime
import json
from ..services.restaurant.find_available_tables import find_available_tables

avail_namespace = Namespace("Availability", description="Availability Namespace")


@avail_namespace.route("/<slug>")
class Availability(Resource):
    """Availability class"""
    def get(self, slug):
        """Return the avilable times"""
        data = request.args

        restaurant = Restaurant.query.filter_by(slug=slug).first()
        if not restaurant:
            return Response(json.dumps({"msg": "Restaurant not found!"}), status=400, mimetype='application/json')

        search_times_with_tables = find_available_tables(data, restaurant)
        if not search_times_with_tables:
            return Response(json.dumps({"msg": "Can't find search times with tables!"}), status=400, mimetype='application/json')

        availabilities = []
        for search_time in search_times_with_tables:
            sum_seats = sum([table['seats'] for table in search_time['tables']])
            is_after_opening = datetime.fromisoformat(search_time['date']) >= datetime.fromisoformat(f"{data['date']} {str(restaurant.open_time) + '.000Z'}")
            is_before_closing = datetime.fromisoformat(search_time['date']) < datetime.fromisoformat(f"{data['date']} {str(restaurant.close_time) + '.000Z'}")
            if is_after_opening and is_before_closing:
                availabilities.append({
                    'time': search_time['time'],
                    'available': sum_seats >= int(data['party_size'])
                })

        return availabilities, HTTPStatus.OK
