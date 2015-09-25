# The deldupe() function performs these operations:  
# 1. Removes any line in the assoc file that has an exact duplicate (includes all 16 columns in step 1). 
# 2. Identifies any lines in the association file that has relative duplicates (relative duplicates are rows where everything in columns 1 through 15 are exactly the same, 
#   but the row has different values in column 16.) 
# 3. Removes any relative duplicate rows that contain "-" in column 16. 
# 4. performs a check to see if the expected number of rows are removed.

############################################################################################################
# usage: deldupe("name_of_association_file_to_be_fixed")                                                  #
# enter the name using quotes, as seen above.                                                             #
# output prints how many exact dupes, and relative dupes were fixed.                                      #  
# the fixed_assoc file will be written to the working directory with the prefix "fixed_"                  #
############################################################################################################




#function delete dupes
deldupe<-function(assocfilename){
  
  #specify the name of the output file
  newfilename<-paste("fixed_",assocfilename, sep="")
  
  #select association file to be fixed
  #assocfile_to_be_fixed<-read.csv(file.choose(),header=FALSE,sep = "\t")
  
  assocfile_to_be_fixed<-read.csv(assocfilename,header=FALSE,sep = "\t")
  
  #remove any 'exact duplicates'
  df_no_exactdupes.16 <- unique(assocfile_to_be_fixed)
  
  #make new data frame without column 16
  df_no_exactdupes.15<-df_no_exactdupes.16[,-16]
  #df_no_exactdupes.15$V16=NULL
  
  #Identify 'relative duplicates', put those rows into a vector.
  relative_dupes<-which(duplicated(df_no_exactdupes.15) | duplicated(df_no_exactdupes.15[nrow(df_no_exactdupes.15):1, ])[nrow(df_no_exactdupes.15):1])
  
  #remove relative dupe rows that have "-" in column16 of the original data
  todelete<-NULL
  for (rows in relative_dupes){
    if(df_no_exactdupes.16[rows,16]=='-'){
      todelete<-append(todelete,rows)
    }
  }
  
  #create new dataframe without the dupes
  if(length(todelete)==0) {
    cat("No relative dupes were found\n", (nrow(assocfile_to_be_fixed)-nrow(df_no_exactdupes.16))," exact dupes were removed")
    write.table(df_no_exactdupes.16, file=newfilename, quote=FALSE, sep='\t', row.names=FALSE,col.names = FALSE)
    stop("Done.")
    #return(df_no_exactdupes.16)
    }
  
  fixed_assoc<-df_no_exactdupes.16[- todelete,]
  
  #create 15 col df with no exact dupes, and no relative dupes.  Perform a check to see if all relative dupes have one with '-' in col_16, and one with anything else in col_16
  #no rows with information in col_16 will be removed.
  df_no_reldupes.15<-unique(df_no_exactdupes.15)
  if (nrow(fixed_assoc)==nrow(df_no_reldupes.15)){
    cat(" It's all good.\n",nrow(assocfile_to_be_fixed)-nrow(df_no_exactdupes.16)," exact dupes were removed\n",nrow(df_no_exactdupes.16)-nrow(fixed_assoc), " relative dupes were removed")}
  else if(nrow(fixed_assoc)<nrow(df_no_reldupes.15)){cat("something isn't right. \nThere are ",nrow(df_no_reldupes.15)-nrow(fixed_assoc)," too few rows.")}
  else if(nrow(fixed_assoc)>nrow(df_no_reldupes.15)){cat("something isn't right. \nThere are ",nrow(fixed_assoc)-nrow(df_no_reldupes.15)," too many rows.")}
  
  #return (fixed_assoc)

  write.table(fixed_assoc, file=newfilename, quote=FALSE, sep='\t', row.names=FALSE,col.names = FALSE)
  }
