from flask_restx import Namespace, Resource, fields


booking_namepace = Namespace("Booking", description="The booking namespace")

booking_model = booking_namepace.model(
    "Booking", {
        "id": fields.String(),
        "num_of_people": fields.Integer(required=True),
        "booker_first_name": fields.String(required=True),
        "booker_last_name": fields.String(required=True),
        "booking_time": fields.String(required=True),
        "booker_email": fields.String(required=True),
        "booker_phone": fields.String(required=True),
        "booker_occasion": fields.String(),
        "booker_request": fields.String()
    }
)


# @booking_namepace.route("/")