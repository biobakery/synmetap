#!/usr/bin/env python

import re
import sys
import os
import csv
import argparse
import os, errno

def del_short_contig( fileIn, fileOut ):
	dline = 0
	dhead = 0
	dshort = 0
	astrline_cache = []
		
	csv_fasta_in = csv.reader( fileIn, csv.excel_tab )
	csv_fasta_out = csv.reader( fileOut, csv.excel_tab )

	for astrLine in csv_fasta_in:
		dline += 1
		if re.search( r'^>', astrLine[0] ):
			if dhead == 0:
				dhead = dline
			else:
				if dline - dhead - 2 >= 15:
					csv_fasta_out.writerows( astrLine_cache )
				else:
					dshort += 1
				dhead = dline
			astrline_cache = astrLine
	if dline - dhead - 2 >= 15:
		csv_fasta_out.writerows( astrLine_cache )
	else:
		dshort += 1

	return dshort
"""
def contig_pick( hashIndex ):

	#start line number for short contig. 1 based
	aRetS = []
	#end line number for short contig. 1 based
	aRetE = []

	for key in hashIndex.keys():
		aRetS += [key]
	aRetS = sorted(aRetS)
	aRetE = [hashIndex[key] for key in aRetS]
	return [aRetS, aRetE]

def contig_copy( genome_in, genome_out, aaDel ):
	
	#aaDel is [aRetS, aRetE]
	aStart = aaDel[0]
	aEnd = aaDel[1]

	line_num = 0
	try:
		genome_file_in = open( genome_in, "r" )
	except IOError:
		print "Cannot open input genome fasta file."
	try:
		genome_file_out = open( genome_out, "w" )
	except IOError:
		print "Cannot access output genome fasta file."

	for line in genome_file_in:
		line_num += 1
		line_pointer = bisect.bisect( aStart, line_num ) - 1 if line_num<= aStart[-1] else len( aStart ) - 1
		if line_pointer < 0 or line_num > aEnd[line_pointer]:
			genome_file_out.write( line )
	
	genome_file_in.close()
	genome_file_out.close()
"""
			
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

	for astrLine in csv_ref_in:
		
		strinput_Genome = rawGenome_path + astrLine[0]
		stroutput_Genome = checkedGenome_path + astrLine[0]

		dShort = del_short_contig( open( strinput_Genome, "r" ), open( stroutput_Genome, "w"  ) )
		if dShort == 0:
			try:
				os.symlink( strinput_Genome, stroutput_Genome )
			except OSError, e:
				if e.errno == errno.EEXIST:
					os.remove( stroutput_Genome )
					os.symlink( strinput_Genome, stroutput_Genome )
	
if __name__ == "__main__":
	_main()
