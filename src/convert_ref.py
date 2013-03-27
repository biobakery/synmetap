#!/usr/bin/python

import argparse
import os
import sys
import csv

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
	parser.add_argument('-i', metavar="input_abund_file", dest='input_ref', required=True, help="input relative abundance file")
	parser.add_argument('-o', metavar = "output_converted_file", dest='output_ref',required=True, help="output converted GemSIM compatible file")
	parser.add_argument('-r', metavar = "input_taxa_table", dest='ref_taxa',required=True, help="input taxonomy table used to assign ID to taxon name")

	args = parser.parse_args()
	search_name( args.input_ref, args.ref_taxa, args.output_ref )

if __name__ == "__main__":
	_main()
