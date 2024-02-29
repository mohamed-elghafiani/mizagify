from flask_restx import Namespace, Resource, fields
from ..models.restaurant import Restaurant, Cuisine, Item, Location, Table
from http import HTTPStatus
from datetime import time
import uuid
from ..utils import db
from flask_cors import cross_origin
from flask import request, Response
import json


restaurant_namepace = Namespace("Restaurant", description="The restaurant namespace")

review_model = restaurant_namepace.model(
    "Review", {
        "id": fields.String(),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "text": fields.String(),
        "rating": fields.Integer(),
        "restaurant_id": fields.String(),
        "user_id": fields.String()
    }
)

restaurant_model = restaurant_namepace.model(
    "Restaurant", {
        "id": fields.String(),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "open_time": fields.String(required=True),
        "close_time": fields.String(required=True),
        "price": fields.String(required=True, enum=["CHEAP", "REGULAR", "EXPENSIVE"]),
        "location": fields.String(required=True),
        "cuisine": fields.String(required=True),
        "images": fields.String(required=True),
        "reviews": fields.List(fields.Nested(review_model)),
        "cuisine_id": fields.String(),
        "slug": fields.String()
    }
)

rest_images_model = restaurant_namepace.model(
    "RestaurantImages", {
        "primary": fields.String(required=True),
        "secondary": fields.List(fields.String(), required=True)
    }
)

image_model = restaurant_namepace.model(
    "ImageModel", {
        "id": fields.String(),
        "restaurant_id": fields.String(),
        "url": fields.String(),
        "type": fields.String()
    }
)

@restaurant_namepace.route("/")
class RestGetCreate(Resource):
    """"Get and create restaurant"""
    @restaurant_namepace.marshal_list_with(restaurant_model)
    def get(self):
        """Resturn all restaurants"""
        restaurants = Restaurant.query.all()
        response_data = []
        for restaurant in restaurants:
            response_data.append({
                "id": restaurant.id,
                "name": restaurant.name,
                "description": restaurant.description,
                "open_time": restaurant.open_time,
                "close_time": restaurant.close_time,
                "price": restaurant.price,
                "location": Location.query.filter_by(id=restaurant.location_id).first().name,
                "cuisine": Cuisine.query.filter_by(id=restaurant.cuisine_id).first().name,
                "images": restaurant.images,
                "reviews": restaurant.reviews,
                "slug": restaurant.slug
            })
        return response_data, HTTPStatus.OK

    @restaurant_namepace.expect(restaurant_model)
    @restaurant_namepace.marshal_with(restaurant_model)
    def post(self):
        """Create a restaurant"""
        data = restaurant_namepace.payload

        # Create cuisine if not existent
        cuisine = Cuisine.query.filter_by(name=data["cuisine"].lower()).first()
        if not cuisine:
            Cuisine(name=data["cuisine"].lower()).save()
        
        location = Location.query.filter_by(name=data["location"].lower()).first()
        if not location:
            Location(name=data["location"].lower()).save()

        try:
            ot_hour, ot_min = list(map(int, data["open_time"].split(":")))
            ct_hour, ct_min = list(map(int, data["close_time"].split(":")))
            images = f"main::{data['main_image']}||other::{';'.join(data['images'])}"
            new_restaurant = Restaurant(
                name=data["name"],
                description=data["description"],
                open_time=time(ot_hour, ot_min),
                close_time=time(ct_hour, ct_min),
                price=data["price"],
                location_id=Location.query.filter_by(name=data["location"].lower()).first().id,
                cuisine_id=Cuisine.query.filter_by(name=data["cuisine"].lower()).first().id,
                slug=data["slug"],
                images=images
            )
            new_restaurant.save()
            print("Restaurant Added!")
        except Exception as e:
            print("ERROR!", e)
            return "ERROR! something went wrong"
        
        return new_restaurant, HTTPStatus.CREATED

