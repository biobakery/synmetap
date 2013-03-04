#!/usr/bin/env python

import re
import sys
import os
import bisect
import argparse

def short_header_line( fileIn ):
	line_index = 0
	hashIndex = {}
	head = 0
	for strLine in fileIn:
		line_index += 1
		if re.search( r'^>', strLine ):
			if head == 0:
				head = line_index
			else:
				if line_index - head - 2 < 15:
					hashIndex[head] = line_index - 1
				head = line_index
	if line_index - head - 2 < 15:
		hashIndex[head] = line_index
	return hashIndex

def contig_pick( hashIndex ):
	
	aRetS = []
	aRetE = []
	for key in hashIndex.keys():
		aRetS += [key]
	aRetS = sorted(aRetS)
	aRetE = [hashIndex[key] for key in aRetS]
	return [aRetS, aRetE]

def contig_copy( genome_in, genome_out, aaDel ):
	
	aStart = aaDel[0]
	aEnd = aaDel[1]

	line_num = 0
	genome_file_in = open( genome_in, "r" )
	genome_file_out = open( genome_out, "w" )

	#print "copy called!"
	#print aaDel
	for line in genome_file_in:
		line_num += 1
		line_pointer = bisect.bisect( aStart, line_num ) - 1 if line_num<= aStart[-1] else len( aStart ) - 1
		#print line_pointer
		#print line_num
		#print aEnd[line_pointer]
		if line_pointer < 0 or line_num > aEnd[line_pointer]:
			#print line
			genome_file_out.write( line )
	
	genome_file_in.close()
	genome_file_out.close()
			
def main():
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

	refFile = open( args.input_ref, "r" )
	for line in refFile:
		aline = line.strip().split("\t")
		hashLine = short_header_line( open( rawGenome_path+aline[0], "r" ) )
		aaDel = contig_pick( hashLine )
		input_Genome = rawGenome_path + aline[0]
		output_Genome = checkedGenome_path + aline[0]
		
		print output_Genome
		print input_Genome	
		if aaDel == [[],[]]:
			if not os.path.exists( output_Genome ):
				os.symlink( input_Genome, output_Genome )
		else:
			contig_copy( input_Genome, output_Genome, aaDel )
	
if __name__ == "__main__":
	main()
