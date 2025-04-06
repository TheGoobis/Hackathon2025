import requests

#this is an autocomplete API call from iNaturalist for the search function
def autocomplete_species(partial_name):
    url = "https://api.inaturalist.org/v1/taxa/autocomplete"
    params = {"q": partial_name, "per_page": 10}
    try:
        res = requests.get(url, params=params)
        results = res.json().get("results", [])
        #return a list of dicts with common and scientific names
        suggestions = []
        for r in results:
            sci_name = r.get("name")
            common_name = r.get("preferred_common_name") or ""
            if sci_name:
                label = f"{common_name} ({sci_name})" if common_name else sci_name
                suggestions.append({
                    "label": label, #what shows up
                    "value": sci_name  #what will actually be submitted
                })
        return suggestions
    except Exception:
        return []