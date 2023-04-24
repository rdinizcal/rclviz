from typing import Dict
from tqdm import tqdm
from scholarly import scholarly

def clean_affiliation(affiliation: str) -> str:
    possible_separators = [',', ' at ', ' @ ', ' - ', ' and ']
    for separator in possible_separators:
        if separator in affiliation:
            parts = affiliation.split(separator)
            # look for a part that has a common university suffix
            for part in parts:
                part = part.strip()
                if part.endswith('University') or part.endswith('University of Technology') or \
                        part.endswith('Institute of Technology') or part.endswith('College') or \
                        part.endswith('Research Center') or part.endswith('Laboratory') or \
                        part.endswith('Institute') or part.endswith('Foundation'):
                    return part
            # if no part has a common university suffix, return the last one
            return parts[-1].strip()
    # if no separator is found, try splitting using "at" separator
    parts = affiliation.split(' at ')
    if len(parts) > 1:
        return parts[1].strip()
    # if still no separator is found, return the original string
    return affiliation.strip()

def get_coauthors(name: str) -> Dict[str, str]:
    try:
        search_query = scholarly.search_author(name)
        author_dict = next(search_query)
        author = scholarly.fill(author_dict)
        coauthors = {}
        for coauthor in tqdm(author['coauthors'], desc="Fetching coauthors"):
            try:
                coauthor_dict = next(scholarly.search_author(coauthor['name']))
                coauthor = scholarly.fill(coauthor_dict)
                affiliation = clean_affiliation(coauthor['affiliation'])  # cleans affiliation if it has a comma
                coauthors[coauthor['name']] = affiliation
            except StopIteration:
                print(f"No results found for {coauthor['name']}")
            except Exception as e:
                print(f"Error occurred while fetching data for {coauthor['name']}: {str(e)}")
        return coauthors
    except StopIteration:
        print(f"No results found for {name}")
    except Exception as e:
        print(f"Error occurred while fetching data for {name}: {str(e)}")
