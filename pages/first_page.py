import streamlit as st
from streamlit.components.v1 import html
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2



st.set_page_config(page_title="Mulder's Map", 
                   page_icon="🌍", 
                   layout="wide", 
                   menu_items={
                              'Get Help': 'https://www.extremelycoolapp.com/help',
                              'Report a bug': "https://www.extremelycoolapp.com/bug",
                              'About': "# This is a header. This is an *extremely* cool app!"
                  })
ClarifaiStreamlitCSS.insert_default_css(st)

# # This must be within the display() function.
# auth = ClarifaiAuthHelper.from_streamlit(st)
# stub = create_stub(auth)
# userDataObject = auth.get_user_app_id_proto()

#st.title("Mulder's Map")

# Embedding Leaflet map using HTML component
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Leaflet Map</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <style>
        html,body {
            height: 100%;
            overflow: hidden;
            background-color: #000000;
            padding: 0;
            margin: 0;
        }
        .page-wrapper {
            height: 100vh;
        } 
        #mapid {
            height: 100%;
            width: 100%;
        }
        .modal {
            width: 100%;
            max-height: 100%;
            text-align: center;
            vertical-align: top;
            z-index: 999999;
        }
        #myModal {
            background-color:rgba(0, 0, 0, .8);
        }
        .modal-dialog {
            display: inline-block;
            text-align: left;
            vertical-align: middle;
            margin-right: 0;
            margin-left: 0;
            min-width: 50%;
            max-width: 80%;
        }
        table{
            table-layout: fixed;
        }
        .modal-content {
            max-width: 100%;
            width: 100%;
            margin-right: 0;
            margin-left: 0;
            border: none;
            opacity: 0.97;
        }
        .modal-header {
            border-bottom: None;
            height:30px;
            padding: 0px;
            background-color:#212529;
            color:#212529;
            opacity:0.9;
        }
        .modal-footer {
            border-top: None;
            background-color:#212529;
            color:#212529;
            opacity:0.9;
        }
        .modal-title {
            margin-top:0px;
            font-size:16px;
        }
        .modal-header .close {
            margin-right:-2px;
            color:#fff;
        }
        .modal-body {
            background-color:#212529;
            opacity:0.9;
            width:100%;
            color:grey;
            padding: 15px 15px 15px 15px;
            border-style: none;
        }
        .modal-body h3 {
            text-align: center;
        }
        .modal-body p {
            padding-top:10px;
            font-size: 1.1em;
        }
        .cover {
            object-fit: cover;
        }
        #container1 {
            height: auto;
            width: auto;
            max-width: 100%;
            overflow: auto;
            overflow-y: auto;
        }
        .widget-area.blank {
            background: none repeat scroll 0 0 rgba(0, 0, 0, 0);
            box-shadow: none;
        }
        .widget-area {
            background-color: #fff;
            border-radius: 4px;
            box-shadow: 0 0 16px rgba(0, 0, 0, 0.05);
            float: left;
            margin-top: 5px;
            padding: 25px 30px;
            position: relative;
            width: 100%;
        }
        .row{
            display: block;
            flex-wrap: wrap;
            margin-right: -15px;
            margin-left: -15px;
        }
        .status-upload {
            background: #f5f5f5;
            border-radius: 4px;
            float: left;
            width: 100%;
        }
        .status-upload form {
            float: left;
            width: 100%;
        }
        .status-upload form textarea {
            background: #fff;
            border: 1px solid #F2F2F2;
            border-radius: 4px 4px 0 0;
            color: #777777;
            float: left;
            font-family: Lato;
            font-size: 14px;
            height: 180px;
            letter-spacing: 0.3px;
            padding: 20px;
            width: 100%;
            resize: vertical;
            outline: none;
        }
        pre {
            color: #ddd;
        }
        .status-upload ul {
            float: left;
            list-style: none outside none;
            margin: 0;
            padding: 0 0 0 15px;
            width: auto;
        }
        .status-upload ul > li {
            float: left;
        }
        .status-upload ul > li > a {
            border-radius: 4px;
            color: #777777;
            float: left;
            font-size: 14px;
            height: 30px;
            line-height: 30px;
            margin: 10px 0 10px 10px;
            text-align: center;
            transition: all 0.4s ease 0s;
            width: 30px;
            cursor: pointer;
        }
        .status-upload ul > li > a:hover {
            background: #606060;
            color: #fff;
        }
        .status-upload form button {
            border: none;
            border-radius: 4px;
            color: #fff;
            float: right;
            font-family: Lato;
            font-size: 14px;
            letter-spacing: 0.3px;
            margin-right: 9px;
            margin-top: 9px;
            padding: 6px 15px;
        }
        .dropdown > a > span.green:before {
            border-left-color: #2dcb73;
        }
        .chiller-theme .sidebar-wrapper {
            background: #31353D;
        }
        .chiller-theme .sidebar-wrapper .sidebar-header,
        .chiller-theme .sidebar-wrapper .sidebar-search,
        .chiller-theme .sidebar-wrapper .sidebar-menu {
            border-top: 0px solid #3a3f48;
        }
        .chiller-theme .sidebar-wrapper .sidebar-search input.search-menu,
        .chiller-theme .sidebar-wrapper .sidebar-search .input-group-text {
            border-color: transparent;
            box-shadow: none;
        }
        .chiller-theme .sidebar-wrapper .sidebar-header .user-info .user-role,
        .chiller-theme .sidebar-wrapper .sidebar-header .user-info .user-status,
        .chiller-theme .sidebar-wrapper .sidebar-search input.search-menu,
        .chiller-theme .sidebar-wrapper .sidebar-search .input-group-text,
        .chiller-theme .sidebar-wrapper .sidebar-brand > a,
        .chiller-theme .sidebar-wrapper .sidebar-menu ul li a,
        .chiller-theme .sidebar-wrapper .sidebar-footer > a {
            color: #818896;
        }
        .chiller-theme .sidebar-wrapper .sidebar-menu ul li:hover > a,
        .chiller-theme .sidebar-wrapper .sidebar-menu .sidebar-dropdown.active > a,
        .chiller-theme .sidebar-wrapper .sidebar-header .user-info,
        .chiller-theme .sidebar-wrapper .sidebar-brand > a:hover,
        .chiller-theme .sidebar-wrapper .sidebar-footer > a:hover i {
            color: #b8bfce;
        }
        .page-wrapper.chiller-theme.toggled #close-sidebar,
        .page-wrapper.chiller-theme.toggled #close-sidebar2 {
            color: #bdbdbd;
        }
        .page-wrapper.chiller-theme.toggled #close-sidebar:hover,
        .page-wrapper.chiller-theme.toggled #close-sidebar2:hover {
            color: #ffffff;
        }
        .chiller-theme .sidebar-wrapper ul li:hover a i,
        .chiller-theme .sidebar-wrapper .sidebar-dropdown .sidebar-submenu li a:hover:before,
        .chiller-theme .sidebar-wrapper .sidebar-search input.search-menu:focus + span,
        .chiller-theme .sidebar-wrapper .sidebar-menu .sidebar-dropdown.active a i {
            color: #16c7ff;
            text-shadow: 0px 0px 10px rgba(22, 199, 255, 0.5);
        }
        .chiller-theme .sidebar-wrapper .sidebar-menu ul li a i,
        .chiller-theme .sidebar-wrapper .sidebar-menu .sidebar-dropdown div,
        .chiller-theme .sidebar-wrapper .sidebar-search input.search-menu,
        .chiller-theme .sidebar-wrapper .sidebar-search .input-group-text {
            background: #3a3f48;
        }
        .chiller-theme .sidebar-wrapper .sidebar-menu .header-menu span {
            color: #6c7b88;
        }
        .chiller-theme .sidebar-footer {
            background: #3a3f48;
            box-shadow: 0px -1px 5px #282c33;
            border-top: 1px solid #464a52;
        }
        .chiller-theme .sidebar-footer > a:first-child {
            border-left: none;
        }
        .chiller-theme .sidebar-footer > a:last-child {
            border-right: none;
        }
    </style>
