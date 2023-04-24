import sys
from rclviz import kml
from rclviz.scholarly import get_coauthors

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide your name and your university as command line arguments.')
        print('Example usage: python main.py "John Doe" "University of California, Los Angeles"')
        sys.exit()

    name = sys.argv[1]
    university = sys.argv[2]

    # Validate user input
    if not name.strip() or not university.strip():
        print('Please provide valid non-empty strings for your name and your university.')
        sys.exit()

    # Get coauthors
    coauthors = get_coauthors(name)

    if not coauthors:
        print('Could not find any coauthors for the given name.')
        sys.exit()

    # Generate KML file
    kml.generate_kml_file(name, university, coauthors)
