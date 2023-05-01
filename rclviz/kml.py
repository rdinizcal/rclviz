from typing import Dict
from lxml import etree
from tqdm import tqdm
from scholar import get_coauthors
from location import fetch_location, LocationNotFoundError

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
    # coauthor_folder = etree.SubElement(author_placemark, 'Folder')
    for coauthor, coauthor_affiliation in tqdm(coauthors.items(), desc="Connecting "+name+ " to their co-authors"):
        try:
            coauthor_location = fetch_location(coauthor_affiliation)
        except LocationNotFoundError as e:
            print(f"Error: {str(e)}")
            continue # skip this university and move on to the next one
        
        # Add connection between author and co-author
        line_string = etree.SubElement(document, 'Placemark')
        line_string_name = etree.SubElement(line_string, 'name')
        line_string_name.text = f'{name} - {coauthor}'
        line_string_description = etree.SubElement(line_string, 'description')
        line_string_description.text = f'{name} and {coauthor} have collaborated on a project.'
        line_string_style = etree.SubElement(line_string, 'Style')
        line_string_line_style = etree.SubElement(line_string_style, 'LineStyle')
        line_string_line_style_width = etree.SubElement(line_string_line_style, 'width')
        line_string_line_style_width.text = '1'
        line_string_line_style_color = etree.SubElement(line_string_line_style, 'color')
        line_string_line_style_color.text = '000000'
        line_string_coordinates = etree.SubElement(line_string, 'LineString')
        line_string_coordinates_tessellate = etree.SubElement(line_string_coordinates, 'tessellate')
        line_string_coordinates_tessellate.text = '1'
        line_string_coordinates_altitude_mode = etree.SubElement(line_string_coordinates, 'altitudeMode')
        line_string_coordinates_altitude_mode.text = 'clampToGround'
        line_string_coordinates_coordinates = etree.SubElement(line_string_coordinates, 'coordinates')
        line_string_coordinates_coordinates.text = f"{location['lng']},{location['lat']},0 {coauthor_location['lng']},{coauthor_location['lat']},0"

    # Write KML document to file
    with open(f'{name}.kml', 'wb') as kml_file:
        kml_file.write(etree.tostring(kml_doc, pretty_print=True))

    print(f'KML file generated for {name} with co-authors.')
