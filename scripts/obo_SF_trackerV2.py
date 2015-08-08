#### code to pull old 7 digit sourceforge trackers and hopefully replace them (or add)
## new git trackers

import requests
from bs4 import BeautifulSoup
import csv

################################
"""
This function gets passed a url, and sends a request to the server at that url
then the module 'beautifulsoup' finds all tables in the HTML with a "class" of "ticket-list"
this happens to only be one single table in our case, and there is only one result in the table
the result is the number of the git tracker, it is a link to that tracker, so then this 
function puts that link into the "links" object.  It then returns the text of that link. (not the actual link)
"""
def webscrape(url):
    r= requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    tables = soup.find_all("table", {"class": "ticket-list"})
    for table in tables:
        links = table.tbody.a
        return links.text
        
################################
"""
this creates a list, and iterates through the .obo file, pulls out the 7-digit SF xref,
and puts them all into a list 'SFtrack'
"""

# this specifies which ontology to look for these xrefs (must be .OBO format)
name = "/Users/austinmeier/Documents/jaiswal/git/plant-ontology/plant-ontology.obo"

OBO = open(name)

SFtrack=[]

### Loop to pull out all the OBO_SF_PO numbers, put them in a list "SFtrack"

for line in OBO:
  
    if not line.startswith('xref: OBO_SF_PO:'):
        continue
    else:
        #the line contains a new line character '\n' that gets pulled with the tracker number if not stripped()
        line=line.strip()
        SFxref= line.split(':')
        
        #the line contains 2 colons, and must be split.(':'), this leaves a list of strings, and we want the 3rd string, AKA [2]
        SFtrack.append(SFxref[2])
       
"""  
loop through the previously generated list "SFtrack", add the OBO_SF_PO number to the end of the url
execute the function webscrape() on that URL that is unique for each SF tracker
webscrape returns the git tracker, and this loop creates a dictionary (lookup{}) with SF:git trackers       
""" 

lookup ={}

for SF in SFtrack:
    
    url = "https://sourceforge.net/p/obo/plant-ontology-po-term-requests/search/?q=import_id%3A" +SF
    git=webscrape(url)
    
    lookup.update({SF:git})
    

"""
now export the dictionary to a CSV
note: the search on sourceforge didn't return any results for a few, and lol had to manually add the remainder
"""
writer = csv.writer(open('obo_SF_trackerV2.csv', 'wb'))
for key, value in lookup.items():
   writer.writerow([key, value])


