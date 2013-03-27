#!/usr/bin/env python

import re
import sys
import os
import csv
import argparse

def del_short_contig( strfileIn, strfileOut ):
	
	try:
		fileIn = open( strfileIn, "r" )
	except IOError:
		print "Cannot open IMG genome file."
	try:
		fileOut = open( strfileOut, "w" )
	except IOError:
		print "Cannot access output checked file."
		
	dline = 0
	dhead = 0
	dshort = 0
	dseqs = 0
	aastrline_cache = []
		
	csv_fasta_in = csv.reader( fileIn, csv.excel_tab )
	csv_fasta_out = csv.writer( fileOut, csv.excel_tab )

	for astrLine in csv_fasta_in:
		dline += 1
		if ( astrLine and re.search( r'^>', astrLine[0] ) ):
			dseqs += 1
			if dhead == 0:
				dhead = dline
			else:
				if dline - dhead - 2 >= 15:
					csv_fasta_out.writerows( aastrLine_cache )
				else:
					dshort += 1
				dhead = dline
			aastrLine_cache = [astrLine]
		else:
			aastrLine_cache += [astrLine]
	if dline - dhead - 2 >= 15:
		csv_fasta_out.writerows( aastrLine_cache )
	else:
		dshort += 1
	if not dshort:
		os.remove( strfileOut )
	return [dshort, dseqs]

def _main():

	#needed input: input files from the converted step(call it input_ref). Path to the raw genomes(rawGenome_path), path to the checked genome(checkedGenome_path)
	#input_ref should be the full path for the reference file
	#Use argparser.
	parser = argparse.ArgumentParser(description='Check genomes files and filtered out too short contigs. No short contig means creating symlink to the raw file. Filtered genome will be placed in the path users can specify.')
	parser.add_argument('-i',dest='input_ref',required=True)
	parser.add_argument('-g',dest='rawGenome_path',required=True)
	parser.add_argument('-o',dest='checkedGenome_path',required=True)

	args = parser.parse_args()	
	
	rawGenome_path = args.rawGenome_path
	checkedGenome_path = args.checkedGenome_path

	if rawGenome_path[-1]!='/':
		rawGenome_path += '/'
	if checkedGenome_path[-1]!='/':
		checkedGenome_path += '/'
	if not os.path.exists( checkedGenome_path ):
		os.makedirs( checkedGenome_path )

	try:
		refFile = open( args.input_ref, "r" )
	except IOError:
		print "Cannot open input converted abundance file!"

	csv_ref_in = csv.reader( refFile, csv.excel_tab )	
	
	print "IMG Taxon ID\t# Total Contigs\t# Short Contigs"

	for astrLine in csv_ref_in:
		
		strinput_Genome = rawGenome_path + astrLine[0]
		stroutput_Genome = checkedGenome_path + astrLine[0]
		if os.path.exists( stroutput_Genome ):
			os.remove( stroutput_Genome )

		dShort, dSeqs = del_short_contig( strinput_Genome, stroutput_Genome )
		if dShort == 0:
			os.symlink( strinput_Genome, stroutput_Genome )
		print astrLine[0] + "\t" + str(dSeqs) + "\t" + str(dShort)
	
if __name__ == "__main__":
	_main()
