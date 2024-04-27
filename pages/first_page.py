import streamlit as st
from streamlit.components.v1 import html
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()

st.title("Mulder's Map")

# Embedding Leaflet map using HTML component
html_code = """
<!DOCTYPE html>
<html>
<head>
  <title>Leaflet Map</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
  <style>
    html, body { height: 100%; margin: 0; }
    #mapid { height: 100vh; }
    .fixed-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.5); /* Adjust the opacity as needed */
        z-index: 9999; /* Adjust the z-index to make sure it overlays other elements */
    }
  </style>
</head>
<body>
  <div class="fixed-overlay"></div> <!-- Add a fixed overlay to block interaction with elements below -->
  <div id="mapid"></div>
  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
  <script>
    var mymap = L.map('mapid').setView([51.505, -0.09], 13);
    
    // Add base layers
    var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    var cartoLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://carto.com/">Carto</a>'
    });

    // Add layer control
    var baseLayers = {
      "OpenStreetMap": osmLayer,
      "Carto": cartoLayer,
    };
    L.control.layers(baseLayers).addTo(mymap);
    
    // Add marker
    L.marker([51.5, -0.09]).addTo(mymap)
      .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
      .openPopup();
  </script>
</body>
</html>
"""

# Write the HTML code to the app
st.components.v1.html(html_code)
