import pytest
from unittest.mock import MagicMock
from rclviz.scholar import clean_affiliation, get_coauthors
from scholarly import scholarly

def test_clean_affiliation():
    # test affiliation with comma separator
    assert clean_affiliation('Department of Computer Science, University of Bristol') == 'University of Bristol'
    # test affiliation with "at" separator
    assert clean_affiliation('Department of Computer Science at University of Bristol') == 'University of Bristol'
    # test affiliation with "@" separator
    assert clean_affiliation('Department of Computer Science @ University of Bristol') == 'University of Bristol'
    # test affiliation with "-" separator
    assert clean_affiliation('Department of Computer Science - University of Bristol') == 'University of Bristol'
    ## test affiliation with multiple possible separators
    # assert clean_affiliation('Department of Computer Science, University of Bristol - Research Center') == 'University of Bristol'
    # test affiliation with multiple parts, but none with a university suffix
    assert clean_affiliation('Department of Computer Science, Research Center') == 'Research Center'
    # test affiliation with no separator
    assert clean_affiliation('University of Bristol') == 'University of Bristol'

def test_get_coauthors_stop_iteration():
    # Test case 2: author not found
    with pytest.raises(StopIteration):
        get_coauthors("Random Name")

def test_get_coauthors_exceptions():
    # Test case 3: invalid author name
    with pytest.raises(Exception):
        get_coauthors("")
