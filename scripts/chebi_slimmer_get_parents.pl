#!/usr/bin/perl

###############################################################
#  Justin Elser  (elserj@science.oregonstate.edu)             #
#		Parses the assoc files for any taxon ids              #
#		used in planteome assoc files.  Uses that to          #
#		get all parent ids.  Once the terms with parents are  #
#		are generated, use the following to create OBO file:  #
#		./robot extract --input ../temp/chebi.obo --method STAR --term-file ../temp/chebi_terms_with_parents_4.lst --output ../temp/chebi_filtered_5.obo
#		or similar											  #
#                                                             #
###############################################################


use strict;
use warnings;

# check for arguments and explain usage
if ($#ARGV !=2) {
	print "usage: chebi_slimmer_get_parents.pl input_file obo_file output_file\n";
	exit;
}

my $input_file = $ARGV[0];
my $obo_file = $ARGV[1];
my $output_file = $ARGV[2];

my %chebi_hash;

# get the relevant chebi ids
open(INFILE, "$input_file") || die "Error: file '$input_file' can not be opened\n";
while(<INFILE>){
	my $line = $_;
	chomp $line;
	
	if($line =~ /(CHEBI:\d+)/) {
			my $term = $1;
			if(!defined($chebi_hash{$term})){
					$chebi_hash{$term} = $term;
			}
	}
}
close(INFILE);



# Attempt to get all parent ids as well and add them to the list
my $new_id = 1;
my $keep_section = 0;
my $counter = 0;
while($new_id == 1) {
		$new_id = 0;
		$counter++;
		open(OBOFILE, "$obo_file") || die "Error: file '$obo_file' can not be opened\n";
		my $line_number = 0;
		my $term;
		while (<OBOFILE>){
				my $line = $_;
				chomp $line;
				$line_number++;
				
				if($line =~ /^id:\s(CHEBI:\d+)/) {
					$term = $1;
					if(defined($chebi_hash{$term})) {
							$keep_section = 1;
							next;
					}
				}
				
				if($keep_section == 1) {
						#if($line =~ /^is_a:\s(CHEBI:\d+)/ or $line =~ /has_role\s(CHEBI:\d+)/) {
						if($line =~ /^is_a:\s(CHEBI:\d+)/) {
								my $chebi = $1;
								if(!defined($chebi_hash{$chebi})) {
										$new_id = 1;
										print "Found a new id! $chebi\n";
										$chebi_hash{$chebi} = $chebi;
								}
						}
				}elsif($line =~ /has_role\s(CHEBI:\d+)/) {
						if(defined($chebi_hash{$1})) {
								if(!defined($chebi_hash{$term})) {
										$new_id = 1;
										$chebi_hash{$term} = $term;
								}
						}
				}
				
				if($line =~ /^$/) {
				$keep_section = 0;
				}
		}
		close(OBOFILE);
		print "Counter = $counter\n";
		
}



# Print out a list of all chebi ids

open(OUTFILE, ">$output_file");
foreach my $key (keys %chebi_hash) {
		print OUTFILE "$key\n";
}
close(OUTFILE);
