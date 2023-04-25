import sys
from kml import generate_kml_file
from location import fetch_location, LocationNotFoundError
from scholar import get_coauthors

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide your name and your university as command line arguments.')
        print('Example usage: python main.py "Paulo Freire" "Universidade de Pernambuco"')
        sys.exit()

    name = sys.argv[1]
    university = sys.argv[2]

    # Validate user input
    if not name.strip() or not university.strip():
        print('Please provide valid non-empty strings for your name and your university.')
        sys.exit()

    try:
        fetch_location(university) # Get location
        coauthors = get_coauthors(name) # Get coauthors
    except LocationNotFoundError as e:
        print(f"Error: {str(e)}")
        sys.exit()
    except StopIteration as e:
        print(f"Error: {str(e)}")
        sys.exit()
    
    generate_kml_file(name, university, coauthors) # Generate KML file