@restaurant_namepace.route("/<restaurant_slug>")
class RestaurantImage(Resource):
    """Restaurant Images Route"""
    @restaurant_namepace.marshal_with(restaurant_model)
    def get(self, restaurant_slug):
        """Retrieve restaurant iamges"""
        restaurant = Restaurant.query.filter_by(slug=restaurant_slug).first()
        if restaurant:
            data = {
                "id": restaurant.id,
                "name": restaurant.name,
                "description": restaurant.description,
                "open_time": restaurant.open_time,
                "close_time": restaurant.close_time,
                "price": restaurant.price,
                "location": restaurant.location,
                "cuisine": Cuisine.query.filter_by(id=restaurant.cuisine_id).first().name,
                "images": restaurant.images,
                "reviews": restaurant.reviews,
                "slug": restaurant.slug
            }

            return data, HTTPStatus.OK

@restaurant_namepace.route("/<restaurant_slug>/images")
class RestaurantImage(Resource):
    """Restaurant Images Route"""
    @restaurant_namepace.marshal_list_with(image_model)
    def get(self, restaurant_slug):
        """Retrieve restaurant iamges"""
        restaurant = Restaurant.query.filter_by(slug=restaurant_slug).first()
        images = restaurant.images

        return images, HTTPStatus.OK

    # @restaurant_namepace.expect(rest_images_model)
    # @restaurant_namepace.marshal_list_with(image_model)
    # def post(self, restaurant_slug):
    #     """Add restaurant image"""
    #     data = restaurant_namepace.payload

    #     restaurant = Restaurant.query.filter_by(slug=restaurant_slug).first()
    #     Image(
    #         url=data["primary"],
    #         type="PRIMARY",
    #         restaurant_id=restaurant.id
    #     ).save()
        
    #     for img in data["secondary"]:
    #         Image(
    #             url=img,
    #             type="SECONDARY",
    #             restaurant_id=restaurant.id
    #         ).save()

    #     images = Restaurant.query.filter_by(id=restaurant.id).first().images
    #     return images, HTTPStatus.CREATED


item_model = restaurant_namepace.model(
    "Item", {
        "name": fields.String(required=True),
        "price": fields.String(required=True),
        "description": fields.String(required=True)
    }
)

@restaurant_namepace.route("/<restaurant_slug>/items")
class AddItems(Resource):
    """GET/POST restaurant's menu items to database"""
    @restaurant_namepace.marshal_list_with(item_model)
    def get(self, restaurant_slug):
        """Retrieve restaurant's menu items"""
        restaurant = Restaurant.query.filter_by(slug=restaurant_slug).first()
        if not restaurant:
            return {"msg": f"No restaurant with slug={restaurant_slug} found in database!"}
        
        print("Items returned: ", len(restaurant.items))
        return restaurant.items, HTTPStatus.OK

    @restaurant_namepace.expect(item_model)
    def post(self, restaurant_slug):
        """Retrieve restaurant's menu items"""
        restaurant = Restaurant.query.filter_by(slug=restaurant_slug).first()
        if not restaurant:
            return {"msg": f"No restaurant with slug={restaurant_slug} found in database!"}
        
        data = restaurant_namepace.payload

        try:
            item = Item(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                restaurant_id=restaurant.id
            )
            item.save()
            print("Items saved to database successfully!")
            return {"msg": "Item was added successfully to database!"}

        except:
            print("An error occured!")
            return {"msg": "Error Saving item to database!"}


@restaurant_namepace.route("/location/<location>")
class RestaurantsByLocation(Resource):
    """Retrieve restaurants by location"""
    @restaurant_namepace.marshal_list_with(restaurant_model)
    def get(self, location):
        """retrieve restaurants by location"""
        location = Location.query.filter_by(name=location.lower()).first()
        if not location:
            return [], HTTPStatus.NOT_FOUND
        
        restaurants = Restaurant.query.filter_by(location_id=location.id).all()
        if restaurants:
            data = []
            for item in restaurants:
                data.append({
                    "id": item.id,
                    "name": item.name,
                    "price": item.price,
                    "location": location.name,
                    "cuisine": Cuisine.query.filter_by(id=item.cuisine_id).first().name,
                    "images": item.images,
                    "slug": item.slug,
                })
            return data, HTTPStatus.OK
        return [], HTTPStatus.OK


