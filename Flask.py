# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:06:10 2024

@author: Admin
"""
import os
from flask import Flask, render_template, request, jsonify
from backend import *

app = Flask(__name__)

# Initialize the world backend
world = World()
user_manager = UserManager()

# Preload some data into the world
world.add_country("Italy")
world.add_country("France")
world.add_place_of_interest("Italy", "Colosseum")
world.add_place_of_interest("France", "Eiffel Tower")

#%%
load_world_data(world,filename="world_data_old.json")
load_user_data(user_manager,filename="user_data_old.json")

#%%
def save_data_periodically():
    global timer
    save_world_data(world)
    save_user_data(user_manager)

    timer = threading.Timer(5, save_data_periodically)
    timer.start()

def stop_timer():
    global timer
    if timer is not None:
        timer.cancel()

atexit.register(stop_timer)
save_data_periodically()


#%%

@app.route('/')
def index():
    # Pass top places to the template to be displayed
    top_places_list = world.get_top_places()
    return render_template('index.html', top_places=top_places_list)

@app.route('/add_place_of_interest', methods=['POST'])
def add_place_of_interest():
    country_name = request.form.get('country')
    place_name = request.form.get('place')
    
    # Check if country_name or place_name is None or empty
    if not country_name or not place_name:
        return jsonify({"error": "Country and place name are required."}), 400
    
    # Check if the country exists, if not, add it
    country_node = world.countries.find(country_name)
    if not country_node:
        world.add_country(country_name)
    
    # Check if the place already exists
    country_node = world.countries.find(country_name)
    place_node = country_node.places.find(place_name) if country_node else None
    if place_node:
        return jsonify({"error": f"Place '{place_name}' already exists in '{country_name}'."}), 400
    
    # Add the place of interest
    world.add_place_of_interest(country_name, place_name)
    return jsonify({"message": f"Place of interest '{place_name}' added to '{country_name}' successfully"})


@app.route('/vote_for_place', methods=['POST'])
def vote_for_place():
    country_name = request.form.get('country')
    place_name = request.form.get('place')
    feedback_content = request.form.get('feedback')
    user_id = request.form.get('user_id')
    
    user = user_manager.get_user_by_id(int(user_id))
    if user:
        country_node = world.countries.find(country_name)
        if country_node:
            place_node = country_node.places.find(place_name)
            if place_node:
                if place_name in user.voting_history:
                    # User has already voted for this place
                    return jsonify({"error": "You have already voted for this place"}), 400
                else:
                    # Vote for the place
                    user.vote_place(world, country_name, place_name, feedback_content)
                    return jsonify({"message": f"Vote cast for '{place_name}' in {country_name} successfully"})
            else:
                return jsonify({"error": f"Place '{place_name}' not found in '{country_name}'."}), 404
        else:
            return jsonify({"error": f"Country '{country_name}' not found."}), 404
    else:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404


@app.route('/get_top_places')
def get_top_places():
    top_places_json = world.get_top_places()
    return top_places_json

@app.route('/get_top_countries')
def get_top_countries():
    top_countries_info = world.get_top_countries()  
    return top_countries_info


@app.route('/get_id', methods=['GET'])
def get_id():
    user = user_manager.register_user()
    if request.method == 'GET':
        return jsonify({"id": user.user_id})
    else:
        return jsonify({"error": "Method not allowed"}), 405


@app.route('/history')
def history():
    user_id = request.args.get('id')  # Retrieve user ID from request
    if user_id:
        user = user_manager.get_user_by_id(int(user_id))  # Get the user object based on user ID
        if user:
            formatted_history_data = user.get_history()  # Call get_history method for the user
            return formatted_history_data
        else:
            return jsonify({"error": f"User with ID {user_id} not found"}), 404
    else:
        return jsonify({"error": "User ID not provided"})

@app.route('/filter_by_country')
def filter_by_country():
    country_name = request.args.get('country')
    if not country_name:
        return jsonify({"error": "Country name not provided"}), 400
    places = world.get_places_by_country(country_name)
    if places:
        return places
    else:
        return jsonify({"error": "Place not found"}), 404


@app.route('/search')
def search():
    country_name = request.args.get('country')
    place_name = request.args.get('place')
    search_data = world.find_place_data(country_name, place_name)
    if search_data:
        return search_data
    else: return jsonify({"error": "Place not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)