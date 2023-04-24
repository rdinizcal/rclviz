from typing import Dict
from tqdm import tqdm
from scholarly import scholarly
from location import fetch_location

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
