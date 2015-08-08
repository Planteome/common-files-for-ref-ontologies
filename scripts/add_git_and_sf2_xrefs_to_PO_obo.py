
"""
This is a script that iterates through an .obo file, finds specific xrefs, and adds corresponding
xrefs using a 'decoderring' csv file that it turns into a dictionary to return the correct tracker number
"""



import fileinput
import csv
import sys


#### read in the csv decoder ring
reader = csv.reader(open('OBO_SF_PO_to_GIT.csv', 'rb'))
decoderring = dict(x for x in reader)

 ###################
"""
This function is passed OBO_SF_PO xrefs number and prints the corresponding PO_GIT xref
"""
def sf2git(sf):
    git = decoderring[sf]
    gitxref= 'xref: PO_GIT:' +git
    print gitxref

  ###################
"""
This function is passed
"""
def sf1_sf2(sf):
    git = decoderring[sf]
    sf2xref= 'xref: OBO_SF2_PO:' +git
    print sf2xref

  ###################
  
def sf2_to_git(sf):
    gitxref= 'xref: PO_GIT:' +sf
    print gitxref

  ###################

        #begin
  
  ######################
"""  
this section finds SF2 trackers and adds GIT trackers (xrefs)
You have to find all the loner SF2 xrefs first, so they don't get caught by the second iteration
when you are adding new SF2 xrefs.
The first 'if' looks for rare cases where there are two consecutive lines with the same xref
it pretty much goes through every line, if the line starts with "xref..." it turns on the variable 'processing_foo1s'
then prints the line.  If the variable is "True" it executes the above functions, printing the corresponding xrefs
then turns the boolean variable back to 'False'. continuing to print each line.
it essentially reads in the file, and prints it back out, line by line.
"""

processing_foo1s = False
sf=None

for line in fileinput.input('plant-ontology.obo', inplace=1):

    if line.startswith('xref: OBO_SF2_PO:') and processing_foo1s:
        sf2_to_git(sf)
        line1=line.strip()
        sftrack1=line1.split(':')
        sf =sftrack1[2]
        processing_foo1s = True
    
    elif line.startswith('xref: OBO_SF2_PO:'):
        line1=line.strip()
        sftrack1=line1.split(':')
        sf =sftrack1[2]
        processing_foo1s = True
        
    else:
        if processing_foo1s:
            #print '\n'
            sf2_to_git(sf)
        processing_foo1s = False
        
    print line,
  
  #######################
  """
  This does the exact same thing as above, but looks for OBO_SF_PO xrefs not SF2.  It then adds
  SF2 and GIT trackers.
"""
#def SF1_to_GIT_and_SF2():

processing_foo1s = False
sf=None

for line in fileinput.input('plant-ontology.obo', inplace=1):

    if line.startswith('xref: OBO_SF_PO:') and processing_foo1s:
        sf2git(sf)
        sf1_sf2(sf)
        line1=line.strip()
        sftrack1=line1.split(':')
        sf =sftrack1[2]
        processing_foo1s = True
    
    elif line.startswith('xref: OBO_SF_PO:'):
        line1=line.strip()
        sftrack1=line1.split(':')
        sf =sftrack1[2]
        processing_foo1s = True
        
    else:
        if processing_foo1s:
            sf2git(sf)
            sf1_sf2(sf)
        processing_foo1s = False
        
    print line,

  #######################
 
    