from app import create_app
import os
import atexit

app = create_app()
MAP_FILE = "app/static/folium_map.html"

#cleanup function to clear the folium map when exiting the app
# this is to prevent sending a new folium_map to github each time
def remove_folium_map():
    if os.path.exists(MAP_FILE):
        os.remove(MAP_FILE)
        print(f"[Cleanup] Deleted: {MAP_FILE}")

atexit.register(remove_folium_map)

# Run app
if __name__ == "__main__":
    app.run(debug=True)