This script is meant to transform an original data file into GAF2 annotation file.
use the -h option to list all of the other options.

columns 1-4 must be in the format specified:

#ID, name, reference, origin_country

after the first 4, columns can be in any order.  They must have headers.  These headers are listed in the traitmap.csv file that you submit.
examples of original datafiles and traitmaps can be found in this folder (sample_OG_data.tsv - tab separated, and sample_OG_data.csv - comma separated)
traitmaps must be comma separated. In the form:
header,TO:xxxxxx
the evidence code is optional, and the default is EXP.  This can change on a trait by trait basis.
