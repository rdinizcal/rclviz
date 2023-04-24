import requests
from typing import Dict, List
from geopy.geocoders import Nominatim
from lxml import etree

from scholarly import scholarly

from time import sleep
from tqdm import tqdm

import sys

def clean_affiliation(affiliation : str) -> str:
    separator = ','
    affiliation= affiliation.split(separator,1)[1] if separator in affiliation else affiliation
    separator = ' at '
    affiliation= affiliation.split(separator,1)[1] if separator in affiliation else affiliation
    separator = ' and '
    affiliation= affiliation.split(separator,1)[0] if separator in affiliation else affiliation
    return affiliation

def get_coauthors(name: str) -> Dict[str, str]:
    search_query = scholarly.search_author(name)
    author_dict = next(search_query)
    author = scholarly.fill(author_dict)
    coauthors = {}
    for coauthor in tqdm(author['coauthors'], desc="Fetching coauthors"):
        coauthor_dict = next(scholarly.search_author(coauthor['name']))
        coauthor = scholarly.fill(coauthor_dict)
        affiliation = clean_affiliation(coauthor['affiliation'])  # cleans affiliation if it has a comma
        coauthors[coauthor['name']] = affiliation
    return coauthors

def fetch_location(university: str) -> Dict[str, float]:
    """Fetches the latitude and longitude of a university using geopy."""
    geolocator = Nominatim(user_agent="world_academic_collab")
    location = geolocator.geocode(university)
    if not location: 
        print("[WARN] Did not find " + str(university) + ". Excluding connection from plot.")
        return {'lat': 0, 'lng': 0}
    else: return {'lat': location.latitude, 'lng': location.longitude}

def generate_kml_file(name: str, university: str, coauthors: Dict[str, str]):
    """Generates a KML file with the locations of authors and their connections."""
    # Fetch location of main author's university
    location = fetch_location(university)
    if location['lng'] == 0 or location['lat'] == 0:
        print("Could not find the resercher's location.")
        print("Terminating the program...") 
        return None

    # Create KML document
    kml_doc = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = etree.SubElement(kml_doc, 'Document')

    # Add author's placemark
    author_placemark = etree.SubElement(document, 'Placemark')
    author_name = etree.SubElement(author_placemark, 'name')
    author_name.text = name
    author_description = etree.SubElement(author_placemark, 'description')
    author_description.text = f'{name} at {university}'
    author_point = etree.SubElement(author_placemark, 'Point')
    author_coordinates = etree.SubElement(author_point, 'coordinates')
    author_coordinates.text = f"{location['lng']},{location['lat']},0"

    # Add co-authors' placemarks and connections
    folder = etree.SubElement(document, 'Folder')
    folder_name = etree.SubElement(folder, 'name')
    folder_name.text = 'Co-Authors (according to Google Scholar)'
    for coauthor, coauthor_university in tqdm(coauthors.items(), desc="Drawing connections"):
        coauthor_location = fetch_location(coauthor_university) # fetch actual location
        if coauthor_location['lng'] == 0 or coauthor_location['lat'] == 0: continue

        coauthor_placemark = etree.SubElement(folder, 'Placemark')
        coauthor_name = etree.SubElement(coauthor_placemark, 'name')
        coauthor_name.text = coauthor
        coauthor_description = etree.SubElement(coauthor_placemark, 'description')
        coauthor_description.text = f"{coauthor} at {coauthor_university}"
        coauthor_point = etree.SubElement(coauthor_placemark, 'Point')
        coauthor_coordinates = etree.SubElement(coauthor_point, 'coordinates')
        coauthor_coordinates.text = f"{coauthor_location['lng']},{coauthor_location['lat']},0"
        line_string = etree.SubElement(coauthor_placemark, 'LineString')
        line_coordinates = etree.SubElement(line_string, 'coordinates')
        line_coordinates.text = f"{location['lng']},{location['lat']},0 {coauthor_location['lng']},{coauthor_location['lat']},0"

    # Write KML file
    with open(f'{name}_coauthors.kml', 'wb') as kml_file:
        kml_file.write(etree.tostring(kml_doc, pretty_print=True))

if len(sys.argv) != 3: 
    print("Enter the researcher's complete and affiliation as arguments. Example: \"Paulo Freire\" \"Universidade Federal de Pernambuco\"")
    print("Terminating program...")

name = sys.argv[1]
university = sys.argv[2]
coauthors = get_coauthors(name)
generate_kml_file(name, university, coauthors)
