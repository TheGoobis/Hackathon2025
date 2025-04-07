#helper function for displaying animal sightings on the folium map
import requests #html requests

def get_observations(species_name, per_page = 50):
    #this is the 'data set' we are using. An API call to iNaturalist to get any
    #   and all sightings with a species lookup on a map
    url = "https://api.inaturalist.org/v1/observations"

    #get species info
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

        #get type of search (plant, animal, fungi, whatever) to change folium map icon!!
        icon_type = "camera"  #the default icon if this doesn't work for whatever reason
        if "taxon" in item and "iconic_taxon_name" in item["taxon"]: #taxon is scientific name for species i think (its what iNaturalist uses)
            group = item.get("taxon", {}).get("iconic_taxon_name", "")
            icon_map = {
                "Plantae": ("leaf", "green"),
                "Fungi": ("mound", "orange"),
                "Insecta": ("bugs", "purple"),
                "Mammalia": ("paw", "blue"),
                "Arachnida": ("spider", "black"),
                "Reptilia": ("worm", "red"),
                "Amphibia": ("frog", "darkgreen"),
                "Actinopterygii": ("fish-fins", "beige"),
                "Aves": ("dove", "gray")
            }
            #use defaults if group not found
            icon_type, icon_color = icon_map.get(group, ("camera", "white"))

        #used to build map. Is sent to route.py /map route
        observations.append({
            "lat": lat,
            "lng": lng,
            "name": name,
            "date": date,
            "photo": photo,
            "icon": icon_type,
            "color": icon_color
        })

    return observations