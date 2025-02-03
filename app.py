from flask import Flask, render_template
import geopandas as gpd
import folium
from folium import plugins

app = Flask(__name__)

@app.route('/')
def map_view():
    # Load Data
    BDR_Points = gpd.read_file("./data/BDR_Points.geojson")

    # Map Initialization
    m = folium.Map(location=[BDR_Points.geometry.y.mean(), BDR_Points.geometry.x.mean()],
            zoom_start=13,
            tiles="OpenStreetMap",
            control_scale=True
    )
    m.get_root().html.add_child(folium.Element("""
        <style>
            /* Move the zoom control to the bottom right corner */
            .leaflet-control-zoom {
                position: absolute !important;
                bottom: 10px;
                right: 10px;
            }
        </style>
    """))

    # Marker Loop
    for idx, row in BDR_Points.iterrows():
        image_url = f"images/{row['Image_Url']}"

        icon_html = f'''
    <div style="position: relative; width: 30px; height: 30px; background-color: lightblue;
    border-radius: 50%; padding: 5px; border: 2px solid blue;
    display: flex; justify-content: center; align-items: center;">
        <img src='images/GoogleAptIcon.png' style="width: 20px; height: 20px;"/>  
        <div style="position: absolute; bottom: -1.5px; font-size: 7px; color: blue; font-weight: bold;">
            {row['Page_No']}
        </div>
    </div>
''' 
        
        popup_html = f'''
<div style="font-family: 'Fira Code', monospace; border: 2px solid black; padding: 7px; border-radius: 5px; background-color: white;">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&display=swap');
        h4 {{
            font-family: 'Fira Code', monospace;
            font-weight: 700;
            color: #17365d; /* Hex color for heading */
            text-transform: uppercase;
        }}
        p {{
            color: #17365d; /* Hex color for paragraph text */
        }}
        a {{
            color: #0066cc; /* Hex color for links */
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
    <h4>{row["Name"]}</h4>
    <img src="{image_url}" alt="Building Image" style="width: 200px; height: auto;" />
    <p style="font-weight: 700;">{row["Neighborhood"]}</p>
    <p style="font-weight: 700;">{row["Address"]}</p>
    <p style="font-weight: 700;">{row["Type"]}</p>
    <p style="font-weight: 700;">{row["Status"]}</p>
    <p style="font-weight: 700;">About: </p>
    <p style="font-weight: 400;">{row["Description"]}</p>
    <p style="font-weight: 700;">Learn more: <a href="{row["Link"]}" target="_blank">Click here</a></p>
    <p style="font-weight: 700;">Page No: {row["Page_No"]}</p>
</div>
''' 
    # Marker Plot
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            icon=folium.DivIcon(html=icon_html),
            tooltip=row['Name'],
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)

    # Save Map to HTML
    map_html_path = "static/map_with_images.html"
    m.save(map_html_path)

    # Render Map in Flask Template
    return render_template('index.html', map_html=map_html_path)

if __name__ == "__main__":
    app.run(debug=False)
