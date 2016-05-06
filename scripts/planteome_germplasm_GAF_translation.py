#OG_datafile.csv must be in the same format as the file contained in this repo
#Trait_map.csv must also be in the same format as the sample file contained in this repo

#########################################################################
#                       imports
#########################################################################
import time

import sys

import os


usage_statement = "usage: python2.7 planteome_germplasm_GAF_translation.py <OG_datafile.csv> <Trait_map.csv> <taxonID> <DatabaseID> <path of output directory>"

#check the number of arguments
if len(sys.argv) !=6:
	print("Error: incorrect number of arguments")
	print(usage_statement)
	quit()

OG_datafile = sys.argv[1]
traitmap = sys.argv[2]
taxonID = "NCBITaxon:" + str(sys.argv[3])
database = sys.argv[4]
#outdir
if sys.argv[5].endswith('/'):
	outdir = sys.argv[5]
else: outdir = sys.argv[5]+'/'
#check if the outdirectory specified exists, if not, make it.
if not os.path.exists(sys.argv[5]):
	os.makedirs(sys.argv[5])





evidencecode = "EXP"
outfile = outdir + database + ".assoc"
assigned_by = "austin_meier"



#########################################################################
#                 Create translation dictionary
#########################################################################
traitdict = {}
with open(traitmap,'r') as x:
    for traitname in x:
        #print traitname.strip()
        line1 = traitname.strip('\n')
        line = line1.split(',')
        traitdict[line[0]] = line[1]

#print traitdict





#########################################################################
#                        Get trait names
#########################################################################
with open(OG_datafile, 'r') as f:
    headers = f.readline().strip().split(",")

traitcolumns = {}     # a dictionary of TO IDs, and their index numbers
for item in headers:
    if item in traitdict:
        traitcolumns[traitdict[item]] = (headers.index(item))
#########################################################################
#                        one run, one GAF line
#########################################################################

def gafline(phenotype_object,TO_num, outfile):

    #check to make sure each column call function returns a value, if any return False, it will not write a GAF line
    if col1() and col2(phenotype_object) and col3(phenotype_object)  and col5(TO_num) and col6(phenotype_object) and col7() \
             and col9() and col12() and col13(phenotype_object) and col14() and col15 and col16(phenotype_object,TO_num):

        outfile.write(
            #print(
            col1()+"\t"+
            col2(phenotype_object)+"\t"+
            col3(phenotype_object)+"\t"+
            col4()+"\t"+
            col5(TO_num)+"\t"+
            col6(phenotype_object)+"\t"+
            col7()+"\t"+
            col8(phenotype_object)+"\t"+
            col9()+"\t"+
            col10(phenotype_object)+"\t"+
            col11(phenotype_object)+"\t"+
            col12()+"\t"+
            col13(phenotype_object)+"\t"+
            col14()+"\t"+
            col15()+"\t"+
            col16(phenotype_object,TO_num)+"\t"+
            "\n")



# required
def col1():
    return database

#required
def col2(phenotype_object):
    return phenotype_object[0]

#required
def col3(phenotype_object):
    #check if the accession has a name
    if phenotype_object[1] != "":
        #return the germplasm name (unless here is a germplasm symbol)
        #Name= str(phenotype_object[1]).split('::') #not sure if I will need to convert the name to a string or edit it
        return phenotype_object[1]
    else:
        print('record for\n', phenotype_object,"\nwill not be included.  It is missing a name")
        return False

#not required
def col4():
    return ""

#required
def col5(TO_num):
    #return the TO:xxxxxxxx or CO:xxxxxxxx
    return TO_num

#required
def col6(phenotype_object):
    #check to see if there is a reference in OG, if no ref, use the database name
    if phenotype_object[2] != "":
        return phenotype_object[2]
    else:
        return database

#required
def col7():
    #return the evidence code
    return evidencecode

#not required
def col8(phenotype_object):
    #check if the OG contains a country
    if phenotype_object[3] != "":
        #return the relationship "from_country" and the country of origin
        country_origin = phenotype_object[3]
        column8 = "from_country(%s)"%(country_origin)
        return column8.replace(" ","_")
    else:
        return ""



#required
def col9():
    #return aspect
    return "T"

#not required
def col10(phenotype_object):

    #check if the accession has a name
    if phenotype_object[1] != "":
        #return the germplasm name (unless there is a germplasm symbol)
        return phenotype_object[1]
    else:
        print('record for\n', phenotype_object,"\nwill not be included.  It is missing a name")
        return False
        #this name is not required, so it won't return anything.  However, in this case, if there isn't a name,
        #it will error out on col3(), so it doesn't really matter



#not required
def col11(phenotype_object):
    #get synonyms
    #in this case, there is no synonyms... Can't think of an elegant way to add them, so if someone has synonyms we can add them here
    if 'name' in phenotype_object:
        #Name= str(phenotype_object['name']).split('::')
        return "this should never get printed"
    else:
        return ""


#required
def col12():
    #return object type
    return "germplasm"

#required
def col13(phenotype_object):
    #taxon
    return taxonID


#required
def col14():
    #return date
    date=str(time.strftime('%m%d%Y'))
    return date

#not required
def col15():
    return assigned_by


#not required for GAF, but required for germplasm
def col16(phenotype_object,TO_num):
    phenotype_value= phenotype_object[traitcolumns[TO_num]]
    phenotypename = traitdict.keys()[traitdict.values().index(TO_num)].replace(" ","_")
    return "has_phenotype_score(" + phenotypename + "=" + phenotype_value +")"


    #return the variable (if it exists)
    #return the method, if it exists
    #return the evaluation location (evaluation_location(x))


#########################################################################
#                           MAIN
#########################################################################

def main():
    OUTWRITE = open(outfile, "w")
    OUTWRITE.write("!gaf-version: 2.0\n")
    #print traitcolumns
    with open(OG_datafile,'r') as og:
        for accession in og:
            if not accession.startswith("#"):
                accessionlist = accession.strip().split(',')
                #print accession
                #print accessionlist
                for TO_num in traitcolumns:
                    gafline(accessionlist,TO_num, OUTWRITE)
    OUTWRITE.close()


#########################################################################
#                    run actual code here
#########################################################################

main()