#!/usr/bin/python

import argparse
import os
import sys
import csv
import re

alevel = ["Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Strain"]

def parse_taxon_table_new( taxon_path ):
	
	try:
		fileIn_taxa = open( taxon_path, "r" )
	except IOError:
		print("Cannot open taxonomy table file!")
	
	csv_in_taxa = csv.reader( fileIn_taxa, csv.excel_tab )
	hashhashhashTaxon = {}
	fHead = True

	for astrLine in csv_in_taxa:
		if fHead:
			fHead = False
			continue

		#and is necessary for we want to get
		#rid of entry without IMG taxon ID
		#This ID is in astrLine[0]
		if astrLine and astrLine[0]:
			hashLine = {}	
			hashLine["ID"] = astrLine[0]
			hashLine["Name"] = astrLine[3]
			hashLine["Status"] = astrLine[2]
			hashLine["Domain"] = astrLine[1]
			hashLine["Phylum"] = astrLine[8]
			hashLine["Class"] = astrLine[9]
			hashLine["Order"] = astrLine[10]
			hashLine["Family"] = astrLine[11]
			hashLine["Genus"] = astrLine[12]
			hashLine["Species"] = astrLine[13]
			hashLine["Strain"] = astrLine[14]

			for level in alevel:
				hashhashTaxon = hashhashhashTaxon.setdefault( level, {} )
				#Get rid of some special keywords which do not
				#represent a unique clade. unclassified is most
				#usual. sp. cf. bacterium happen in species
				#colums.
				if hashLine[level] and ( "unclassified" not in hashLine[level].lower() ) and ( hashLine[level] != "sp." ) and ( hashLine[level] != "cf." ) and ( hashLine[level] != "bacterium" ):
					hashTaxon = hashhashTaxon.setdefault( hashLine[level], {} )
					if ( hashTaxon and hashTaxon["Status"].lower() == "draft" and hashLine["Status"].lower() == "finished" ) or ( not hashTaxon ):
						hashTaxon["Name"] = hashLine["Name"]
						hashTaxon["Status"] = hashLine["Status"]
						hashTaxon["ID"] = hashLine["ID"]

	return hashhashhashTaxon

def search_name_new( abun_path, hashhashhashTaxon, out_path ):
	
	aastrLog = []
	try:
		fileIn_abun =  open( abun_path, "r" )
	except IOError:
		print "Cannot open input abundance file!"

	out_path = os.path.abspath( out_path )
        strOut_base = os.path.basename( out_path )
        strOut_path = os.path.dirname( out_path )
        if not os.path.exists( strOut_path ):
                os.makedirs( strOut_path )
	try:
        	fileOut_abun = open ( out_path, "w" )
	except IOError:
		print "Cannot access output abundance file!"

	csv_reader_in = csv.reader( fileIn_abun, csv.excel_tab )
	csv_writer_out = csv.writer( fileOut_abun, csv.excel_tab )

	hashLevel = {"d":"Domain", "p":"Phylum", "c":"Class", "o":"Order", "f":"Family", "g":"Genus", "sp": "Species", "str":"Strain"}

	aastrLog.append( ["Input Name", "IMG genome name", "IMG taxon ID", "IMG status"] )
	for astrLine in csv_reader_in:
		if astrLine:
			strBug = astrLine[0]
			strAbun = astrLine[1]

			strBug_level = hashLevel[ strBug.split("|")[-1].split("_")[0] ]
			strBug_name = strBug.split("|")[-1].split("_")[1:][0]
			
			hashhashTaxon = hashhashhashTaxon.setdefault( strBug_level, {} )
			#use regular expression to search some tricky strain or
			#species names contain in raw input. Here can only han-
			#dle strBug_name is a subset of key and shouldn't be
			#part of a word.
			ahashInfo = [ hashhashTaxon[key] for key in hashhashTaxon.keys() if ( re.search( r'(^| )' + strBug_name + r'($| )', key  ) ) ]			
			hashInf = ahashInfo[0] if ahashInfo else {}

			if hashInf:
				csv_writer_out.writerow( [hashInf["ID"] + ".fna", strAbun] )
				aastrLog.append( [strBug, hashInf["Name"], hashInf["ID"], hashInf["Status"]] )
			else:
				raise Exception( "Bug " + strBug + " does not have IMG genome!" )
	
	return aastrLog

def _main():
	parser = argparse.ArgumentParser(description='Convert abun files to GemSIM compatible format.')
	parser.add_argument('-i', metavar = "input_abund_file", dest = 'input_ref', required = True, help = "input relative abundance file")
	parser.add_argument('-o', metavar = "output_converted_file", dest = 'output_ref', required = True, help = "output converted GemSIM compatible file")
	parser.add_argument('-r', metavar = "parsed_taxa_table_file", dest = 'ref_taxa',required = True, help = "input raw taxonomy table .txt used to assign ID to taxon name")
	parser.add_argument('-l', metavar = "log_file", dest = 'strLog', required = True, help = "output log file")

	args = parser.parse_args()

	hashhashhashTaxon = parse_taxon_table_new( args.ref_taxa )
	aastrLog = search_name_new( args.input_ref, hashhashhashTaxon, args.output_ref )
	
	csv.writer( open( args.strLog, "w" ), csv.excel_tab ).writerows( aastrLog )
	csv.writer( sys.stdout, csv.excel_tab ).writerows( aastrLog )

if __name__ == "__main__":
	_main()
