from flask import Blueprint, jsonify, render_template, request
from .controller import autocomplete_species #for the search bar
from app.sightings import get_observations #the main iNaturalist API call function is here
import folium #for maps
#imports for graphs
import json

main = Blueprint('main', __name__, template_folder='templates') #just to make sure its getting the right template folder

#the route for the map as a post request
@main.route('/', methods=['GET'])
def index():
    #for chart 1
    with open("app/static/avg_trend.json") as f:
        bar_data = f.read()

    #for chart 2
    with open("app/static/species_trends.json") as f:
        line_data = f.read()
    return render_template("index.html", bar_data=bar_data, line_data=line_data)

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
        #the gathered info
        name = obs["name"]
        date = obs["date"]
        photo = obs["photo"]
        icon_type = obs["icon"]
        icon_color = obs["color"]

        #---------old popup code ---------
        # popup = f"{obs['name']}<br>{obs['date']}"
        # if obs["photo"]:
        #     popup += f"<br><img src='{obs['photo']}' width='100'>"

        #popup code to allow image enlargememt
        popup_html = f"""
            <div style = 'font-family: Arial, sans-serif; max-width: 200px;'>
                <h6 style = 'mb-5;'>{name}</h6>
                <p style = 'margin:0; font-size: 12px;'>Observed on: {date}</p>
                {'<a href="' + photo + '" target = "_blank"><img src="' + photo + '"width="150" style = "mt-5; border-radius: 6px;"></a>' if photo else ''}
            </div>"""

        folium.Marker(
            location=[obs['lat'], obs['lng']],
            popup=folium.Popup(popup_html, max_width= 250), icon = folium.Icon(color = icon_color, icon = icon_type, prefix = 'fa')
        ).add_to(m) #add to map

    #save the map to an HTML file so you can pull it up in web app
    m.save("app/static/folium_map.html")
    return render_template("map.html", species = species)

#route for the controller that autocompletes search queries
@main.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("q", "")
    suggestions = autocomplete_species(query)
    return jsonify(suggestions)
