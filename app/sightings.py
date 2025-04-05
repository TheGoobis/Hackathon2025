#helper function for displaying animal sightings on the folium map
import requests #html requests

def get_observations(species_name, per_page = 50):
    #this is the 'data set' we are using. An API call to iNaturalist to get any
    #   and all sightings with a species lookup on a map
    url = "https://api.inaturalist.org/v1/observations"

    params = {
        "taxon_name": species_name,
        "per_page": per_page,
        "order_by": "observed_on",
        "order": "desc"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json().get("results", [])
    observations = []

    #going through each observation
    for item in data:
        if not item.get("geojson"): #if a obs doesn't have a geo location, skip it
            continue
        #folium expects (lat, lng) so we get lat then lng
        lat = item["geojson"]["coordinates"][1]
        lng = item["geojson"]["coordinates"][0]
        name = item["species_guess"] or species_name #best guess at what was observed, the fallback is species name searched
        date = item["observed_on"] or "Unknown"
        photo = item["photos"][0]["url"].replace("square", "medium") if item["photos"] else None

        #used to build map
        observations.append({
            "lat": lat,
            "lng": lng,
            "name": name,
            "date": date,
            "photo": photo
        })

    return observations