</head>
<body class="page-wrapper chiller-theme ">
    <div id="mapid"></div>
    <div id="myModal" class="modal fade" role="dialog">
        <div class="modal-dialog">
            <div class="modal-content">
                <div id="mhead" class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                </div>
                <div id="modcont" class="modal-body">
                    <div class="container">
                        <div class="row">
                            <h3>Placeholder Modal</h3>
                        </div>
                        <div class="row">
                            <div>
                                <div class="widget-area no-padding blank">
                                    <div class="status-upload">
                                        <form name="form4" action="#" onsubmit="subcomment();return false">
                                            <textarea id="commentsection" placeholder="Type some stuff here?"></textarea>
                                            <button type="submit" class="btn btn-success green">
                                                <i class="fa fa-share"></i> Submit
                                            </button>
                                        </form>
                                    </div>
                                    <!-- Status Upload  -->
                                </div>
                                <!-- Widget Area -->
                            </div>
                        </div>
                    </div>
                </div>
                <div id="mfoot" class="modal-footer">
                    <button id="closemodal" type="button" class="btn btn-secondary btn-sm" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        function subcomment() {
            console.log("subcomment");
        }

        var mymap = L.map('mapid').setView([38.26741,-77.71869], 13);
        
        // Add base layers
        var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(mymap);
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
        L.marker([38.26741,-77.71869]).addTo(mymap).on({
            click: function(e) {
                $("#myModal").modal("show");
            }
        });
    </script>
</body>
</html>

"""

# Write the HTML code to the app
st.components.v1.html(html_code, height=500)
