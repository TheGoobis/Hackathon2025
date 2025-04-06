from flask import Blueprint, make_response, jsonify, render_template, request, redirect, url_for, flash
from .controller import autocomplete_species #for the search bar
from app.sightings import get_observations #the main iNaturalist API call function is here
import folium #for maps


main = Blueprint('main', __name__, template_folder='templates') #just to make sure its getting the right template folder

#the route for the map as a post request
@main.route('/', methods=['GET'])
def index():
    return render_template("index.html")

#the route for the map as a post request
@main.route('/map', methods=['POST'])
def show_map():
    species = request.form.get("species")
    # use sightings.py to get observations from iNaturalist API call
    # generate the folium map and return it

    if not species: #if there isn't a species provided
        return "No species provided.", 400
    
    observations = get_observations(species) #get the sightings of the entered species
    if not observations: #if no sightings found
        return f"No sightings found for '{species}'", 404

    #start folium map centered on the first observation
    first = observations[0]
    m = folium.Map(location=[first['lat'], first['lng']], zoom_start=4)

    for obs in observations:
        popup = f"{obs['name']}<br>{obs['date']}"
        if obs["photo"]:
            popup += f"<br><img src='{obs['photo']}' width='100'>"

        folium.Marker(
            location=[obs['lat'], obs['lng']],
            popup=popup
        ).add_to(m)

    #save the map to an HTML file so you can pull it up in web app
    m.save("app/static/folium_map.html")
    return render_template("map.html", species = species)

#route for the controller that autocompletes search queries
@main.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("q", "")
    suggestions = autocomplete_species(query)
    return jsonify(suggestions)