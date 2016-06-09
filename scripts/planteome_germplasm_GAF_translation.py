#!/usr/bin/python

#OG_datafile.csv must be in the same format as the file contained in this repo
#Trait_map.csv must also be in the same format as the sample file contained in this repo
#test config:  "/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/test_10line.txt" "/Users/meiera/Documents/Jaiswal/Planteome/IRRI/jeffs_trait_map.txt" "4530" "GRIMS" "/Users/meiera/Documents/Jaiswal/Planteome/IRRI/"
#########################################################################
#                       imports
#########################################################################
import time

import os

import argparse


parser = argparse.ArgumentParser(description = "Transform original germplasm data in to GAF2 formatted annotation files for display on Plantome.org")
parser.add_argument("OG_datafile", help = "This is the original data file.  Refer to template for format")
parser.add_argument("traitmap", help = "this is a file that maps the headers of the OG_datafile to their traitID in the TO")
parser.add_argument("database", help = "This is the database that holds the germplasm.")
parser.add_argument("-o","--outdir", help = "The directory you would like the GAF file written to.")
parser.add_argument("-t","--taxon", help = "The NCBI taxon ID number for the species being annotated (Default is 4530, which is Oryza sativa)")
parser.add_argument("-e","--evidence", help = "The evidence code associated with this file's annotation.  Default is EXP")
parser.add_argument("-c","--currator", help = "The person who did the curration.  Default is 'austin_meier'")
parser.add_argument("-n","--outfile", help = "Name of the output file.  Default is '<database>.assoc'")
parser.add_argument("-s","--separator", type = int, choices = [1,2], default=1, help = "the field separator for the OG datafile.  1 = CSV, 2 = TSV. Default is CSV.")

args = parser.parse_args()

# positional arguments
OG_datafile = args.OG_datafile
traitmap = args.traitmap
database = args.database
# optional arguments

# output directory
if args.outdir:
    if args.outdir.endswith('/'):
        outdir = args.outdir
    else: outdir = args.outdir + '/'
 #check if the outdirectory specified exists, if not, make it.
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
else:
    outdir = os.getcwd() + '/'

# Taxon argument
if args.taxon:
    taxonID = "NCBITaxon:" + args.taxon
else:
    taxonID = "NCBITaxon:4530"

# Evidence argument
if args.evidence:
    evidencecode = args.evidence
else:
    evidencecode = "EXP"

# assigned by:
if args.currator:
    assigned_by = args.currator
else:
    assigned_by = "austin_meier"

# output filename
if args.outfile:
    outfile = args.outfile + ".assoc"
else:
    outfile = outdir + database + ".assoc"

# OG separator/delimiter selection:
if args.separator == 2:
    delimiter = '\t'
else:
    delimiter = ','






#########################################################################
#                 Make the ULTIMATE TRAIT DICTIONARY
#########################################################################

with open(OG_datafile, 'r') as f:
    headers = f.readline().strip().split(delimiter)       #delimeter was selected at program start


traitdict = {}
with open(traitmap,'r') as x:
    for traitname in x:
        line1 = traitname.strip('\n')
        line = line1.split(',')
        traitdict[line[0]] = {'toID':line[1]}
        try:
           traitdict[line[0]]['evidence'] = line[2]
        except:
           traitdict[line[0]]['evidence'] = evidencecode
        if line[0] in headers:
            traitdict[line[0]]['colnum'] = headers.index(line[0])


def gafline(phenotype_object,trait, outfile):
    TO_num = traitdict[trait]['toID']
    trait_index = int(traitdict[trait]['colnum'])
    #check to make sure each column call function returns a value, if any return False, it will not write a GAF line
    if col1() and col2(phenotype_object) and col3(phenotype_object)  and col5(TO_num) and col6(phenotype_object) and col7(trait) \
             and col9() and col12() and col13(phenotype_object) and col14() and col15 and col16(phenotype_object,trait,trait_index):

        outfile.write(

            col1()+"\t"+
            col2(phenotype_object)+"\t"+
            col3(phenotype_object)+"\t"+
            col4()+"\t"+
            col5(TO_num)+"\t"+
            col6(phenotype_object)+"\t"+
            col7(trait)+"\t"+
            col8(phenotype_object)+"\t"+
            col9()+"\t"+
            col10(phenotype_object)+"\t"+
            col11(phenotype_object)+"\t"+
            col12()+"\t"+
            col13(phenotype_object)+"\t"+
            col14()+"\t"+
            col15()+"\t"+
            col16(phenotype_object,trait,trait_index)+"\t"+
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
        #if there is no name, I had it print the database and the accession number instead
        nameaccession = database +':' + str(phenotype_object[0])
        return nameaccession

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
def col7(trait):
    #return the evidence code
    return traitdict[trait]['evidence']

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
        #if there is no name, I had it print the database and the accession number instead
        nameaccession = database +':' + str(phenotype_object[0])
        return nameaccession


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
def col16(phenotype_object,trait,trait_index):
    phenotype_value= phenotype_object[trait_index]  #phenotype_object[traitcolumns[TO_num]]
    #phenotypename = traitdict.keys()[traitdict.values().index(TO_num)].replace(" ","_")
    if phenotype_value != "":
        return "has_phenotype_score(" + trait + "=" + phenotype_value +")"
    else:
        return False

    #return the variable (if it exists)
    #return the method, if it exists
    #return the evaluation location (evaluation_location(x))


#########################################################################
#                           MAIN
#########################################################################

def main():
    with open(outfile,"w") as OUTWRITE, open(OG_datafile,'r') as og:
        OUTWRITE.write("!gaf-version: 2.0\n")
        for accession in og:   #for every line in the original data file:
            if not accession.startswith("#"):
                accessionlist = accession.strip().split(delimiter)        #delimiter selected at program start
                for trait in traitdict:
                    gafline(accessionlist, trait ,OUTWRITE)
    print "New association file has been created: " + outfile

#########################################################################
#                    run actual code here
#########################################################################

if __name__ == "__main__":
    main()