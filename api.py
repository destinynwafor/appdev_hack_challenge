from bs4 import BeautifulSoup
from urllib.request import urlopen

BASE_URL = "https://events.cornell.edu"

# Retrieves the link associated with a club on the Cornell 
# Events website. 
def get_club_links(section_url):
    html = urlopen(section_url).read()
    soup = BeautifulSoup(html, "lxml")
    place_group = soup.find("div", "place_group")
    club_links = [BASE_URL + div.a["href"] for div in place_group.findAll("div")]
    return club_links

# Retrieves a list of events associated with a club from 
# the Cornell Events website. 
def get_club_events(club_url):
    html = urlopen(club_url).read()
    soup = BeautifulSoup(html, "lxml")
    events = [a.string for a in soup.findAll("a", "summary")]
    return {"events": events}


