#!/usr/bin/env python

import re
import sys
import os
import csv
import argparse

def del_short_contig( strfileIn, strfileOut, iMinLen ):
	
	try:
		fileIn = open( strfileIn, "r" )
	except IOError:
		print "Cannot open IMG genome file."
	try:
		fileOut = open( strfileOut, "w" )
	except IOError:
		print "Cannot access output checked file."
		
	ishort = 0
	iseqs = 0
	strLine_cache = ""
	fWrite = False 
		
	for strLine in fileIn:
		strLine = strLine.strip()
		if ( strLine and re.search( r'^>', strLine ) ):
			iseqs += 1
			fWrite = False
			if strLine_cache:
				ishort += 1
			strLine_cache = ( strLine + "\n" )
		elif fWrite:
			fileOut.write( strLine + "\n" )
		else:
			strLine_cache += ( strLine + "\n" )
			if len( "".join( strLine_cache.split("\n")[1:] ) ) > iMinLen:
				fileOut.write( strLine_cache )
				strLine_cache = ""
				fWrite = True
	if strLine_cache:
		ishort += 1
	
	if not ishort:
		os.remove( strfileOut )

	return [ishort, iseqs]

def _main():

	#needed input: input files from the converted step(call it input_ref). Path to the raw genomes(rawGenome_path), path to the checked genome(checkedGenome_path)
	#input_ref should be the full path for the reference file
	#Use argparser.
	parser = argparse.ArgumentParser( description = "Check genomes files and filtered out too short contigs. No short contig means creating symlink to the raw file. Filtered genome will be placed in the path users can specify." )
	parser.add_argument( "-i", metavar = "input_ref", dest = "input_ref", required = True, help = "input converted abundance files" )
	parser.add_argument( "-g", metavar = "genome_ref_path", dest = "rawGenome_path", required = True, help = "input path to IMG reference genome files" )
	parser.add_argument( "-o", metavar = "output_checked", dest = "checkedGenome_path", required = True, help = "path to output checked required genome files")
	parser.add_argument( "-l", metavar = "log_file", dest = "log", required= True, help = "output log file" )
	parser.add_argument( "-n", metavar = "min_length", dest = "imin", type = int, required = True, help = "minimal contig length" )

	args = parser.parse_args()	
	
	rawGenome_path = args.rawGenome_path
	checkedGenome_path = args.checkedGenome_path
	aastrLog = []

	#This is needed for if you build a node by a path name
	#there is no / at the end.
	#Also add robustness against different user-defined
	#reference genome path.
	if rawGenome_path[-1] != "/":
		rawGenome_path += "/"
	if checkedGenome_path[-1] != "/":
		checkedGenome_path += "/" 
	
	#This is necessary for Scons will not create
	#path if the node being built is a path.
	if not os.path.exists( checkedGenome_path ):
		os.makedirs( checkedGenome_path )

	try:
		refFile = open( args.input_ref, "r" )
	except IOError:
		print "Cannot open input converted abundance file!"

	csv_ref_in = csv.reader( refFile, csv.excel_tab )
	
	aastrLog.append( ["IMG Taxon ID", "# Total Contigs", "# Short Contigs"] )

	for astrLine in csv_ref_in:
		
		strinput_Genome = rawGenome_path + astrLine[0]
		stroutput_Genome = checkedGenome_path + astrLine[0]
		if os.path.exists( stroutput_Genome ):
			os.remove( stroutput_Genome )

		dShort, dSeqs = del_short_contig( strinput_Genome, stroutput_Genome, args.imin )
		if dShort == 0:
			os.symlink( strinput_Genome, stroutput_Genome )
		aastrLog.append( [astrLine[0], str(dSeqs), str(dShort)] )

	csv.writer( open( args.log, "w" ), csv.excel_tab ).writerows( aastrLog )
	csv.writer( sys.stdout, csv.excel_tab ).writerows( aastrLog )

if __name__ == "__main__":
	_main()
