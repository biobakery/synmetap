#!/usr/bin/python

import argparse
import os
import sys
import csv
import gzip
import cPickle
import re

def parse_taxon_table_new( taxon_path ):
	
	try:
		fileIn_taxa = open( taxon_path, "r" )
	except IOError:
		print("Cannot open taxonomy table file!")
	
	csv_in_taxa = csv.reader( fileIn_taxa, csv.excel_tab )
	hashhashhashTaxon = {}
	alevel = ["Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Strain"]
	fHead = True

	for astrLine in csv_in_taxa:
		if fHead:
			fHead = False
			continue

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
				#colum.
				if hashLine[level] and ( "unclassified" not in hashLine[level].lower() ) and ( hashLine[level] != "sp." ) and ( hashLine[level] != "cf." ) and ( hashLine[level] != "bacterium" ):
					hashTaxon = hashhashTaxon.setdefault( hashLine[level], {} )
					if ( hashTaxon and hashTaxon["Status"].lower() == "draft" and hashLine["Status"].lower() == "finished" ) or ( not hashTaxon ):
						hashTaxon["Name"] = hashLine["Name"]
						hashTaxon["Status"] = hashLine["Status"]
						hashTaxon["ID"] = hashLine["ID"]

	return hashhashhashTaxon

def search_name_new( abun_path, hashhashhashTaxon, out_path ):
	
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

	print "Input Name\tIMG genome name\tIMG taxon ID\tIMG status"
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
				print strBug + "\t" + hashInf["Name"] + "\t" + hashInf["ID"] + "\t" + hashInf["Status"]
			else:
				raise Exception( "Bug " + strBug + " does not have IMG genome!" )

	

def parse_taxon_table( taxon_path ):
	
	try:
		fileIn_taxa = open( taxon_path, "r" )
	except IOError:
		print("Cannot open taxonomy table file!")
	
	csv_in_taxa = csv.reader( fileIn_taxa, csv.excel_tab )
	hashhashTaxon = {}
	fHead = True

	for astrLine in csv_in_taxa:
		if fHead:
			fHead = False
			continue

		if astrLine:
			strName = astrLine[3]
			hashTaxon = hashhashTaxon.setdefault( strName, {} )
		
			if ( hashTaxon and hashTaxon["Status"].lower() == "draft" and astrLine[2].lower() == "finished" ) or ( not hashTaxon ):
				hashTaxon["ID"] = astrLine[0]
				hashTaxon["Status"] = astrLine[2]
				hashTaxon["Domain"] = astrLine[1]
				hashTaxon["Phylum"] = astrLine[8]
				hashTaxon["Class"] = astrLine[9]
				hashTaxon["Order"] = astrLine[10]
				hashTaxon["Family"] = astrLine[11]
				hashTaxon["Genus"] = astrLine[12]
				hashTaxon["Species"] = astrLine[13]
				hashTaxon["Strain"] = astrLine[14]
	return hashhashTaxon

def build_Taxon_hash( hashhashTaxon, level ):
	
	hashhashRetTaxon = {}

	for strName, hashTaxon in hashhashTaxon.iteritems():
		if hashTaxon[level] and ( hashTaxon[level].lower != "unclassified" ):
			hashRetTaxon = hashhashRetTaxon.setdefault( hashTaxon[level], {} )
			if ( hashRetTaxon and hashRetTaxon["Status"].lower() == "draft" and hashTaxon["Status"].lower() == "finished" ) or ( not hashRetTaxon ):
				hashRetTaxon["Status"] = hashTaxon["Status"]
				hashRetTaxon["ID"] = hashTaxon["ID"]
				hashRetTaxon["Name"] = strName
	
	return hashhashRetTaxon

def pickle_hash( hashhashTaxon, file_pickle ):
	
	alevel = ["Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Strain"]

	gfile_pickle = gzip.open( file_pickle, "wb" )
	
	for level in alevel:
		cPickle.dump( build_Taxon_hash( hashhashTaxon, level ), gfile_pickle )

def search_name ( ref_path, taxon_path, out_path ):
	
	fileIn_abun = open ( ref_path , 'r' )
	fileIn_taxa = open ( taxon_path , 'r' )
	
	out_path = os.path.abspath( out_path )
	strOut_base = os.path.basename( out_path )
	strOut_path = os.path.dirname( out_path )
	if not os.path.exists( strOut_path ):
		os.makedirs( strOut_path )
	fileOut_abun = open ( out_path, 'w' )
	
	csv_in_abun = csv.reader( fileIn_abun, csv.excel_tab )
	csv_out_abun = csv.writer( fileOut_abun, csv.excel_tab )
	
	for astrLine_abun in csv_in_abun:
		if astrLine_abun:
			strName = astrLine_abun[0]
			dName = len( strName )
			strAbun = astrLine_abun[1]
			strConv_name_fin = ""
			strConv_name_draft = ""
			
			fileIn_taxa.seek(0)
			csv_in_taxa = csv.reader( fileIn_taxa, csv.excel_tab )

			for astrLine_taxa in csv_in_taxa:
				strTaxaName = astrLine_taxa[3]
				strStatus = astrLine_taxa[2]
				strID = astrLine_taxa[0]

				if len( strTaxaName ) >= dName:
					if strName.lower() == strTaxaName.lower()[:dName] and strStatus.lower() == 'finished': 
						strConv_name_fin = strID + ".fna"
						print strName + "\t=>\t" + strTaxaName + "\tIMG finished"
						csv_out_abun.writerow( [strConv_name_fin, strAbun] )
						break
					if strName.lower() == strTaxaName.lower()[:dName] and strStatus.lower() == 'draft' and not strConv_name_draft:
						strConv_name_draft = strID + ".fna"
				else:
					continue
			#if no taxon found in IMG data set, write an empty converted file.
			if strConv_name_fin == "" and strConv_name_draft == "":
				raise Exception( "Taxon " + strName + " does not exist!" )
			elif strConv_name_fin == "":
				csv_out_abun.writerow( [strConv_name_draft, strAbun] )
				print strName + "\t=>\t" + strTaxaName + "\tIMG draft"

def _main():
	parser = argparse.ArgumentParser(description='Convert abun files to GemSIM compatible format.')
	parser.add_argument('-i', metavar = "input_abund_file", dest = 'input_ref', required = True, help = "input relative abundance file")
	parser.add_argument('-o', metavar = "output_converted_file", dest = 'output_ref', required = True, help = "output converted GemSIM compatible file")
	parser.add_argument('-r', metavar = "parsed_taxa_table_file", dest = 'ref_taxa',required = True, help = "input raw taxonomy table .txt used to assign ID to taxon name")
	parser.add_argument('-R', metavar = "raw_taxa_table_file", dest = "gzip_ref_taxa", help = "input parsed taxonomy table .gzip used to update .gzip file" )

	args = parser.parse_args()

	alevel = ["Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Strain"]

	hashhashhashTaxon = parse_taxon_table_new( args.ref_taxa )
	search_name_new( args.input_ref, hashhashhashTaxon, args.output_ref )
		
	"""
	pickle_file = args.ref_taxa
	raw_file =  args.raw_ref_taxa
	
	if raw_file:
		hashhashTaxon = parse_taxon_table( raw_file )
		pickle_hash( hashhashTaxon, pickle_file )

	hashhashUse = {}
	gfile = gzip.open( pickle_file, "rb" )

	alevel = ["Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Strain"]
	for level in alevel:
		hashhashUse[level] = cPickle.load( gfile )
	"""
	#search_name( args.input_ref, args.ref_taxa, args.output_ref )

if __name__ == "__main__":
	_main()
