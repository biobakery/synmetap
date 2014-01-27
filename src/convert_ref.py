#!/usr/bin/python

import argparse
import os
import sys
import csv
import re

def parse_taxon_table( table_path ):
	
	try:
		fileIn_table = open( table_path, "rU" )
	except IOError:
		sys.stderr.write( "Cannot open IMG genome files.\n" )
		raise
	
	hashTaxon = {}
	fHead = True

	for astrLine in csv.reader( fileIn_table, csv.excel_tab ):
		if fHead:
			fHead = False
			continue
		elif astrLine:
			astrInfo, strG, strSp, strSt = [[astrLine[0], astrLine[3], astrLine[2], int( astrLine[-1] )]] + [strTmp.lower() for strTmp in astrLine[12:15]]
			strG, strSp, strSt = [ " ".join( [ strWord for strWord in strInd.split( " " ) if strWord != "candidatus"] ) for strInd in [strG, strSp, strSt] ]
			#if len( strSp.split(" ") ) > 1:
				#print strSp

			tKey = ()
			for strTmp in [strG, strSp, strSt]:
				if ( not strTmp ) or ( strTmp == "unclassified" ):
					break
				else:
					tKey += (strTmp,)
					astrValue = hashTaxon.get( tKey, [] )
					#prioritize user defined genomes, then finished database genomes, then unfinished/draft database genomes
					if ( not astrValue ) or ( astrValue[2] != "Finished" and astrInfo[2] == "Finished" and astrValue[3] == astrInfo[3] ) or ( astrValue[3] == 0 and astrInfo[3] == 1 ):
						hashTaxon[tKey] = astrInfo
	return hashTaxon
				

def search_name( hashTaxon, strInput, strOutput ):
	
	try:
		fileIn = open( strInput, "rU" )
	except IOError:
		sys.stderr.write( "Cannot open input abundance file.\n" )
		raise
	
	try:
		fileOut = open( strOutput, "w" )
	except IOError:
		sys.stderr.write( "Cannot access output converted file.\n" )
		raise
	
	aastrOut = []
	aastrLog = [["Input Name", "IMG ID", "IMG Name", "IMG Status"]]
	for astrLine in csv.reader( fileIn, csv.excel_tab ):

		if astrLine:
			strBug, strAbun = astrLine
			astrBug = strBug.lower().split( " " )
			tBug = tuple( astrBug[:2] ) + tuple( [" ".join( astrBug[2:] )] ) if len( astrBug ) > 2 else tuple( astrBug[:2] )
			astrInfo = hashTaxon.get( tBug, [] )
			if astrInfo:
				aastrOut.append( [astrInfo[0] + ".fna", strAbun] )
				aastrLog.append( [strBug] + astrInfo )
			else:
				raise Exception( "Cannot find " + strBug + "!" )

	csv_writer_Con = csv.writer( fileOut, csv.excel_tab )
	csv_writer_Con.writerows( aastrOut )

	return aastrLog

def _main():
	parser = argparse.ArgumentParser(description='Convert abun files to GemSIM compatible format.')
	parser.add_argument('-i', metavar = "input_abund_file", dest = 'input_ref', required = True, help = "input relative abundance file")
	parser.add_argument('-o', metavar = "output_converted_file", dest = 'output_ref', required = True, help = "output converted GemSIM compatible file")
	parser.add_argument('-r', metavar = "parsed_taxa_table_file", dest = 'ref_taxa',required = True, help = "input raw taxonomy table .txt used to assign ID to taxon name")
	parser.add_argument('-l', metavar = "log_file", dest = 'strLog', required = True, help = "output log file")

	args = parser.parse_args()

	hashTaxon = parse_taxon_table( args.ref_taxa )
	aastrLog = search_name( hashTaxon, args.input_ref, args.output_ref )
	
	csv.writer( open( args.strLog, "w" ), csv.excel_tab ).writerows( aastrLog )
	csv.writer( sys.stdout, csv.excel_tab ).writerows( aastrLog )

if __name__ == "__main__":
	_main()