cuisine_model = restaurant_namepace.model(
    "Cuisine", {
        "name": fields.String(required=True)
    }
)

@restaurant_namepace.route("/cuisines")
class GetCuisines(Resource):
    """Retrieve all cuisines available"""
    @restaurant_namepace.marshal_list_with(cuisine_model)
    def get(self):
        """Retrieve all cuisines"""
        cuisines = Cuisine.query.all()
        filtered_cuisines = []
        for item in cuisines:
            if not any([el["name"] == item.name for el in filtered_cuisines]):
                filtered_cuisines.append({
                    "name": item.name
                }) 
        return filtered_cuisines, HTTPStatus.OK
    
location_model = restaurant_namepace.model(
    "Location", {
        "name": fields.String(required=True)
    }
)

@restaurant_namepace.route("/locations")
class GetCuisines(Resource):
    """Retrieve all cuisines available"""
    @restaurant_namepace.marshal_list_with(location_model)
    def get(self):
        """Retrieve all cuisines"""
        locations = Location.query.all()
        filtered_locations = []
        for item in locations:
            if not any([el["name"] == item.name for el in filtered_locations]):
                filtered_locations.append({
                    "name": item.name
                })
        return filtered_locations, HTTPStatus.OK



@restaurant_namepace.route("/filter")
class FilterResults(Resource):
    """Filter the results based on @params -> [location, cuisine, price]"""
    @restaurant_namepace.marshal_list_with(restaurant_model)
    def get(self):
        """Filter the results based on params"""
        # params = restaurant_namepace.payload
        city = request.args.get("city")
        cuisine_name = request.args.get("cuisine")
        price = request.args.get("price")

        cuisine = Cuisine.query.filter_by(name=cuisine_name).first()
        location = Location.query.filter_by(name=city.lower()).first()
        if all([location, cuisine, price]):
            restaurants = Restaurant.query.filter_by(location_id=location.id, price=price, cuisine_id=cuisine.id).all()
        elif location and price:
            restaurants = Restaurant.query.filter_by(location_id=location.id, price=price).all()
        elif location and cuisine:
            restaurants = Restaurant.query.filter_by(location_id=location.id, cuisine_id=cuisine.id).all()
        elif location:
            restaurants = Restaurant.query.filter_by(location_id=location.id).all()
        else:
            return [], HTTPStatus.OK
        
        response_data = []
        for restaurant in restaurants:
            response_data.append({
                "id": restaurant.id,
                "name": restaurant.name,
                "description": restaurant.description,
                "open_time": restaurant.open_time,
                "close_time": restaurant.close_time,
                "price": restaurant.price,
                "location": Location.query.filter_by(id=restaurant.location_id).first().name,
                "cuisine": Cuisine.query.filter_by(id=restaurant.cuisine_id).first().name,
                "images": restaurant.images,
                "reviews": restaurant.reviews,
                "slug": restaurant.slug
            })
        return response_data, HTTPStatus.OK
    

# ========================================================
# ==================== CREATE TABLES =====================
table_model = restaurant_namepace.model("Table", {
    "name": fields.String("Table name", required=True),
    "seats": fields.Integer("Number of seats", required=True),
})

@restaurant_namepace.route("/<slug>/create_table")
class CreateTable(Resource):
    """Create a table"""
    @restaurant_namepace.expect(table_model)
    def post(self, slug):
        """Create a table route"""
        data = restaurant_namepace.payload

        restaurant = Restaurant.query.filter_by(slug=slug).first()
        if not restaurant:
            return Response(json.dumps({"msg": "Restautant not found!"}), status=400, mimetype='application/json')

        try:
            new_table = Table(name=data["name"], seats=data["seats"], restaurant_id=restaurant.id)
            new_table.save()
            return Response(json.dumps({"msg": "Table was created successfully!"}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            return Response(json.dumps({"msg": "Something wrong happened, please try again later!"}), status=500, mimetype='application/json')
